"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me

assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Consultar reproducciones basadas en una carectarestica de contenido para un rango determinado")
    print("3- Consultar musica para festejar: ")
    print("4- Consultar musica para estudiar: ")
    print("5- Consultar numero de canciones por genero prederteminado o genero al criterio del usuario: ")
    print("6- Consultar género musical más escuchado en el tiempo:")


def initCatalog():
    return controller.newCatalog()
    

def loadData(catalog):
    return controller.loadData(catalog)

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalog = initCatalog()
        result = controller.loadData(catalog)
        print('Eventos cargados: ' , catalog['numevent'], '\n'
            'Numero Artistas: ' ,mp.size(catalog['artists']), '\n'
            'Numero Pistas: ' ,mp.size(catalog['trackhashtag']))
        pos = 1
        print(lt.size(result[0]))
        print('---5 Primeros eventos cargados---\n')
        for event in lt.iterator(lt.subList(result[0], 1, 5)):
            print('Event ', pos, ' : ' + event)
            pos += 1
        pos = 63229
        print('\n---5 Ultimos eventos cargados---\n')
        for event in lt.iterator(lt.subList(result[0], 6, 5)):
            print('Event ', pos, ' : ' + event)
            pos += 1
        print("\nTiempo [ms]: ", f"{result[1][0]:.3f}", "  ||  ",  "Memoria [kB]: ", f"{result[1][1]:.3f}")
        
    elif int(inputs[0]) == 2:
        try:
            inputc = input('Ingrese la caracteristica: ')
            inputm = float(input('Ingrese el valor minimo: '))
            inputM = float(input('Ingrese el valor maximo: '))
            result = controller.reprodByCharactRange(catalog, inputc, (inputm, inputM))
            print ('++++++ Req No. 1 results... ++++++','\n'+
                inputc.capitalize(), ' is between ', inputm, ' and ', inputM, '\n'
                'Total of reproduction: ', result[0][0], ' Total of unique artists: ', result[0][1])
            print("Tiempo [ms]: ", f"{result[1][0]:.3f}", "  ||  ",  "Memoria [kB]: ", f"{result[1][1]:.3f}")
        except Exception:
            print ('Ha surgido un error, asegurese de digitar los datos correctamente y vuelva a intentarlo.')
        
        
    elif int(inputs[0]) == 3:
        try:
            inputm1 = float(input('Ingrese el valor minimo para Energy: '))
            inputM1 = float(input('Ingrese el valor maximo para Energy: '))
            inputm2 = float(input('Ingrese el valor minimo para Danceability: '))
            inputM2 = float(input('Ingrese el valor maximo para Danceability: '))
            result = controller.songByTwoCharactRange(catalog, ('energy','danceability'), (inputm1, inputM1), (inputm2, inputM2))
            print ('++++++ Req No. 2 results... ++++++','\n'
                'Energy is between ', inputm1, ' and ', inputM1, '\n'
                'Danceability is between ', inputm2, ' and ', inputM2, '\n'
                'Total of unique tracks in events: ', result[0][0], '\n'+'\n',
                '--- Unique track_id ---')
            for value in lt.iterator(result[0][1]):
                print (value)
            print("Tiempo [ms]: ", f"{result[1][0]:.3f}", "  ||  ",  "Memoria [kB]: ", f"{result[1][1]:.3f}")
        except Exception:
            print ('Ha surgido un error, asegurese de digitar los datos correctamente y vuelva a intentarlo.')
    elif int(inputs[0]) == 4:
        try:
            inputm1 = float(input('Ingrese el valor minimo para Instrumentalness: '))
            inputM1 = float(input('Ingrese el valor maximo para Instrumentalness: '))
            inputm2 = float(input('Ingrese el valor minimo para Tempo: '))
            inputM2 = float(input('Ingrese el valor maximo para Tempo: '))
            result = controller.songByTwoCharactRange(catalog, ('instrumentalness','tempo'), (inputm1, inputM1), (inputm2, inputM2))
            print ('++++++ Req No. 3 results... ++++++\n'
                'Instrumentalness is between ', inputm1, ' and ', inputM1, '\n'
                'Tempo is between ', inputm2, ' and ', inputM2, '\n'
                'Total of unique tacks in events: ', result[0][0], '\n'+'\n',
                '--- Unique track_id ---')
            for value in lt.iterator(result[0][1]):
                print (value)
            print("Tiempo [ms]: ", f"{result[1][0]:.3f}", "  ||  ",  "Memoria [kB]: ", f"{result[1][1]:.3f}")
        except Exception:
            print ('Ha surgido un error, asegurese de digitar los datos correctamente y vuelva a intentarlo.')
    elif int(inputs[0]) == 5:
        try:
            print ('Lista de generos:\n- Reggae\n- Dowm-tempo\n- Chill-out\n- Hip-hop\n- Jazz and Funk\n- Pop\n'
                    '- RGB\n- Rock\n- Metal')
            prd = input('De la anterior lista ingresa los generos a consultar separados por una coma: ')
            add = input('¿Desea agregar un nuevo genero a su criterio?, responda con ''SI'' o ''NO'':')
            if add.upper() == 'SI':
                name = input('Ingrese el nombre del nuevo genero: ')
                inputm = float(input('Ingrese el valor minimo para Tempo: '))
                inputM = float(input('Ingrese el valor maximo para Tempo: '))
                controller.addGenre(catalog, [name, inputm, inputM])
                prd += ','+ name
            lstgenre = prd.split(',')
            reprod = controller.totalReprodByGenre(catalog, lstgenre)
            print('++++++ Req No. 4 results... ++++++\n'
                'Total of reproductions: ', reprod[0])
            result = controller.consultByGenre(catalog, lstgenre)
            answer = (reprod[1][0]+result[0],reprod[1][1]+result[1])
            print("Tiempo [ms]: ", f"{answer[0]:.3f}", "  ||  ",  "Memoria [kB]: ", f"{answer[1]:.3f}")
        except Exception:
            print ('Ha surgido un error, asegurese de digitar los datos correctamente y vuelva a intentarlo.')
    elif int(inputs[0]) == 6:
        try:
            inputm = (input('Ingrese el valor minimo para Created: '))
            inputM = (input('Ingrese el valor maximo para Created: '))
            result = controller.reprodGenreByTime(catalog, ('created_at'), (inputm, inputM))
            reprod = 0
            for tup in lt.iterator(result[0][0][0]):
                reprod += tup[1][1]
            print ('++++++ Req No. 5 results... ++++++\n'
                'There is a total of ', reprod, ' reproductions between ', inputm, ' and ', inputM, '\n'
                '====================== GENRES SORTED REPRODUCTIONS ====================== \n')
            rank = 1
            for tup in lt.iterator(result[0][0][0]):
                    print('TOP ', rank, ' : '+ tup[0]+ ' with ', tup[1][1], ' reps')
                    rank += 1
            print ('The TOP GENRE is Metal with ', lt.getElement(result[0][0][0],1)[1][1], ' reproductions...\n'
                '\n========================== Metal SENTIMENT ANALYSIS =========================\n'
                'Metal has ', result[0][1], ' unique tracks...\nThe first TOP 10 tracks are...')
            pos = 1
            for song in lt.iterator(result[0][0][1]):
                if pos <= 10:
                    print(song)
                else:
                    break
                pos += 1
            print("Tiempo [ms]: ", f"{result[1][0]:.3f}", "  ||  ",  "Memoria [kB]: ", f"{result[1][1]:.3f}")
        except Exception:
            print ('Ha surgido un error, asegurese de digitar los datos correctamente y vuelva a intentarlo.')
    else:
        sys.exit(0)
sys.exit(0)
