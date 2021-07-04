import base64
import os
import limits as limits
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt

def get_table_download_link(file):
    data = pd.read_csv(file, sep=";")
    csv_file = data.to_csv(index=False)
    b64 = base64.b64encode(csv_file.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="metrics_description.txt">Descargar</a>'

def limits(x, dict_ranges, col):
    if x > dict_ranges[col][1]:
        return dict_ranges[col][1]
    else:
        if x < dict_ranges[col][0]:
            return dict_ranges[col][0]
        else:
            return x

def radarChart(df, teams_selection, stats_radar, ranges_cols):
    from functions_radarchart import ComplexRadar
    df_filter = df[['Equipo'] + stats_radar]
    df_teams_filter = df_filter[df_filter.Equipo.isin(teams_selection)]
    ranges_cols_selected = [ranges_cols[s] for s in stats_radar]

    df_plot = df_teams_filter.copy()
    for c in df_plot.columns[1:]:
        df_plot[c] = df_plot[c].apply(lambda x: limits(x, ranges_cols, c))
    fig = plt.figure(figsize=(6, 6))
    radar = ComplexRadar(fig, tuple(stats_radar), ranges_cols_selected)
    for t in teams_selection:
        df_teams_t = list(df_plot[df_plot.Equipo == t].iloc[:, 1:].values[0])
        radar.plot(tuple(df_teams_t), label=t)
        radar.fill(tuple(df_teams_t), alpha=0.2)

    return fig, df_teams_filter

def radarChartPorteros(df, porterosSelected, stats_radar, ranges_cols):
    from functions_radarchart import ComplexRadar
    dfPorteros_filter = df[['Jugador'] + stats_radar]
    dfPorteros_filter = dfPorteros_filter[dfPorteros_filter.Jugador.isin(porterosSelected)]
    ranges_cols_selected = [ranges_cols[s] for s in stats_radar]

    df_plotPorteros = dfPorteros_filter.copy()
    for c in df_plotPorteros.columns[1:]:
        df_plotPorteros[c] = df_plotPorteros[c].apply(lambda x: limits(x, ranges_cols, c))
    figPortero = plt.figure(figsize=(6, 6))
    radar = ComplexRadar(figPortero, tuple(stats_radar), ranges_cols_selected)
    for t in porterosSelected:
        df_porterosFinal = list(df_plotPorteros[df_plotPorteros.Jugador == t].iloc[:, 1:].values[0])
        radar.plot(tuple(df_porterosFinal), label=t)
        radar.fill(tuple(df_porterosFinal), alpha=0.2)

    return figPortero, dfPorteros_filter

def radarChartJugador(df, players_selection, stats_radar, ranges_cols):
    from functions_radarchart import ComplexRadar
    dfJugador_filter = df[['Jugador'] + stats_radar]
    dfJugador_filter = dfJugador_filter[dfJugador_filter.Jugador.isin(players_selection)]
    ranges_cols_selected = [ranges_cols[s] for s in stats_radar]

    df_plotJugador = dfJugador_filter.copy()
    for c in df_plotJugador.columns[1:]:
        df_plotJugador[c] = df_plotJugador[c].apply(lambda x: limits(x, ranges_cols, c))
    figJugador = plt.figure(figsize=(6, 6))
    radar = ComplexRadar(figJugador, tuple(stats_radar), ranges_cols_selected)
    for t in players_selection:
        df_player_t = list(df_plotJugador[df_plotJugador.Jugador == t].iloc[:, 1:].values[0])
        radar.plot(tuple(df_player_t), label=t)
        radar.fill(tuple(df_player_t), alpha=0.2)

    return figJugador, dfJugador_filter

def radarPlayer(dfPlayers, players, metrics):
    from soccerplots.radar_chart import Radar
    # Definición de rangos
    ranges = []
    for c in metrics:
        ranges.append((dfPlayers[c].min(), dfPlayers[c].max()))

    # Extraccion de los valores
    values = dfPlayers[dfPlayers.Jugador.isin(players)][['Jugador'] + metrics].values.tolist()
    values

    # Nos quedamos sólo con las métricas
    values_metrics = []

    for l in values:
        values_metrics.append(l[1:])

    title = dict(
        title_name=values[0][0],
        title_color='firebrick',
        subtitle_name=values[0][1],
        subtitle_color='indianred',
        title_name_2=values[1][0],
        title_color_2='royalblue',
        subtitle_name_2=values[1][1],
        subtitle_color_2='steelblue',
        title_fontsize=18,
        subtitle_fontsize=15
    )

    endnote = 'FBREF / Statsbomb'

    radar = Radar()

    fig, ax = radar.plot_radar(ranges=ranges,
                               params=metrics,
                               values=values_metrics,
                               radar_color=['firebrick', 'royalblue'],
                               alphas=[.75, .6],
                               title=title,
                               endnote=endnote,
                               compare=True)
    return fig, ax

def statsLaLiga(df, stats):
    col1, col2, col3 = st.beta_columns((1, 1, 1))

    clasificacion = df[['RL', 'Equipo', 'PJ', 'Pts', 'PG', 'PE', 'PP', 'GF', 'GC']]

    col1.header('Clasificación La Liga')
    col1.table(clasificacion.assign(hack='').set_index('hack'))

    dfScatter = df[['Equipo'] + stats]

    col2.plotly_chart(getScatterPlotLaLiga(dfScatter, stats))

def getScatterPlotLaLiga(dfScatter, stats):
    fig = px.scatter(dfScatter, x=stats[0], y=stats[1],
                     hover_data=['Equipo'])

    max_x = 0.1 * (dfScatter.iloc[:, -2].max() - dfScatter.iloc[:, -2].min())
    max_y = 0.1 * (dfScatter.iloc[:, -1].max() - dfScatter.iloc[:, -1].min())

    for i in range(len(dfScatter)):
        t = dfScatter.iloc[i, 0]
        with open(os.getcwd() + "/Equipos/" + t + ".png", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        # Add the prefix that plotly will want when using the string as source
        encoded_image = "data:image/png;base64," + encoded_string
        fig.add_layout_image(
            dict(
                source=encoded_image,
                xref="x", yref="y",
                x=dfScatter.iloc[i, -2], y=dfScatter.iloc[i, -1],
                sizex=max_x, sizey=max_y,
                sizing="contain", layer='above',
                xanchor="center", yanchor="middle"))
    fig.update_traces(textposition='top center')
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))

    fig.add_shape(type='line',
                  x0=dfScatter[stats[0]].mean(),
                  y0=dfScatter[stats[1]].min(),
                  x1=dfScatter[stats[0]].mean(),
                  y1=dfScatter[stats[1]].max(),
                  line=dict(dash='dot', width=1))
    fig.add_shape(type='line',
                  x0=dfScatter[stats[0]].min(),
                  y0=dfScatter[stats[1]].mean(),
                  x1=dfScatter[stats[0]].max(),
                  y1=dfScatter[stats[1]].mean(),
                  line=dict(dash='dot', width=1))

    return fig

def statsTeams(dfTeam, stats_selected):

    dfTeam = dfTeam[['Jugador', stats_selected]]
    dfTeam = dfTeam.sort_values(stats_selected,ascending=True)

    fig, ax = plt.subplots()
    fig.set_size_inches(9, 9)

    hbars = ax.barh(y=list(dfTeam.Jugador.values), width=list(dfTeam[stats_selected].values))
    ax.bar_label(hbars, fmt='%.1f')
    ax.set_xlabel(stats_selected)

    return fig

def statsJornadas(dfMatches, inicioJornada, finalJornada):

    dfMatches_filter = dfMatches[['Jornada', 'GF', 'GC', 'Adversario']]
    dfMatchesjornadas_filter = dfMatches_filter.sort_values('Jornada', ascending=True)
    dfMatchesjornadas_filter = dfMatchesjornadas_filter.iloc[inicioJornada - 1:finalJornada, ]
    dfMatchesjornadas_filter['GF'] = dfMatchesjornadas_filter['GF'].astype(int)
    dfMatchesjornadas_filter['GC'] = dfMatchesjornadas_filter['GC'].astype(int)

    labels = list(dfMatchesjornadas_filter.Jornada.values)
    golesFavor = list(dfMatchesjornadas_filter.GF.values)
    golesContra = list(dfMatchesjornadas_filter.GC.values)
    adversario = list(dfMatchesjornadas_filter.Adversario.values)
    listAdversarioFavor = []
    listAdversarioContra = []

    for k in range(len(adversario)):
        golFavor = golesFavor[k]
        golContra = golesContra[k]
        contrincante = adversario[k]
        cadenaFavor = 'Goles a favor: '+str(golFavor)+' Adversario: '+contrincante
        cadenaContra = 'Goles en contra: ' + str(golContra) + ' Adversario: ' + contrincante
        listAdversarioFavor.append(cadenaFavor)
        listAdversarioContra.append(cadenaContra)

    textFavor = [f"{str(v)}" for v in listAdversarioFavor]
    textContra = [f"{str(v)}" for v in listAdversarioContra]

    fig = go.Figure(data=[
        go.Bar(name='Goles a favor', x=labels, y=golesFavor, marker_color='indianred', text=textFavor, hoverinfo='text'),
        go.Bar(name='Goles en contra', x=labels, y=golesContra, marker_color='lightsalmon', text=textContra, hoverinfo='text')
    ])
    # Change the bar mode
    fig.update_layout(width=800, height=500, barmode='group')

    return fig

def getCombosSelected(listTemporadas, dfPlayers):
    col1, col2, col3 = st.beta_columns((1, 1, 1))
    tempSelected = col1.selectbox(
        'Seleccionar temporada', listTemporadas, index=3)

    listEquipos = pd.unique(dfPlayers.loc[(dfPlayers['Temporada'] == tempSelected)]['Equipo'].tolist()).tolist()
    listEquipos.insert(0, '    ')
    equipoSelected = col2.selectbox('Seleccionar Equipo', listEquipos, index=0)
    listJugadores = pd.unique(
        dfPlayers.loc[(dfPlayers['Temporada'] == tempSelected) & (dfPlayers['Equipo'] == equipoSelected)][
            'Jugador'].tolist()).tolist()
    listJugadores.insert(0, '    ')
    jugadorSelected = col3.selectbox('Seleccionar Jugador', listJugadores, index=0)

    return tempSelected, equipoSelected, jugadorSelected

def getDFPorcentajesZonas(df_statsZonas):
    for i in range(len(df_statsZonas)):
        # PresionesZ3
        presionesZ3 = df_statsZonas.iloc[i, 1]
        presionesTotal = df_statsZonas.iloc[i, 4]
        valor = (100 * presionesZ3 / presionesTotal)
        df_statsZonas.iloc[i, 1] = round(valor, 1)

        # PresionesZ2
        presionesZ2 = df_statsZonas.iloc[i, 2]
        valor = (100 * presionesZ2 / presionesTotal)
        df_statsZonas.iloc[i, 2] = round(valor, 1)

        # PresionesZ1
        PresionesZ1 = df_statsZonas.iloc[i, 3]
        valor = (100 * PresionesZ1 / presionesTotal)
        df_statsZonas.iloc[i, 3] = round(valor, 1)

        # TaklesZ3
        TaklesZ3 = df_statsZonas.iloc[i, 5]
        taklesTotal = df_statsZonas.iloc[i, 8]
        valor = (100 * TaklesZ3 / taklesTotal)
        df_statsZonas.iloc[i, 5] = round(valor, 1)

        # TaklesZ2
        TaklesZ2 = df_statsZonas.iloc[i, 6]
        valor = (100 * TaklesZ2 / taklesTotal)
        df_statsZonas.iloc[i, 6] = round(valor, 1)

        # TaklesZ1
        TaklesZ1 = df_statsZonas.iloc[i, 7]
        valor = (100 * TaklesZ1 / taklesTotal)
        df_statsZonas.iloc[i, 7] = round(valor, 1)

        # ToquesZ3
        ToquesZ3 = df_statsZonas.iloc[i, 9]
        toquesTotal = df_statsZonas.iloc[i, 12]
        valor = (100 * ToquesZ3 / toquesTotal)
        df_statsZonas.iloc[i, 9] = round(valor, 1)

        # ToquesZ2
        ToquesZ2 = df_statsZonas.iloc[i, 10]
        valor = (100 * ToquesZ2 / toquesTotal)
        df_statsZonas.iloc[i, 10] = round(valor, 1)

        # ToquesZ1
        ToquesZ1 = df_statsZonas.iloc[i, 11]
        valor = (100 * ToquesZ1 / toquesTotal)
        df_statsZonas.iloc[i, 11] = round(valor, 1)

    return df_statsZonas


def draw_pitch(team, list_colors, list_values, metric_selected):
    line = "black"
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg

    fig, ax = plt.subplots(figsize=(10.4, 6.8))
    plt.xlim(-1, 121)
    plt.ylim(-4, 91)
    ax.axis('off')

    # lineas campo
    ly1 = [0, 0, 90, 90, 0]
    lx1 = [0, 120, 120, 0, 0]

    plt.plot(lx1, ly1, color=line, zorder=5)

    # area grande
    ly2 = [25, 25, 65, 65]
    lx2 = [120, 103.5, 103.5, 120]
    plt.plot(lx2, ly2, color=line, zorder=5)

    ly3 = [25, 25, 65, 65]
    lx3 = [0, 16.5, 16.5, 0]
    plt.plot(lx3, ly3, color=line, zorder=5)

    # porteria
    ly4 = [40.5, 40.7, 48, 48]
    lx4 = [120, 120.2, 120.2, 120]
    plt.plot(lx4, ly4, color=line, zorder=5)

    ly5 = [40.5, 40.5, 48, 48]
    lx5 = [0, -0.2, -0.2, 0]
    plt.plot(lx5, ly5, color=line, zorder=5)

    # area pequeña
    ly6 = [36, 36, 54, 54]
    lx6 = [120, 114.5, 114.5, 120]
    plt.plot(lx6, ly6, color=line, zorder=5)

    ly7 = [36, 36, 54, 54]
    lx7 = [0, 5.5, 5.5, 0]
    plt.plot(lx7, ly7, color=line, zorder=5)

    # lineas y puntos
    vcy5 = [0, 90]
    vcx5 = [60, 60]
    plt.plot(vcx5, vcy5, color=line, zorder=5)

    plt.scatter(109, 45, color=line, zorder=5)
    plt.scatter(11, 45, color=line, zorder=5)
    plt.scatter(60, 45, color=line, zorder=5)

    # circulos
    circle1 = plt.Circle((109.5, 45), 9.15, ls='solid', lw=1.5, color=line, fill=False, zorder=1, alpha=1)
    circle2 = plt.Circle((10.5, 45), 9.15, ls='solid', lw=1.5, color=line, fill=False, zorder=1, alpha=1)
    circle3 = plt.Circle((60, 45), 9.15, ls='solid', lw=1.5, color=line, fill=False, zorder=2, alpha=1)

    # rectangulos
    rec1 = plt.Rectangle((103.5, 30), 16, 30, ls='-', color="white", zorder=1, alpha=1)
    rec2 = plt.Rectangle((0, 30), 16.5, 30, ls='-', color="white", zorder=1, alpha=1)
    # rec3 = plt.Rectangle((-1,-1), 122, 92,color=pitch,zorder=1,alpha=1)

    # colors
    zone1 = plt.Rectangle((0, 0), 40, 90, color=list_colors[0], zorder=1, alpha=0.5)
    zone2 = plt.Rectangle((40, 0), 40, 90, color=list_colors[1], zorder=1, alpha=0.5)
    zone3 = plt.Rectangle((80, 0), 40, 90, color=list_colors[2], zorder=1, alpha=0.5)

    # ax.add_artist(rec3)
    ax.add_artist(circle1)
    ax.add_artist(circle2)
    ax.add_artist(rec1)
    ax.add_artist(rec2)
    ax.add_artist(circle3)

    # zones
    ax.add_artist(zone1)
    ax.add_artist(zone2)
    ax.add_artist(zone3)

    # text
    plt.text(17, 80, str(list_values[0]) + " %", color='black',
             weight='semibold', size=12)
    plt.text(46, 80, str(list_values[1]) + " %", color='black',
             weight='semibold', size=12)
    plt.text(97, 80, str(list_values[2]) + " %", color='black',
             weight='semibold', size=12)

    # flecha
    plt.arrow(55, -3, dx=10, dy=0, linewidth=1.5, head_width=1)

    # image
    img = mpimg.imread(os.getcwd() + "/Equipos/" + team + '.png')
    plt.imshow(img, zorder=0, extent=[35, 85, 20, 70])

    plt.title(metric_selected, fontweight='semibold')

    return fig


def color_percentiles_zones(val):
    if val < 20:
        color = 'red'
    else:
        if val < 30:
            color = 'darkorange'
        else:
            if val < 45:
                color = 'gold'
            else:
                color = 'green'
    return color

def plot_zones(df_zone, team_zone_select, metric_selected):
    df_zone_percent = df_zone.iloc[:,0:4]

    i_team = [i for i in range(len(df_zone_percent))
              if df_zone_percent.iloc[i,0] == team_zone_select][0]

    colors_team = list(df_zone_percent.iloc[i_team,1:].\
                       apply(color_percentiles_zones).values)

    values_team = list(df_zone_percent.iloc[i_team,1:].values)

    fig = draw_pitch(team_zone_select, colors_team, values_team, metric_selected)
    return fig

def radarPlayer(dfPlayers, players, metrics):
    from soccerplots.radar_chart import Radar
    # Definición de rangos
    ranges = []
    for c in metrics:
        ranges.append((dfPlayers[c].min(), dfPlayers[c].max()))

    # Extraccion de los valores
    values = dfPlayers[dfPlayers.Jugador.isin(players)][['Jugador'] + metrics].values.tolist()
    values

    # Nos quedamos sólo con las métricas
    values_metrics = []

    for l in values:
        values_metrics.append(l[1:])

    title = dict(
        title_name=values[0][0],
        title_color='firebrick',
        subtitle_name=values[0][1],
        subtitle_color='indianred',
        title_name_2=values[1][0],
        title_color_2='royalblue',
        subtitle_name_2=values[1][1],
        subtitle_color_2='steelblue',
        title_fontsize=18,
        subtitle_fontsize=15
    )

    endnote = 'FBREF / Statsbomb'

    radar = Radar()

    fig, ax = radar.plot_radar(ranges=ranges,
                               params=metrics,
                               values=values_metrics,
                               radar_color=['firebrick', 'royalblue'],
                               alphas=[.75, .6],
                               title=title,
                               endnote=endnote,
                               compare=True)
    return fig, ax

def donutPartidos(dfTeam):
    dfResumeTeam = dfTeam[['Equipo','PG','PE','PP']]

    valuesPartidos = dfResumeTeam[['PG','PE','PP']].values.tolist()
    metricsPartidos = ['Partidos Ganados: ' +str(dfResumeTeam.iloc[0]['PG']),
                       'Partidos Empatados: ' +str(dfResumeTeam.iloc[0]['PE']),
                       'Partidos Perdidos: '+str(dfResumeTeam.iloc[0]['PP']),]
    explode = (0, 0,0)

    plt.figure(1)
    plt.pie(valuesPartidos[0],explode=explode, labels=metricsPartidos, colors=["#60D394", "#FFD97D", "#EE6055"], autopct="%1.1f %%", shadow=True)
    plt.axis("equal")

    return plt

def statsUnderstat(dfUnderstat, statSelected):
    dfUnderstat = dfUnderstat.sort_values('Jornada', ascending=True)
    fig = px.line(dfUnderstat, x="Jornada",
                  y=statSelected,
                  color="Equipo")
    return fig

def getDfJornada(dfMatches, tempSelected, jornada_selected, equipoSelected):
    dfJornadaSelected = dfMatches.loc[
        (dfMatches['Temporada'] == tempSelected) & (dfMatches['Equipo'] == equipoSelected) & (
                dfMatches['Jornada'] == jornada_selected)]
    adversario = dfJornadaSelected.iloc[0]['Adversario']
    if adversario == 'Betis':
        adversario = 'Real Betis'
    dfAdversario = dfMatches.loc[
        (dfMatches['Temporada'] == tempSelected) & (dfMatches['Equipo'] == adversario) & (
                dfMatches['Jornada'] == jornada_selected)]

    return dfAdversario.append(dfJornadaSelected, ignore_index=True), adversario

def barJornada(dfMatches, equipo, adversario):

    dfMatchesjornadas_filter = dfMatches[['Equipo','xG','xGA','PPDA','OPPDA','DC','ODC']]

    listLabels = ['xG','xGA','PPDA','OPPDA','DC','ODC']

    golesEsperados = list(dfMatchesjornadas_filter.xG.values)
    assistenciasEsperadas = list(dfMatchesjornadas_filter.xGA.values)
    ppda = list(dfMatchesjornadas_filter.PPDA.values)
    oppda = list(dfMatchesjornadas_filter.OPPDA.values)
    dc = list(dfMatchesjornadas_filter.DC.values)
    odc = list(dfMatchesjornadas_filter.ODC.values)
    listEquiposJornada = [equipo, adversario]

    figJornada = go.Figure(data=[
        go.Bar(name=listLabels[0], x=listEquiposJornada, y=golesEsperados, marker_color='yellowgreen'),
        go.Bar(name=listLabels[1], x=listEquiposJornada, y=assistenciasEsperadas, marker_color='darkorange'),
        go.Bar(name=listLabels[2], x=listEquiposJornada, y=ppda, marker_color='chocolate'),
        go.Bar(name=listLabels[3], x=listEquiposJornada, y=oppda, marker_color='goldenrod'),
        go.Bar(name=listLabels[4], x=listEquiposJornada, y=dc, marker_color='lightsalmon'),
        go.Bar(name=listLabels[5], x=listEquiposJornada, y=odc, marker_color='indianred')
    ])
    # Change the bar mode
    figJornada.update_layout(width=800, height=500, barmode='group')

    return figJornada

def getResultJornadaDF(dfMatches, equipo, adversario):
    golLocal = dfMatches.iloc[0]['GF']
    golVisitante = dfMatches.iloc[0]['GC']
    arbitro = dfMatches.iloc[0]['Árbitro']
    horaPartido = dfMatches.iloc[0]['Hora']
    fechaPartido = dfMatches.iloc[0]['Fecha']

    if dfMatches.iloc[0]['Sedes'] == 'Local':
        data = {'Fecha': [fechaPartido], 'Hora':[horaPartido], 'Equipo local': [equipo], 'Gol local': [golLocal],
                'Gol visitante': [golVisitante], 'Equipo visitante': [adversario], 'Árbitro': [arbitro]}
    else:
        data = {'Fecha': [fechaPartido], 'Hora':[horaPartido], 'Equipo local': [adversario], 'Gol local': [golLocal],
                'Gol visitante': [golVisitante], 'Equipo visitante': [equipo], 'Árbitro': [arbitro]}

    dfResultJornada = pd.DataFrame(data)
    return dfResultJornada