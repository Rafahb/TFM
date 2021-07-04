import requests
import pandas as pd
import os
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings('ignore')


def getDataFrameTeams(tables, temp, listTemp):
    for j in range(0, len(tables)):

        table_standard = tables[j]
        stats = table_standard.find('tbody').find_all('tr')
        # Encabezado de la tabla
        cols_list = [table_standard.find_all('th', scope='col')[i].text
                     for i in range(len(table_standard.find_all('th', scope='col')))]
        cols = cols_list[:[i for i in range(len(cols_list)) if cols_list[i] == 'Equipo'][1]]

        # Obtenemos valores
        list_stats = []
        for i in range(len(stats)):
            club = stats[i].find_all('th')[0].text
            values = [stats[i].find_all('td')[j].text for j in range(len(stats[i].find_all('td')))]
            list_stats.append([club] + values)

        if j == 0:
            cols.pop()

        if j == 1:
            # Añado a las ultimas columnas el valor 90min
            for k in range(len(cols) - 5, len(cols)):
                cols[k] = cols[k] + '/90'
            for m in range(len(cols) - 14, len(cols)-9):
                cols[m] = cols[m] + '/90'

        if j == 2:
            cols[len(cols) - 5] = "Penales intentados"
            cols[len(cols) - 4] = "Penales concedidos"
            cols[len(cols) - 3] = "Penales detenidos"
            cols[len(cols) - 2] = "Penales fallidos"
            cols[len(cols) - 1] = "%Penales salvados"

        #Acciones defensivas del equipo
        if j == 8:
            cols[len(cols) - 9] = "Presiones Z3"
            cols[len(cols) - 10] = "Presiones Z2"
            cols[len(cols) - 11] = "Presiones Z1"
            cols[len(cols) - 14] = "Presiones"
            cols[len(cols) - 19] = "Takles Z3"
            cols[len(cols) - 20] = "Takles Z2"
            cols[len(cols) - 21] = "Takles Z1"
            cols[len(cols) - 23] = "Takles"

        #Posesion del equipo
        if j == 9:
            cols[len(cols) - 20] = "Toques Z3"
            cols[len(cols) - 21] = "Toques Z2"
            cols[len(cols) - 22] = "Toques Z1"
            cols[len(cols) - 24] = "Toques"

        if temp == listTemp[0]:
            temporada = '2017-2018'
        if temp == listTemp[1]:
            temporada = '2018-2019'
        if temp == listTemp[2]:
            temporada = '2019-2020'
        if temp == listTemp[3]:
            temporada = '2020-2021'

        # Construimos el dataframe
        final_data = pd.DataFrame(list_stats, columns=cols)

        if j == 0:
            final_data = final_data.applymap((lambda x: "".join(x.lstrip()) if type(x) is str else x))
            final_data0 = final_data[['Equipo', 'RL', 'PJ', 'PG', 'PE', 'PP', 'GF', 'GC', 'DG', 'Pts']]

        if j == 1:
            final_data1 = final_data[['Equipo', 'Gls.', 'Ass', 'G-TP', 'Gls./90', 'Ast/90', 'G-TP/90', 'xG', 'npxG', 'xA', 'xG/90', 'npxG/90', 'xA/90']]

        if j == 2:
            final_data2 = final_data[
                ['Equipo', 'Penales intentados', 'Penales concedidos', 'Penales detenidos', 'Penales fallidos',
                 '%Penales salvados']]

        if j == 8:
            final_data8 = final_data[['Equipo',"Presiones Z3","Presiones Z2","Presiones Z1","Presiones","Takles Z3","Takles Z2","Takles Z1","Takles"]]

        if j == 9:
            final_data9 = final_data[['Equipo',"Toques Z3","Toques Z2","Toques Z1","Toques"]]

        if j == 11:
            final_data12 = final_data[['Equipo', 'TA', 'TR', '2a amarilla', 'Fls', 'FR']]

    final_data = pd.merge(final_data0, final_data1)
    final_data = pd.merge(final_data, final_data2)
    final_data = pd.merge(final_data, final_data8)
    final_data = pd.merge(final_data, final_data9)
    final_data = pd.merge(final_data, final_data12)

    season = []
    for k in list_stats:
        season.append(temporada)
    final_data['Temporada'] = season

    return final_data


# Extraccion datos de datos estadisticos equipos FBREF, por temporadas
def scrapingGeneral(dfStatUndersat):
    temp1718 = 'https://fbref.com/es/comps/12/1652/Estadisticas-2017-2018-La-Liga'
    temp1819 = 'https://fbref.com/es/comps/12/1886/Estadisticas-2018-2019-La-Liga'
    temp1920 = 'https://fbref.com/es/comps/12/3239/Estadisticas-2019-2020-La-Liga'
    temp2021 = 'https://fbref.com/es/comps/12/Estadisticas-de-La-Liga'

    listTemp = [temp1718, temp1819, temp1920, temp2021]

    for temp in listTemp:
        page = requests.get(temp)
        soup = BeautifulSoup(page.text, 'lxml')  # Obtenemos el HTML

        tables = soup.find_all("div", attrs={"class": "table_wrapper tabbed"})
        # Obtenemos la tabla

        if temp == listTemp[0]:
            temporada = 'Temp1718'
            df1718 = getDataFrameTeams(tables, temp, listTemp)
        if temp == listTemp[1]:
            temporada = 'Temp1819'
            df1819 = getDataFrameTeams(tables, temp, listTemp)
        if temp == listTemp[2]:
            temporada = 'Temp1920'
            df1920 = getDataFrameTeams(tables, temp, listTemp)
        if temp == listTemp[3]:
            temporada = 'Temp2021'
            df2021 = getDataFrameTeams(tables, temp, listTemp)

    finalDF = df1718.append(df1819, ignore_index=True)
    finalDF = finalDF.append(df1920, ignore_index=True)
    finalDF = finalDF.append(df2021, ignore_index=True)
    finalDF = pd.merge(finalDF, dfStatUndersat, how="outer")

    # Cambiamos los valores vacios o nulos por 0
    finalDF = finalDF.fillna(0)

    finalDF.to_csv(os.getcwd() + '/datos/statsLaLiga.csv')
    print('Almacenada informacion de la liga')
