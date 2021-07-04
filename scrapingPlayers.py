import requests
import pandas as pd
import os
from bs4 import BeautifulSoup

import warnings
warnings.filterwarnings('ignore')

def getDataFramePlayers():
    temporada = ['2017-2018/', '2018-2019/', '2019-2020/', '']
    bandera = True

    #Obtenemos las url de los datos
    for temp in temporada:
        #listURL = []
        atletico = 'https://fbref.com/es/equipos/db3b9613/' + temp + 'Estadisticas-de-Atletico-Madrid'
        madrid = 'https://fbref.com/es/equipos/53a2f082/' + temp + 'Estadisticas-de-Real-Madrid'
        barcelona = 'https://fbref.com/es/equipos/206d90db/' + temp + 'Estadisticas-de-Barcelona'
        sevilla = 'https://fbref.com/es/equipos/ad2be733/' + temp + 'Estadisticas-de-Sevilla'
        realsociedad = 'https://fbref.com/es/equipos/e31d1cd9/' + temp + 'Estadisticas-de-Real-Sociedad'
        betis = 'https://fbref.com/es/equipos/fc536746/' + temp + 'Estadisticas-de-Real-Betis'
        villareal = 'https://fbref.com/es/equipos/2a8183b3/' + temp + 'Estadisticas-de-Villarreal'
        celtavigo = 'https://fbref.com/es/equipos/f25da7fb/' + temp + 'Estadisticas-de-Celta-Vigo'
        bilbao = 'https://fbref.com/es/equipos/2b390eca/' + temp + 'Estadisticas-de-Athletic-Club'
        valencia = 'https://fbref.com/es/equipos/dcc91a7b/' + temp + 'Estadisticas-de-Valencia'
        levante = 'https://fbref.com/es/equipos/9800b6a1/' + temp + 'Estadisticas-de-Levante'
        getafe = 'https://fbref.com/es/equipos/7848bd64/' + temp + 'Estadisticas-de-Getafe'
        alaves = 'https://fbref.com/es/equipos/8d6fd021/' + temp + 'Estadisticas-de-Alaves'
        eibar = 'https://fbref.com/es/equipos/bea5c710/' + temp + 'Estadisticas-de-Eibar'
        listURL = [atletico, madrid, barcelona, sevilla, realsociedad, betis, villareal, celtavigo, bilbao, valencia, levante, getafe, alaves, eibar]
        if temp == temporada[3]:
            cadiz = 'https://fbref.com/es/equipos/ee7c297c/' + temp + 'Estadisticas-de-Cadiz'
            elche = 'https://fbref.com/es/equipos/6c8b07df/' + temp + 'Estadisticas-de-Elche'
            huesca = 'https://fbref.com/es/equipos/c6c493e6/' + temp + 'Estadisticas-de-Huesca'
            valladolid = 'https://fbref.com/es/equipos/17859612/' + temp + 'Estadisticas-de-Valladolid'
            osasuna = 'https://fbref.com/es/equipos/03c57e2b/' + temp + 'Estadisticas-de-Osasuna'
            granada = 'https://fbref.com/es/equipos/a0435291/' + temp + 'Estadisticas-de-Granada'
            listURL.append(cadiz)
            listURL.append(elche)
            listURL.append(huesca)
            listURL.append(valladolid)
            listURL.append(osasuna)
            listURL.append(granada)
        if temp == temporada[2]:
            osasuna = 'https://fbref.com/es/equipos/03c57e2b/' + temp + 'Estadisticas-de-Osasuna'
            granada = 'https://fbref.com/es/equipos/a0435291/' + temp + 'Estadisticas-de-Granada'
            leganes = 'https://fbref.com/es/equipos/7c6f2c78/' + temp + 'Estadisticas-de-Leganes'
            mallorca = 'https://fbref.com/es/equipos/2aa12281/' + temp + 'Estadisticas-de-Mallorca'
            espanyol = 'https://fbref.com/es/equipos/a8661628/' + temp + 'Estadisticas-de-Espanyol'
            valladolid = 'https://fbref.com/es/equipos/17859612/' + temp + 'Estadisticas-de-Valladolid'
            listURL.append(valladolid)
            listURL.append(osasuna)
            listURL.append(granada)
            listURL.append(mallorca)
            listURL.append(leganes)
            listURL.append(espanyol)
        if temp == temporada[1]:
            valladolid = 'https://fbref.com/es/equipos/17859612/' + temp + 'Estadisticas-de-Valladolid'
            girona = 'https://fbref.com/es/equipos/9024a00a/' + temp + 'Estadisticas-de-Girona'
            huesca = 'https://fbref.com/es/equipos/c6c493e6/' + temp + 'Estadisticas-de-Huesca'
            rayo = 'https://fbref.com/es/equipos/98e8af82/' + temp + 'Estadisticas-de-Rayo-Vallecano'
            espanyol = 'https://fbref.com/es/equipos/a8661628/' + temp + 'Estadisticas-de-Espanyol'
            leganes = 'https://fbref.com/es/equipos/7c6f2c78/' + temp + 'Estadisticas-de-Leganes'
            listURL.append(leganes)
            listURL.append(espanyol)
            listURL.append(valladolid)
            listURL.append(girona)
            listURL.append(rayo)
            listURL.append(huesca)
            listURL.append(leganes)
        if temp == temporada[0]:
            depor = 'https://fbref.com/es/equipos/2a60ed82/' + temp + 'Estadisticas-de-Deportivo-La-Coruna'
            laspalmas = 'https://fbref.com/es/equipos/0049d422/' + temp + 'Estadisticas-de-Las-Palmas'
            espanyol = 'https://fbref.com/es/equipos/a8661628/' + temp + 'Estadisticas-de-Espanyol'
            girona = 'https://fbref.com/es/equipos/9024a00a/' + temp + 'Estadisticas-de-Girona'
            malaga = 'https://fbref.com/es/equipos/1c896955/' + temp + 'Estadisticas-de-Malaga'
            leganes = 'https://fbref.com/es/equipos/7c6f2c78/' + temp + 'Estadisticas-de-Leganes'
            listURL.append(leganes)
            listURL.append(espanyol)
            listURL.append(girona)
            listURL.append(depor)
            listURL.append(laspalmas)
            listURL.append(malaga)

        for teamsURL in listURL:
            page = requests.get(teamsURL)
            soup = BeautifulSoup(page.text, 'lxml') #Obtenemos el HTML

            tables = soup.find_all("div", attrs={"class": "table_wrapper tabbed"})

            #Obtenemos la tabla
            table_standard = tables[0]
            table_porteros = tables[2]
            table_porterosAvanzados = tables[3]

            stats = table_standard.find('tbody').find_all('tr')
            stats_porteros = table_porteros.find('tbody').find_all('tr')
            stats_porterosAvanzados = table_porterosAvanzados.find('tbody').find_all('tr')

            #Encabezado de la tabla
            cols_list = [table_standard.find_all('th', scope='col')[i].text
                         for i in range(len(table_standard.find_all('th', scope='col')))]

            cols_list_porteros = [table_porteros.find_all('th', scope='col')[i].text
                         for i in range(len(table_porteros.find_all('th', scope='col')))]

            cols_list_porterosAvanzados = [table_porterosAvanzados.find_all('th', scope='col')[i].text
                         for i in range(len(table_porterosAvanzados.find_all('th', scope='col')))]

            # Obtenemos valores
            list_stats = []
            for i in range(len(stats)):
                club = stats[i].find_all('th')[0].text
                values = [stats[i].find_all('td')[j].text for j in range(len(stats[i].find_all('td')))]
                list_stats.append([club] + values)

            #Valores de porteros
            list_stats_porteros = []
            for i in range(len(stats_porteros)):
                club = stats_porteros[i].find_all('th')[0].text
                values = [stats_porteros[i].find_all('td')[j].text for j in
                          range(len(stats_porteros[i].find_all('td')))]
                list_stats_porteros.append([club] + values)

            #valores de porteros avanzados
            list_stats_porterosAvanzadas = []
            for i in range(len(stats_porterosAvanzados)):
                club = stats_porterosAvanzados[i].find_all('th')[0].text
                values = [stats_porterosAvanzados[i].find_all('td')[j].text for j in
                          range(len(stats_porterosAvanzados[i].find_all('td')))]
                list_stats_porterosAvanzadas.append([club] + values)

            for k in range(len(cols_list) - 6, len(cols_list) - 1):
                cols_list[k] = cols_list[k] + '/90'
            for h in range(len(cols_list) - 15, len(cols_list) - 10):
                cols_list[h] = cols_list[h] + '/90'

            cols_list_porteros[19] = 'PConcedidos'
            cols_list_porteros[20] = 'PC'
            cols_list_porteros[21] = 'Pfallidos'
            cols_list_porteros[22] = '%PC'
            cols_list_porterosAvanzados[9] = cols_list_porterosAvanzados[9] + 'propios'
            cols_list_porterosAvanzados[15] = 'P'+cols_list_porterosAvanzados[15]

            title = soup.find_all("span")
            equipo = title[7].text.replace("Estadísticas de ", "")
            lista = equipo.split(" ")
            seasonTeam = lista[len(lista) - 1]
            teamList = equipo.split(" " + seasonTeam)
            nameTeam = teamList[0]
            season = []
            team = []

            for k in list_stats:
                season.append(seasonTeam)
                team.append(nameTeam)

            season_portero = []
            team_portero = []
            for k in list_stats_porteros:
                season_portero.append(seasonTeam)
                team_portero.append(nameTeam)

            season_portero_avanzada = []
            team_portero_avanzada = []
            for k in list_stats_porterosAvanzadas:
                season_portero_avanzada.append(seasonTeam)
                team_portero_avanzada.append(nameTeam)

            # Construimos el dataframe
            if bandera:
                final_data = pd.DataFrame(list_stats, columns=cols_list)
                final_data_porteros = pd.DataFrame(list_stats_porteros, columns=cols_list_porteros)
                final_data_porterosAvanzadas = pd.DataFrame(list_stats_porterosAvanzadas,
                                                            columns=cols_list_porterosAvanzados)

                final_data['Temporada'] = season
                final_data['Equipo'] = team
                final_data_porteros['Temporada'] = season_portero
                final_data_porteros['Equipo'] = team_portero
                final_data_porterosAvanzadas['Temporada'] = season_portero_avanzada
                final_data_porterosAvanzadas['Equipo'] = team_portero_avanzada

                bandera = False
            else:
                finalDF = pd.DataFrame(list_stats, columns=cols_list)
                finalDF_data_porteros = pd.DataFrame(list_stats_porteros, columns=cols_list_porteros)
                finalDF_data_porterosAvanzadas = pd.DataFrame(list_stats_porterosAvanzadas,
                                                            columns=cols_list_porterosAvanzados)

                finalDF['Temporada'] = season
                finalDF['Equipo'] = team
                finalDF_data_porteros['Temporada'] = season_portero
                finalDF_data_porteros['Equipo'] = team_portero
                finalDF_data_porterosAvanzadas['Temporada'] = season_portero_avanzada
                finalDF_data_porterosAvanzadas['Equipo'] = team_portero_avanzada
                bandera = True

            if bandera:
                final_data = final_data.append(finalDF, ignore_index=True)
                final_data_porteros = final_data_porteros.append(finalDF_data_porteros, ignore_index=True)
                final_data_porterosAvanzadas = final_data_porterosAvanzadas.append(finalDF_data_porterosAvanzadas, ignore_index=True)
                bandera = False

    #Eliminamos las columnas que no necesitamos y seleccionamos las que necesitamos
    final_data.drop(['Partidos'], axis=1)

    final_data_porteros = final_data_porteros[
        ['Jugador','País','Posc','Edad','PJ','Titular','Mín','90 s','GC','GC90','DaPC','Salvadas','% Salvadas','PaC','PaC%','PC','%PC','Temporada','Equipo']]

    final_data_porterosAvanzadas = final_data_porterosAvanzadas[[
          'Jugador', 'TL', 'TE', 'GCpropios', 'PSxG', 'PSxG/SoT','PSxG+/-','/90', 'Cmp', 'PInt.', '% Cmp', 'Opp', 'Stp','% de Stp', 'Núm. de OPA', 'Núm. de OPA/90', 'Temporada'
    ]]

    final_data_porteros = final_data_porteros.fillna(0)
    final_data_porterosAvanzadas = final_data_porterosAvanzadas.fillna(0)

    #Mergeamos los dataframe de porteros
    final_data_porteros_merge = pd.merge(final_data_porteros, final_data_porterosAvanzadas, how="outer")

    #Cambiamos los valores vacios o nulos por 0
    final_data = final_data.fillna(0)
    final_data_porteros_merge = final_data_porteros_merge.fillna(0)

    final_data.to_csv(os.getcwd() + '/datos/statsPlayers.csv')
    final_data_porteros_merge.to_csv(os.getcwd() + '/datos/statsPorteros.csv')
    print('Almacenada informacion de Jugadores y Porteros')