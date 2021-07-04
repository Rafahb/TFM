import os
import ssl
import urllib.request
import numpy as np
import pandas as pd
import streamlit as st

import functions as functions

if __name__ == "__main__":
    ssl._create_default_https_context = ssl._create_unverified_context
    response = urllib.request.urlopen('https://www.python.org')

    dfLaLiga = pd.read_csv(os.getcwd() + '/datos/statsLaLiga.csv')
    dfMatches = pd.read_csv(os.getcwd() + '/datos/statsMatches.csv')
    dfPlayers = pd.read_csv(os.getcwd() + '/datos/statsPlayers.csv')
    dfPorteros = pd.read_csv(os.getcwd() + '/datos/statsPorteros.csv')

    listTemporadas = pd.unique(dfLaLiga["Temporada"].tolist())

    st.sidebar.title('Dashboard')

    page = st.sidebar.radio("Selecciona una opción",
                            ("Estadísticas LaLiga",
                             "Estadísticas Equipo",
                             "Comparar Equipos",
                             "Comparar Jugadores",
                             "Comparar Porteros",
                             "Zonas de campo"))

    with st.sidebar.beta_expander("Métricas"):
        st.write('''
        En el siguiente enlace puedes consultar la descripción de 
        todas las métricas que encontraras en este cuadro de mando
        ''')
        st.markdown(functions.get_table_download_link(os.getcwd() + '/datos/descripcionMetricas.csv'),
                    unsafe_allow_html=True)

    if page == 'Estadísticas LaLiga':
        st.title('La Liga Española')
        tempSelected = st.selectbox(
            'Seleccionar temporada', listTemporadas, index=3)

        df_statsLaLiga = dfLaLiga.loc[(dfLaLiga['Temporada'] == tempSelected)]

        default_stats = ['xG', 'Gls.']
        stats = ['Gls.', 'Ass', 'G-TP', 'Gls./90', 'Ast/90', 'G-TP/90', 'xG', 'npxG', 'xA', 'xG/90',
                           'npxG/90',
                           'xA/90']

        clasificacion = df_statsLaLiga[['RL', 'Equipo', 'PJ', 'Pts', 'PG', 'PE', 'PP', 'GF', 'GC']]

        st.header('Clasificación La Liga')
        st.table(clasificacion.assign(hack='').set_index('hack'))

        stats_selection = st.multiselect(
            'Metrics', options=stats, default=default_stats)

        if len(stats_selection) != 2:
            st.error('Solamente está permitido comparar dos metricas')
        else:
            dfScatter = df_statsLaLiga[['Equipo'] + stats_selection]
            st.plotly_chart(functions.getScatterPlotLaLiga(dfScatter, stats_selection))

        dfUnderstat_filter = dfMatches.loc[(dfMatches['Temporada'] == tempSelected)]
        dfUnderstat_filter = dfUnderstat_filter[['Equipo','Jornada','PPDA','OPPDA','DC','ODC']]

        listMetricaUnderstat = [' ','PPDA','OPPDA','DC','ODC']

        stats_selected = st.selectbox(
            'Seleccionar metrica', listMetricaUnderstat, index=0)
        if stats_selected != ' ':
            fig = functions.statsUnderstat(dfUnderstat_filter, stats_selected)
            st.plotly_chart(fig)

    elif page == 'Estadísticas Equipo':
        col1, col2 = st.beta_columns((1, 1))
        tempSelected = col1.selectbox(
            'Seleccionar temporada', listTemporadas, index=3)

        listEquipos = pd.unique(dfPlayers.loc[(dfPlayers['Temporada'] == tempSelected)]['Equipo'].tolist()).tolist()
        listEquipos.insert(0, ' ')

        equipoSelected = col2.selectbox('Seleccionar Equipo', listEquipos, index=0)
        if equipoSelected == ' ':
            st.error('Debe seleccionar un equipo')
        if equipoSelected != ' ':
            if equipoSelected == 'Real Betis':
                equipoSelected = 'Betis'
            col3, col4 = st.beta_columns((1,2))

            #Donut e imagen
            dfLaLiga_filter = dfLaLiga.loc[
                (dfLaLiga['Temporada'] == tempSelected) & (dfLaLiga['Equipo'] == equipoSelected)]

            figDonutPartidos = functions.donutPartidos(dfLaLiga_filter)

            col3.image(os.getcwd() + "/Equipos/" + equipoSelected + '.png')
            col4.pyplot(figDonutPartidos)

            #Seleccion de metrica a representar
            stats_selection_radar = [' ', 'Gls.', 'Ass', 'G-TP', 'TP', 'TPint', 'TA', 'TR', 'Gls./90', 'Ast/90',
                                     'G+A/90',
                                     'G-TP/90', 'G+A-TP/90', 'xG', 'npxG', 'xA', 'npxG+xA', 'xG/90', 'xA/90',
                                     'xG+xA/90',
                                     'npxG/90', 'npxG+xA/90']

            stats_selected = st.selectbox('Seleccionar Métrica', stats_selection_radar, index=0)
            if equipoSelected == 'Betis':
                equipoSelected = 'Real Betis'
            if stats_selected != ' ':
                dfTeamSelected = dfPlayers.loc[(dfPlayers['Temporada'] == tempSelected) & (dfPlayers['Equipo'] == equipoSelected)]
                dfTeamSelected = dfTeamSelected.iloc[:, 0:-3]
                dfTeamSelected = dfTeamSelected.fillna(0)

                fig = functions.statsTeams(dfTeamSelected,stats_selected)
                st.pyplot(fig)

            # Gradica de jornadas
            dfMatchesSelected = dfMatches.loc[
                (dfMatches['Temporada'] == tempSelected) & (dfMatches['Equipo'] == equipoSelected) & (
                        dfMatches['Comp'] == 'La Liga')]
            dfMatchesSelected = dfMatchesSelected[
                ['Jornada', 'Sedes', 'Resultado', 'GF', 'GC', 'Adversario', 'xG', 'xGA', 'Pos.', 'Capitán',
                 'Árbitro', 'Equipo']]

            inicioJornada, finalJornada = st.select_slider(
                'Seleccionar un rango de jornadas',
                options=list(range(1, 39)),
                value=(1, 38))
            figBar = functions.statsJornadas(dfMatchesSelected, inicioJornada, finalJornada)
            st.plotly_chart(figBar)

            #Grafica de partido
            jornada_list = dfMatches['Jornada'].unique().tolist()
            jornada_list.insert(0, ' ')

            jornada_selected = st.selectbox('Seleccionar Jornada', jornada_list, index=0)
            if jornada_selected != ' ':
                dfJornadaFinal, adversario = functions.getDfJornada(dfMatches, tempSelected, jornada_selected, equipoSelected)
                figJornada = functions.barJornada(dfJornadaFinal, equipoSelected, adversario)
                #Creación del grafico de barras
                st.plotly_chart(figJornada)

                #Creación de la tabla con los datos del encuentro
                st.table(functions.getResultJornadaDF(dfJornadaFinal, equipoSelected, adversario).assign(hack='').set_index('hack'))



    elif page == 'Comparar Porteros':
        col1, col2, col3 = st.beta_columns((1, 1, 1))
        tempSelected = col1.selectbox(
            'Seleccionar temporada', listTemporadas, index=3)

        listPorteros = pd.unique(dfPorteros.loc[(dfPorteros['Temporada'] == tempSelected)]['Jugador'].tolist()).tolist()

        default_porteros = ['Jan Oblak', 'Marc-André ter Stegen']

        porteroSelected = col2.multiselect(
            'Seleccionar Portero', options=listPorteros, default=default_porteros)

        default_stats = ['PJ','GC','GC90','DaPC','Salvadas','% Salvadas','PaC','PaC%']

        stats_selection = ['PJ', 'Titular', '90 s', 'GC', 'GC90', 'DaPC', 'Salvadas',
             '% Salvadas', 'PaC', 'PaC%', 'PC', '%PC' , 'TL', 'TE', 'GCpropios', 'PSxG', 'PSxG/SoT', 'PSxG+/-',
             '/90', 'Cmp', 'PInt.', '% Cmp', 'Opp', 'Stp', '% de Stp', 'Núm. de OPA', 'Núm. de OPA/90']

        stats_radar = col3.multiselect(
            'Metricas', options=stats_selection, default=default_stats)

        if len(stats_radar) < 2:
            st.error('Debe seleccionar al menos dos métricas')
        else:
            dfBasic = dfPorteros.loc[(dfPorteros['Temporada'] == tempSelected)]
            dfFinal = dfBasic[['Jugador', 'PJ', 'Titular', '90 s', 'GC', 'GC90', 'DaPC', 'Salvadas',
             '% Salvadas', 'PaC', 'PaC%', 'PC', '%PC' , 'TL', 'TE', 'GCpropios', 'PSxG', 'PSxG/SoT', 'PSxG+/-',
             '/90', 'Cmp', 'PInt.', '% Cmp', 'Opp', 'Stp', '% de Stp', 'Núm. de OPA', 'Núm. de OPA/90']]

            dfFinal = dfFinal.fillna(0)

            ranges_cols = {c: (np.percentile(dfFinal[c].values, 0),
                               np.percentile(dfFinal[c].values, 100))
                           for c in dfFinal.columns[1:]}

            plot_radarPorteros, df_radarPorteros = functions.radarChartPorteros(dfFinal, porteroSelected, stats_radar, ranges_cols)
            st.pyplot(plot_radarPorteros)
            df_radarPorteros = df_radarPorteros.reset_index(drop=True)
            st.table(df_radarPorteros)

    elif page == 'Comparar Jugadores':
        col1, col2, col3 = st.beta_columns((1, 1, 1))
        tempSelected = col1.selectbox(
            'Seleccionar temporada', listTemporadas, index=3)

        listJugadores = pd.unique(
            dfPlayers.loc[(dfPlayers['Temporada'] == tempSelected)]['Jugador'].tolist()).tolist()

        default_players = ['Lionel Messi', 'Marcos Llorente']

        jugadoresSelected = col2.multiselect(
            'Metricas', options=listJugadores, default=default_players)

        default_stats = ['Gls.', 'Ass', 'G-TP', 'xG', 'npxG', 'xA']

        stats_selection_radar = ['Gls.','Ass','G-TP','TP','TPint','TA','TR','Gls./90','Ast/90','G+A/90','G-TP/90','G+A-TP/90','xG','npxG','xA','npxG+xA','xG/90','xA/90','xG+xA/90','npxG/90','npxG+xA/90']
        dfPlayers = dfPlayers.fillna(0)
        dfPlayers = dfPlayers.loc[(dfPlayers['Temporada'] == tempSelected)]
        df_player_radar = dfPlayers[['Jugador'] + stats_selection_radar]

        stats_radar = col3.multiselect(
            'Metricas', options=stats_selection_radar, default=default_stats)

        if len(stats_radar) < 2:
            st.error('Debe seleccionar al menos dos métricas')
        else:
            ranges_cols = {c: (np.percentile(df_player_radar[c].values, 0),
                               np.percentile(df_player_radar[c].values, 100))
                           for c in df_player_radar.columns[1:]}

            plot_radarJugador, df_radarJugador = functions.radarChartJugador(df_player_radar, jugadoresSelected, stats_radar, ranges_cols)
            st.pyplot(plot_radarJugador)
            df_radarJugador = df_radarJugador.reset_index(drop=True)
            st.table(df_radarJugador)


    elif page == 'Zonas de campo':
        col1, col2, col3 = st.beta_columns((1, 1, 1))
        tempSelected = col1.selectbox(
            'Seleccionar temporada', listTemporadas, index=3)

        df_statsZonas = dfLaLiga.loc[(dfLaLiga['Temporada'] == tempSelected)]

        listEquipos = pd.unique(dfLaLiga.loc[(dfLaLiga['Temporada'] == tempSelected)]['Equipo'].tolist()).tolist()
        listEquipos.insert(0, ' ')
        equipoSelected = col2.selectbox('Seleccionar Equipo', listEquipos, index=0)
        if equipoSelected != ' ':
            df_statsZonas = df_statsZonas[['Equipo',"Presiones Z3","Presiones Z2","Presiones Z1","Presiones","Takles Z3","Takles Z2","Takles Z1","Takles","Toques Z3","Toques Z2","Toques Z1","Toques"]]

            df_statsZonas = functions.getDFPorcentajesZonas(df_statsZonas)

            for metric_zone in ['Takles', 'Presiones', 'Toques']:
                df_zone_metric = df_statsZonas[
                    ['Equipo'] + [c for c in df_statsZonas.columns
                                 if metric_zone in c]]
                st.pyplot(functions.plot_zones(df_zone_metric, equipoSelected, metric_zone))
    else:
        if page == 'Comparar Equipos':

            st.title('Comparar Equipos')
            col1, col2, col3 = st.beta_columns((1, 1, 1))
            tempSelected = col1.selectbox(
                'Seleccionar temporada', listTemporadas, index=3)

            df = dfLaLiga.loc[(dfLaLiga['Temporada'] == tempSelected)]

            teams_competition = list(df['Equipo'])
            default_teams = ['Barcelona', 'Real Madrid']

            teams_selection = col2.multiselect(
                'Equipos', options=teams_competition,
                default=default_teams)

            default_stats = ['Gls.', 'Ass', 'G-TP', 'xG', 'npxG', 'xA']

            stats_selection_radar = ['PG','PE','PP','GF','GC','DG','Pts','Gls.', 'Ass', 'G-TP', 'Gls./90', 'Ast/90', 'G-TP/90', 'xG', 'npxG', 'xA', 'xG/90',
                                     'npxG/90', 'xA/90', 'PPDA', 'OPPDA', 'DC', 'ODC','TA','TR','2a amarilla','Fls',
                                     'Penales intentados','Penales concedidos','Penales detenidos','Penales fallidos','%Penales salvados']

            df_radar_chart = df[['Equipo'] + stats_selection_radar]
            stats_radar = col3.multiselect(
                'Metricas', options=stats_selection_radar, default=default_stats)

            if len(stats_radar) < 2:
                st.error('Debe seleccionar al menos dos métricas')
            else:

                ranges_cols = {c: (np.percentile(df_radar_chart[c].values, 0),
                                   np.percentile(df_radar_chart[c].values, 100))
                               for c in df_radar_chart.columns[1:]}

                plot_radar, df_radar = functions.radarChart(df_radar_chart, teams_selection, stats_radar, ranges_cols)
                st.pyplot(plot_radar)
                df_radar = df_radar.reset_index(drop=True)
                st.table(df_radar)