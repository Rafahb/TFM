#Librerias
import scrapingPlayers as players
import scrapingMatches as matches
import scrapingUnderstat as understat
import scrapingStats as generalStats
import warnings
warnings.filterwarnings('ignore')


if __name__ == "__main__":
    #Inicialmente obtenemos los datos de interes de Understat
    dfUnderstatJornada, dfStatUndersat = understat.getDataFrameUnderstat()

    #Obtenemos los datos generales de la liga Santandes
    generalStats.scrapingGeneral(dfStatUndersat)

    #Obtenemos los datos de los jugadores
    players.getDataFramePlayers()

    #Obtenemos los datos de los partidos
    matches.getDataFrameMatches(dfUnderstatJornada)

    print("---COMPLETADO---")