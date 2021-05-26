"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import mergesort as mer
from DISClib.ADT import orderedmap as om
import random
import time

assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newCatalog ():
    catalog = {'songs' : None,
                'hashtags': None,
                'artists': None,
                'numevent': 0,
                'tracksong': None,
                'trackhashtag': None,
                'issong': None,
                'genre': None}
    catalog['songs'] = mp.newMap(11,
                                maptype='PROBING',
                                loadfactor=0.5,
                                comparefunction=cmpByPista)
    catalog['hashtags'] = mp.newMap(6000,
                                maptype='PROBING',
                                loadfactor=0.5,
                                comparefunction=cmpByPista)
    catalog['trackhashtag'] = mp.newMap(1000000,
                                maptype='PROBING',
                                loadfactor=0.5,
                                comparefunction=cmpByPista)
    catalog['artists'] = mp.newMap(1000000,
                                maptype='PROBING',
                                loadfactor=0.5,
                                comparefunction=cmpByPista)
    catalog['tracksong'] = mp.newMap(1000000,
                                maptype='PROBING',
                                loadfactor=0.5,
                                comparefunction=cmpByPista)

    catalog['issong'] = mp.newMap(11,
                                maptype='PROBING',
                                loadfactor=0.5,
                                comparefunction=cmpByPista)
    catalog['genre'] = mp.newMap(11,
                                maptype='PROBING',
                                loadfactor=0.5,
                                comparefunction=cmpByPista)
                                

    return catalog
# Funciones para agregar informacion al catalogo
def addSong (catalog):
    songs = catalog['songs']
    charact = ["instrumentalness","danceability","tempo","energy","acousticness","liveness","speechiness","valence","created_at"]
    for i in charact:
        dataentry = mp.get(songs, i)
        map = me.getValue(dataentry)
        dataentry2 = mp.get(catalog['issong'], i)
        map2 = me.getValue(dataentry2)
        for j in lt.iterator(mp.keySet(map2)):
            if j:
                subentry = mp.get(map2, j)
                newentry = me.getValue(subentry)
                om.put(map, j, newentry)


def addArtist (map, song):
    artist = song['artist_id']
    existpista = mp.contains(map, artist)
    if existpista is False:
        mp.put(map, artist, song)

def addPista (map, song):
    artist = song['track_id']
    existpista = mp.contains(map, artist)
    if existpista is False:
        mp.put(map, artist, song)

def addTrackHashtag (map, song):
    pista = song['track_id']
    existpista = mp.contains(map, pista)
    if existpista:
        entry = mp.get(map, pista)
        ltpista = me.getValue(entry)
    else:
        ltpista = lt.newList('ARRAY_LIST')
        mp.put(map, pista, ltpista)
    if lt.isEmpty(ltpista):
        lt.addLast(ltpista, song['hashtag'].lower())
    else:
        exist = lt.isPresent(ltpista, song['hashtag'].lower())
        if exist == 0:
            lt.addLast(ltpista, song['hashtag'].lower())
        
def newAddSong (catalog):
    catalog['numevent'] += 1


def addGenre (map, genre):
    existgenre = mp.contains(map, genre[0])
    if existgenre is False:
        mp.put(map, genre[0], (genre[1], genre[2]))


def addHashtag (map, dicc):
    hashtag = dicc['hashtag'].lower()
    existpista = mp.contains(map, hashtag)
    if existpista is False:
        mp.put(map, hashtag, dicc)

def addTrack (map, song):
    pista = song['track_id']
    existpista = mp.contains(map, pista)
    if existpista:
        entry = mp.get(map, pista)
        ltpista = me.getValue(entry)
    else:
        ltpista = lt.newList('ARRAY_LIST')
        mp.put(map, pista, ltpista)
    lt.addLast(ltpista, song)

def addHashtagProm(catalog, lstevent):
    for song in lt.iterator(lstevent):
        entry = mp.get(catalog['trackhashtag'],song['track_id'])
        dataentry = me.getValue(entry)
        song['hashtag'] = lt.newList('ARRAY_LIST')
        num = 0
        prom = 0
        for hashtag in lt.iterator(dataentry):
            exist = mp.contains(catalog['hashtags'], hashtag)
            if exist:
                entry = mp.get(catalog['hashtags'], hashtag)
                value = me.getValue(entry)['vader_avg']
                if value != '':
                    lt.addLast(song['hashtag'], hashtag)
                    num += 1
                    prom += float(value)
        if num > 0:
            song['hashtag_avg'] = prom/num

# Funciones para creacion de datos
def newSong (song, contexsong):
    finalsong = None
    if song['user_id'] == contexsong['user_id'] and song['track_id'] == contexsong['track_id'] and song['created_at'] == contexsong['created_at']:
        contexsong['hashtag'] = song['hashtag'].lower()
        finalsong = contexsong
    return finalsong

def createCharact (catalog):
    map = catalog['songs']
    charact = ["instrumentalness","danceability","tempo","energy","acousticness","liveness","speechiness","valence","created_at"]
    for i in charact:
        entry = om.newMap(omaptype='RBT',comparefunction=cmpCharact)
        mp.put(map, i, entry)


def createCharactSong (catalog):
    map = catalog['issong']
    charact =  ["instrumentalness","danceability","tempo","energy","acousticness","liveness","speechiness","valence","created_at"]
    for i in charact:
        entry = mp.newMap(100000,
                            maptype='PROBING',
                            loadfactor=0.5,
                            comparefunction=cmpByPista)
        mp.put(map, i, entry)

def songByUserId(catalog, song):
    map = catalog['tracksong']
    pista = song['track_id']
    song['hashtag'] = lt.newList('ARRAY_LIST', cmpfunction=cmpCharact)
    issong = None
    exist = mp.contains(map, pista)
    if exist:
        entry = mp.get(map, pista)
        ltpista = me.getValue(entry)
        ejecutar = True
        i = 1
        while i <= lt.size(ltpista) and ejecutar == True:
            song1 = lt.getElement(ltpista, i)
            issong = newSong(song1, song)
            if issong is not None:
                lt.deleteElement(ltpista, i)
                ejecutar = False
            i += 1
    return issong

def addSongbyCharact (catalog, song):
    charact =  ["instrumentalness","danceability","tempo","energy","acousticness","liveness","speechiness","valence","created_at"]
    for i in charact:
        entry = mp.get(catalog['issong'], i)
        map = me.getValue(entry)
        if i == "created_at":
            pista = song[i][11:]
        else:
            pista = float(song[i])
        existpista = mp.contains(map, pista)
        if existpista:
            entry = mp.get(map, pista)
            datapista = me.getValue(entry)
        else:
            datapista = lt.newList('ARRAY_LIST')
            mp.put(map, pista, datapista)
        lt.addLast(datapista, song)

# Funciones de consulta
def reprodByCharactRange (catalog, characteristics, range ) :
    songs = catalog['songs']
    dataentry = mp.get(songs, characteristics)
    map = me.getValue(dataentry)
    lstpista = om.values(map, range[0], range[1])
    reprod = 0
    for value in lt.iterator(lstpista):
        reprod += lt.size(value)
    return (lstpista,reprod)

def reprodByCharactRangeLst (lstevent, characteristics, range ) :
    lstpista = lt.newList('ARRAY_LIST')
    for value in lt.iterator(lstevent):
        for pista in lt.iterator(value):
            if float(pista[characteristics]) >= range[0] and float(pista[characteristics]) <= range[1]:
                lt.addLast(lstpista, pista)
    return (lstpista, lt.size(lstpista))

def reprodGenreByTime (catalog, lstevent):
    lstgenre = lt.newList('ARRAY_LIS')
    Genre = mp.keySet(catalog['genre'])
    for genre in lt.iterator(Genre):
        if genre is not None:
            range = getGenreRange(catalog, genre)
            reprod = reprodByCharactRangeLst(lstevent, 'tempo', range)
            lt.addLast(lstgenre, (genre, reprod))
    lstgenresort = mergeSortVideos(lstgenre, lt.size(lstgenre), 'reprod')[0]
    lstreprod = lt.getElement(lstgenresort, 1)[1][0]
    

    return (lstgenresort, lstreprod)

def unicTrackorArtist (catalog, lstevent, id):
    map = mp.newMap(2000,
                    maptype='PROBING',
                    loadfactor=0.5,
                    comparefunction=cmpByPista)
    if lstevent['type'] == 'SINGLE_LINKED':
        for value in lt.iterator(lstevent):
            for song in lt.iterator(value):
                if id == 'track_id':
                    addPista(map, song)
                elif id == 'artist_id':
                    addArtist(map,song)
    else:
        for song in lt.iterator(lstevent):
            if id == 'track_id':
                    addPista(map, song)
            elif id == 'artist_id':
                addArtist(map,song)
    lstvalues = mp.valueSet(map)

    return (lstvalues, mp.size(map))

def selectResults (lstvalues, num, characteristics):
    lstresults = lt.newList('ARRAY_LIST')
    pos = range(1,lt.size(lstvalues))
    pos = random.sample(pos, num)
    i = 1
    if type(characteristics) == tuple :
        for num in pos:
            song = lt.getElement(lstvalues, num)
            element = 'Track '+ str(i)+ ': '+ song['track_id']+ ' with '+ characteristics[0]+ ' of '+ song[characteristics[0]]+ ' and '+ characteristics[1]+ ' of '+ song[characteristics[1]]
            lt.addLast(lstresults, element)
            i += 1
    elif characteristics:
        while i <= 10:
            song = lt.getElement(lstvalues, i)
            element = 'Top '+ str(i)+ ' track'+ ': '+ song['track_id']+ ' with '+ str(lt.size(song['hashtag']))+ ' hashtags and VADER = ' + str(song['hashtag_avg'])
            lt.addLast(lstresults, element)
            i += 1

    else:
        for num in pos:
            song = lt.getElement(lstvalues, num)
            element = 'Artist '+ str(i)+ ': '+ song['artist_id']
            lt.addLast(lstresults, element)
            i += 1
    
    return lstresults



def getGenreRange (catalog, genre):
    entry = mp.get(catalog['genre'], genre)
    min = me.getValue(entry)[0]
    max = me.getValue(entry)[1]

    return (min, max)

def printEvent (song):
    characteristics = ["instrumentalness","acousticness","liveness","speechiness","energy","danceability","valence"]
    element = 'Track '+ song['track_id']+ ' Artist '+ song['artist_id']+ ' with '+ characteristics[0]+ ' of '+ song[characteristics[0]]+ ', '+ characteristics[1]+ ' of '+ song[characteristics[1]]+ ', '+ characteristics[2]+ ' of '+ song[characteristics[2]]+ ', '+ characteristics[3]+ ' of '+ song[characteristics[3]]+', '+ characteristics[4]+ ' of '+ song[characteristics[4]]+ ', '+ characteristics[5]+ ' of '+ song[characteristics[5]]+ ', '+ characteristics[6]+ ' of '+ song[characteristics[6]]+ ' and created date : '+ song['created_at']
    return element

# Funciones utilizadas para comparar elementos dentro de una lista
def cmpByPista(key, element):
        tagentry = me.getKey(element)
        if (str(key) == str(tagentry)):
                return 0
        elif (str(key) != str(tagentry)):
                return 1
        else:
                return 0
def cmpCharact(key1, key2):
    if (key1 == key2):
        return 0
    elif (key1 > key2):
        return 1
    else:
        return -1

def cmpGenreByReprod(tupla1, tupla2):
    return (float(tupla1[1][1]) > float(tupla2[1][1]))

def cmpByHashtag(song1, song2):
    return (float(lt.size(song1['hashtag'])) > float(lt.size(song2['hashtag'])))


# Funciones de ordenamiento

def mergeSortVideos(lstevent, size, parametro):
    sub_list = lt.subList(lstevent, 1, size)
    sub_list = sub_list.copy()
    if parametro == 'reprod':
        start_time = time.process_time()
        mergeSortList = mer.sort(sub_list, cmpGenreByReprod)
        stop_time = time.process_time()
    elif parametro == 'hashtag':
        start_time = time.process_time()
        mergeSortList = mer.sort(sub_list, cmpByHashtag)
        stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000

    return (mergeSortList, elapsed_time_mseg)