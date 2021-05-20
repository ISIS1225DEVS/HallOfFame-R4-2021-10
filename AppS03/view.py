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
from DISClib.DataStructures import mapentry as me
import random
import datetime as dt
assert cf

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Crear catalogo")
    print("2- Cargar información en el catálogo")
    print("3- Caracterizar las reproducciones")
    print("4- Encontrar música para festejar")
    print("5- Encontrar música para estudiar")
    print("6- Estudiar los géneros musicales")
    print("7- Indicar el género musical más escuchado en el tiempo")
    print("0- Salir")
    print("*******************************************")


def printLoadInfo(answer):
    catalog = answer[0]
    print("Total eventos de escucha:", controller.listSize(catalog['events']))
    print("Total eventos de artistas unicos:", answer[1])
    print("Total eventos de tracks unicos:", answer[2], '\n')

    sub_list1 = lt.subList(catalog['events'], 1, 5)
    sub_list2 = lt.subList(catalog['events'], lt.size(catalog['events']) - 6, 5)

    n = 1
    for item in lt.iterator(sub_list1):
        print('Video', n, ':', item, '\n')
        n += 1
    for item in lt.iterator(sub_list2): 
        print('Video', n, ':', item, '\n')
        n += 1


def printTracks(list_of_tracks): 
    print('\n--- Unique track_id ---')
    statement = 'Track {}: {} with energy of {} and danceability of {}'
    for n in range(0, 5): 
        random_pos = random.randint(1, controller.listSize(list_of_tracks))
        rand_item = lt.getElement(list_of_tracks, random_pos)

        print(statement.format(n+1, rand_item['track_id'], rand_item['energy'], rand_item['danceability']))


def printTracks2(list_of_tracks): 
    print('\n--- Unique track_id ---')
    statement = 'Track {}: {} with instrumentalness of {} and tempo of {}'
    for n in range(0, 5): 
        random_pos = random.randint(1, controller.listSize(list_of_tracks))
        rand_item = lt.getElement(list_of_tracks, random_pos)

        print(statement.format(n+1, rand_item['track_id'], rand_item['instrumentalness'], rand_item['tempo']))


# File names
contextcontentfile = '/subsamples-small/context_content_features-small.csv'
sentimentvaluesfile = '/subsamples-small/sentiment_values.csv'
usertrackhashtagtimestampsfile = '/subsamples-small/user_track_hashtag_timestamp-small.csv'


def print_tracks(tracks_sort):
    n = 1
    rta = "TOP {} track: {} with {} hashtags and VADER = {}"
    for track in lt.iterator(tracks_sort): 
        print(rta.format(n, track["track"], track["num_hashtags"], track["average"]))
        n += 1


def print_genre_reps(reps_sort):
    n = 1
    rta = "TOP {}: {} with {} reps"
    for genre in lt.iterator(reps_sort):
        print(rta.format(n, genre["genre"], genre["reps"]))
        n += 1
    top = lt.firstElement(reps_sort)
    print("\nThe TOP GENRE is {} with {} reproductions...".format(top["genre"], top["reps"]))


catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("\nInicializando....")
        catalog = controller.init()

    elif int(inputs[0]) == 2:
        print("Cargando información de los archivos ....")
        answer = controller.loadData(catalog, contextcontentfile, sentimentvaluesfile, usertrackhashtagtimestampsfile)
        printLoadInfo(answer)       

    elif int(inputs[0]) == 3:
        category = input('Qué categoria de contenido desea consultar: ')
        category_tree = controller.getCateory(catalog, category)

        if category_tree is not None:
            min_range = float(input('Valor minimo (debe ser entre 0.0 y 1.0): '))
            max_range = float(input('Valor maximo (debe ser entre 0.0 y 1.0): '))
            
            if (min_range - max_range > 0.0) or min_range < 0.0 or max_range > 1.0: 
                print('Rangos inválidos, inténtelo de nuevo')
            else: 
                answer = controller.categoryCaracterization(catalog, category, min_range, max_range)

                print('\n\n++++++ Req No. 1 results... ++++++')
                statement1 = "{} is between {} and {}"
                statement2 = "Total of reproduction: {} \t Total unique artists {}"
                # print("Para arbol de ", category, "\nElementos:", tree[0], "\nAltura:", tree[1])
                print(statement1.format(category, min_range, max_range))
                print(statement2.format(answer[0], answer[1]))
        else: 
            print('Categoría de contenido no válida')
    elif int(inputs[0]) == 4:
        min_energy = float(input('Valor mínimo para Energy (debe ser entre 0.0 y 1.0): '))
        max_energy = float(input('Valor máximo para Energy (debe ser entre 0.0 y 1.0): '))
        min_danceability = float(input('Valor mínimo para Danceability (debe ser entre 0.0 y 1.0): '))
        max_danceability = float(input('Valor mínimo para Danceability (debe ser entre 0.0 y 1.0): '))

        if (min_energy - max_energy > 0.0) or min_energy < 0.0 or max_energy > 1.0 or (min_danceability - max_danceability > 0.0) or min_danceability < 0.0 or max_danceability > 1:
            print('Rangos inválidos, inténtelo de nuevo')
        else:
            answer = controller.partyMusic(catalog, min_energy, max_energy, min_danceability, max_danceability)

            print('\n \n++++++ Req No. 2 results... ++++++')
            print('Energy is between', min_energy, 'and', max_energy)
            print('Danceability is between', min_danceability, 'and', max_danceability)
            print('Total of unique tracks in events:', answer[1])
            printTracks(answer[0])

    elif int(inputs[0]) == 5:
        min_instrumentalness = float(input('Valor mínimo para Instrumentalness (debe ser entre 0.0 y 1.0): '))
        max_instrumentalness = float(input('Valor máximo para Instrumentalness (debe ser entre 0.0 y 1.0): '))
        min_tempo = float(input('Valor mínimo para  Tempo: '))
        max_tempo = float(input('Valor mínimo para  Tempo: '))

        if (min_instrumentalness - max_instrumentalness > 0.0) or min_instrumentalness < 0.0 or max_instrumentalness > 1.0 or (min_tempo - max_tempo > 0.0) or min_tempo < 0.0:
            print('Rangos inválidos, inténtelo de nuevo')
        else:
            answer = controller.relaxingMusic(catalog, min_instrumentalness, max_instrumentalness, min_tempo, max_tempo)

            print('\n \n++++++ Req No. 3 results... ++++++')
            print('Tempo is between', min_tempo, 'and', max_tempo)
            print('Instrumentalness is between', min_instrumentalness, 'and', max_instrumentalness)
            print('Total of unique tracks in events:', answer[1])
            printTracks2(answer[0])
        
    elif int(inputs[0]) == 6:
        genres = input("Genero(s) a buscar (separelos con un espacio): ").split()

        all_valid = True
        for genre in genres: 
            verf_genre = controller.getGenre(catalog, genre)
            
            if verf_genre is None:
                new_genre = int(input('Desea crear un nuevo género para ' + genre + '?\n 1 - Si \n 2 - No \n>'))
                if new_genre == 1:
                    min_tempo = float(input('Tempo minimo del género: '))
                    max_tempo = float(input('Tempo máximo del género: '))
                    controller.newGenre(catalog, genre, min_tempo, max_tempo)
                else:
                    print('El género', genre, 'no es válido, intentelo de nuevo.')
                    all_valid = False

        if all_valid:
            answer = controller.genreStudy(catalog, genres)

            print('\n \n++++++ Req No. 4 results... ++++++')
            totalReps = controller.getReps(answer)
            print('Total of reproductions: ', totalReps)

            statement1 = "======== {} ========"
            statement2 = "For {} the tempo is between {} and {} BPM"
            statememnt3 = "{} reproductions: {} with {} different artists"
            statememnt4 = "----- Some artists for {} -----"
            statememnt5 = "Artist {}: {}"

            for genre in genres:
                print('\n', statement1.format(genre))
                ranges = me.getValue(mp.get(catalog['genre_dictionary'], genre))
                print(statement2.format(genre, ranges['min'], ranges['max']))
                reps_tot = controller.listSize(me.getValue(mp.get(answer, genre))['list'])
                arts_tot = controller.mapSize(me.getValue(mp.get(answer, genre))['unique_artists'])
                print(statememnt3.format(genre, reps_tot, arts_tot))
                print(statememnt4.format(genre))
                for n in range(1, 11):
                    element = lt.getElement(me.getValue(mp.get(answer, genre))['list'], n)
                    print(statememnt5.format(n, element['artist_id']))
                
    elif int(inputs[0]) == 7:
        min_time = (input('El valor mínimo de la hora del día: '))
        max_time = (input('El valor máximo de la hora del día: '))

        min_time = dt.datetime.strptime(min_time, ("%H:%M:%S"))
        max_time = dt.datetime.strptime(max_time, ("%H:%M:%S"))
        
        if min_time < max_time:
            answer = controller.genreMostListened(catalog, min_time.time(), max_time.time())
            total_reps = answer[0]
            top_genre = answer[1]
            reps_sort = answer[2]
            tracks_sort = answer[3][0]
            total_tracks = answer[3][1]
            print('\n \n++++++Req No. 5 results... ++++++')
            print("There is a total of {} reproductions between {} and {}".format(total_reps, min_time.time(), max_time.time()))
            print("====================== GENRES SORTED REPRODUCTIONS ======================")
            print_genre_reps(reps_sort)
            print("\n========================== {} SENTIMENT ANALYSIS =========================".format(top_genre))
            print("{} has {} unique tracks...".format(top_genre, total_tracks))
            print("The first TOP 10 tracks are..\n")
            print_tracks(tracks_sort)
        else: 
            print("\n Rangos de tiempo inválidos")
    else:
        sys.exit(0)
sys.exit(0)
