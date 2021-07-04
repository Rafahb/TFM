# Librerias de interés
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

def getDataFrameUnderstat():
    url2020_21 = 'https://understat.com/league/La_liga'
    url2019_20 = 'https://understat.com/league/La_liga/2019'
    url2018_19 = 'https://understat.com/league/La_liga/2018'
    url2017_18 = 'https://understat.com/league/La_liga/2017'
    urlList = [url2017_18,url2018_19,url2019_20,url2020_21]

    listPPDA = []
    listOPPDA = []
    listDC = []
    listODC = []
    listEquipo = []
    listTemporada = []
    listJornada = []

    listFinalEquipo = []
    listFinalTemporada = []
    listFinalPPDA = []
    listFinalOPPDA = []
    listFinalDC = []
    listFinalODC = []

    for temp in urlList:
        if temp == url2020_21:
            temporada = '2020-2021'
        if temp == url2019_20:
            temporada = '2019-2020'
        if temp == url2018_19:
            temporada = '2018-2019'
        if temp == url2017_18:
            temporada = '2017-2018'

        res = requests.get(temp)
        soup = BeautifulSoup(res.content, 'lxml')
        scripts = soup.find_all('script')
        strings = scripts[2].string

        # Eliminamos simbolos innecesarios y creamos el JSON
        ind_start = strings.index("('")+2
        ind_end = strings.index("')")
        json_data = strings[ind_start:ind_end]
        json_data = json_data.encode('utf8').decode('unicode_escape')

        # Creamos el JSON y lo visualizamos
        data = json.loads(json_data)

        for key in data.keys():
            anteriorAttPPDA=0
            anteriorDefPPDA=0
            anteriorAttOPPDA=0
            anteriorDefOPPDA=0
            anteriorODC = 0
            anteriorDC = 0

            for i in range(0, len(data[key]['history'])):
                attPPDA = data[key]['history'][i]['ppda']['att']
                defPPDA = data[key]['history'][i]['ppda']['def']
                anteriorAttPPDA=anteriorAttPPDA+attPPDA
                anteriorDefPPDA=anteriorDefPPDA+defPPDA
                ppdaFinal = anteriorAttPPDA / anteriorDefPPDA
                ppdaFinal = round(ppdaFinal, 2)
                listPPDA.append(ppdaFinal)

                attOPPDA = data[key]['history'][i]['ppda_allowed']['att']
                defOPPDA = data[key]['history'][i]['ppda_allowed']['def']
                anteriorAttOPPDA=anteriorAttOPPDA+attOPPDA
                anteriorDefOPPDA=anteriorDefOPPDA+defOPPDA
                oppdaFinal = anteriorAttOPPDA / anteriorDefOPPDA
                oppdaFinal = round(oppdaFinal, 2)
                listOPPDA.append(oppdaFinal)

                valorDC = data[key]['history'][i]['deep']
                anteriorDC = anteriorDC + valorDC
                listDC.append(anteriorDC)
                valorODC = data[key]['history'][i]['deep_allowed']
                anteriorODC = anteriorODC + valorODC
                listODC.append(anteriorODC)
                equipo = data[key]['title']
                listEquipo.append(equipo)
                listTemporada.append(temporada)
                jornada = 'J'+str(i+1)
                listJornada.append(jornada)

                if i == (len(data[key]['history'])-1):
                    listFinalEquipo.append(equipo)
                    listFinalTemporada.append(temporada)
                    listFinalOPPDA.append(oppdaFinal)
                    listFinalPPDA.append(ppdaFinal)
                    listFinalDC.append(anteriorDC)
                    listFinalODC.append(anteriorODC)

    #Renombramos nombres de equipos
    for equipo in range(0,len(listEquipo)):
        if listEquipo[equipo] == 'Malaga':
            listEquipo[equipo] = 'Málaga'
        if listEquipo[equipo] == 'Deportivo La Coruna':
            listEquipo[equipo] = 'La Coruña'
        if listEquipo[equipo] == 'Atletico Madrid':
            listEquipo[equipo] = 'Atlético Madrid'
        if listEquipo[equipo] == 'Real Betis':
            listEquipo[equipo] = 'Betis'
        if listEquipo[equipo] == 'Alaves':
            listEquipo[equipo] = 'Alavés'
        if listEquipo[equipo] == 'Leganes':
            listEquipo[equipo] = 'Leganés'
        if listEquipo[equipo] == 'Real Valladolid':
            listEquipo[equipo] = 'Valladolid'
        if listEquipo[equipo] == 'SD Huesca':
            listEquipo[equipo] = 'Huesca'
        if listEquipo[equipo] == 'Cadiz':
            listEquipo[equipo] = 'Cádiz'

    for equipo in range(0,len(listFinalEquipo)):
        if listFinalEquipo[equipo] == 'Malaga':
            listFinalEquipo[equipo] = 'Málaga'
        if listFinalEquipo[equipo] == 'Deportivo La Coruna':
            listFinalEquipo[equipo] = 'La Coruña'
        if listFinalEquipo[equipo] == 'Atletico Madrid':
            listFinalEquipo[equipo] = 'Atlético Madrid'
        if listFinalEquipo[equipo] == 'Real Betis':
            listFinalEquipo[equipo] = 'Betis'
        if listFinalEquipo[equipo] == 'Alaves':
            listFinalEquipo[equipo] = 'Alavés'
        if listFinalEquipo[equipo] == 'Leganes':
            listFinalEquipo[equipo] = 'Leganés'
        if listFinalEquipo[equipo] == 'Real Valladolid':
            listFinalEquipo[equipo] = 'Valladolid'
        if listFinalEquipo[equipo] == 'SD Huesca':
            listFinalEquipo[equipo] = 'Huesca'
        if listFinalEquipo[equipo] == 'Cadiz':
            listFinalEquipo[equipo] = 'Cádiz'

    # Cambiamos el dato de semana por jornada y numero
    for i in range(0,len(listJornada)):
        if listJornada[i] == 'J1':
            listJornada[i] = 'J01'
        if listJornada[i] == 'J2':
            listJornada[i] = 'J02'
        if listJornada[i] == 'J3':
            listJornada[i] = 'J03'
        if listJornada[i] == 'J4':
            listJornada[i] = 'J04'
        if listJornada[i] == 'J5':
            listJornada[i] = 'J05'
        if listJornada[i] == 'J6':
            listJornada[i] = 'J06'
        if listJornada[i] == 'J7':
            listJornada[i] = 'J07'
        if listJornada[i] == 'J8':
            listJornada[i] = 'J08'
        if listJornada[i] == 'J9':
            listJornada[i] = 'J09'

    dfUnderstatJornada = pd.DataFrame(list(zip(listTemporada,listEquipo, listJornada, listPPDA, listOPPDA, listDC, listODC)),
                               columns=['Temporada','Equipo','Jornada', 'PPDA', 'OPPDA', 'DC', 'ODC'])

    dfStatUndersat = pd.DataFrame(list(zip(listFinalTemporada,listFinalEquipo, listFinalPPDA, listFinalOPPDA, listFinalDC, listFinalODC)),
                                  columns=['Temporada','Equipo', 'PPDA', 'OPPDA', 'DC', 'ODC'])

    return dfUnderstatJornada, dfStatUndersat