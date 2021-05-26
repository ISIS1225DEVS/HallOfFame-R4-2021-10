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


from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import orderedmap as om
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.DataStructures import listiterator as it
import datetime

"""
@@ -38,6 +41,92 @@
"""

# Construccion de modelos


def newCatalog():
    """ Inicializa el analizador
    Crea una lista vacia para guardar todos los crimenes
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas
    Retorna el analizador inicializado.
    """
    catalog = {'eventos': None, 'energy': None, 'instrumentalness': None, 'danceability': None,
               'tempo': None, 'acousticness': None, 'hashtags': None, 'time': None}
    catalog['eventos'] = lt.newList(datastructure='ARRAY_LIST')
    catalog['energy'] = om.newMap(omaptype="RBT")
    catalog['instrumentalness'] = om.newMap(omaptype="RBT")
    catalog['danceability'] = om.newMap(omaptype="RBT")
    catalog['tempo'] = om.newMap(omaptype="RBT")
    catalog['acousticness'] = om.newMap(omaptype="RBT")
    catalog['liveness'] = om.newMap(omaptype="RBT")
    catalog['speechiness'] = om.newMap(omaptype="RBT")
    catalog['valence'] = om.newMap(omaptype="RBT")
    catalog['time'] = om.newMap(omaptype="RBT")
    catalog["energy"] = om.newMap(omaptype="RBT")
    catalog["hashtags"] = mp.newMap(maptype="PROBING", loadfactor=0.5)
    catalog['hashtagsportrack'] = mp.newMap(maptype="PROBING", loadfactor=0.5)
    catalog['tiempo'] = om.newMap(omaptype="RBT")
    return catalog


def addhashtag(catalog, hashtag, vader):
    mapa = catalog['hashtags']
    mp.put(mapa, hashtag, float(vader))


def addevent(catalog, event):
    tupla = (event['track_id'], event['user_id'], event['created_at'])
    lt.addLast(catalog['eventos'], event)
    addtomap2(catalog["tempo"], event, tupla, "tempo")
    addtomap2(catalog["energy"], event, tupla, "energy")
    addtomap2(catalog["instrumentalness"], event, tupla, "instrumentalness")
    addtomap2(catalog["danceability"], event, tupla, "danceability")
    addtomap1(catalog["acousticness"], event, tupla, "acousticness")
    addtomap1(catalog["liveness"], event, tupla, "liveness")
    addtomap1(catalog["speechiness"], event, tupla, "speechiness")
    addtomap1(catalog["valence"], event, tupla, "valence")
    addtime(catalog['time'], event)


def addtime(mapa, event):
    info = datetime.datetime.strptime(event['created_at'], '%Y-%m-%d %H:%M:%S')
    time = info.time()
    if om.contains(mapa, time):
        pareja = om.get(mapa, time)
        lista = me.getValue(pareja)
        lt.addLast(lista, entrytime(event))
    else:
        lista = lt.newList()
        lt.addLast(lista, entrytime(event))
        om.put(mapa, time, lista)


def entrytime(event):
    entry = {'tupla': (event['track_id'], event['user_id'], event['created_at']),
             'genres': genresbytempo(float(event['tempo']))}
    return entry


def addtomap1(mapa, event, tupla, caract):
    llave = event[caract]
    if om.contains(mapa, llave):
        pareja = om.get(mapa, llave)
        entry = pareja["value"]
        mp.put(entry["events"], tupla, None)
        mp.put(entry["artists"], event['artist_id'], None)

    else:
        entry = entrada1(llave, tupla, event['artist_id'])
        om.put(mapa, llave, entry)


def entrada1(llave, tupla, artist):
    entry = {"llave": llave, "events": None, "artists": None}
    entry["events"] = mp.newMap()
    mp.put(entry["events"], tupla, None)
    entry["artists"] = mp.newMap()
    mp.put(entry["artists"], artist, None)
    return entry


def addtomap2(mapa, event, tupla, caract):
    llave = float(event[caract])
    if caract == 'danceability':
        val = (event['energy'], event['danceability'])
    elif caract == 'tempo':
        val = (event['instrumentalness'], event['tempo'])
    else:
        val = None
    if om.contains(mapa, llave):
        pareja = om.get(mapa, llave)
        entry = pareja["value"]
        mp.put(entry["events"], tupla, None)
        mp.put(entry["artists"], event["artist_id"], None)
        mp.put(entry["tracks"], event['track_id'], val)

    else:
        entry = entrada(llave, tupla, event, caract, val)
        om.put(mapa, llave, entry)


def entrada(llave, tupla, event, caract, val):
    entry = {"llave": llave, "events": None, "tracks": None, "artists": None}
    entry["events"] = mp.newMap()
    mp.put(entry["events"], tupla, None)
    entry["tracks"] = mp.newMap()
    mp.put(entry["tracks"], event['track_id'], val)
    entry["artists"] = mp.newMap()
    mp.put(entry["artists"], event["artist_id"], None)

    return entry


def addpromtrack(catalog, event):
    mapa = catalog['hashtagsportrack']
    track = event['track_id']
    x = mp.get(mapa, track)
    if x != None:
        lista = me.getValue(x)
        if lt.isPresent(lista, event['hashtag']) == 0:
            lt.addLast(lista, event['hashtag'])
    else:
        lista = lt.newList(datastructure="ARRAY_LIST")
        lt.addLast(lista, event['hashtag'])
        mp.put(mapa, track, lista)


def promedio(catalog, track):
    par = mp.get(catalog['hashtagsportrack'], track)
    hts = me.getValue(par)
    suma = 0
    num = 0
    i = it.newIterator(hts)
    while it.hasNext(i):
        ht = (it.next(i)).lower()
        if mp.contains(catalog['hashtags'], ht):
            pareja = mp.get(catalog['hashtags'], ht)
            n = me.getValue(pareja)
            suma += n
            num += 1
    if num == 0:
        return None
    else:
        return num, suma/num


def mapaeventos(listadeentries):
    mapa = mp.newMap(maptype="PROBING", loadfactor=0.5)
    i = it.newIterator(listadeentries)
    while it.hasNext(i):
        entry = it.next(i)
        mapatracks = entry['tracks']
        tracks = mp.keySet(mapatracks)
        n = it.newIterator(tracks)
        while it.hasNext(n):
            track = it.next(n)
            mp.put(mapa, track, None)
    return mapa


def tracksencomun(mapa, listadeentries):
    lista = lt.newList(datastructure="ARRAY_LIST")
    x = 1
    i = it.newIterator(listadeentries)
    while it.hasNext(i):
        entry = it.next(i)
        mapatracks = entry['tracks']
        tracks = mp.keySet(mapatracks)
        n = it.newIterator(tracks)
        while it.hasNext(n):
            track = it.next(n)
            if mp.contains(mapa, track) == True:
                if x <= 5:
                    par = mp.get(mapatracks, track)
                    val = me.getValue(par)
                    valor = (track, val)
                else:
                    valor = track
                lt.addLast(lista, valor)

    return lt.size(lista), lt.subList(lista, 1, 2)


def artists(lista, x):
    m = 1
    listafinal = lt.newList(datastructure="ARRAY_LIST")
    final = mp.newMap(maptype="PROBING", loadfactor=0.5)
    i = it.newIterator(lista)

    while it.hasNext(i):
        key = it.next(i)
        mapa = key["artists"]
        artists = mp.keySet(mapa)
        a = it.newIterator(artists)
        while it.hasNext(a):
            artist = it.next(a)
            mp.put(final, artist, None)
            if x != None and m <= x:
                lt.addLast(listafinal, artist)
                m += 1

    return mp.size(final), listafinal


def numevents(lista):
    final = 0
    i = it.newIterator(lista)
    while it.hasNext(i):
        entry = it.next(i)
        num = entry['events']
        final += mp.size(num)
    return final


def genresbytempo(num):
    genres = lt.newList(datastructure="ARRAY_LIST")
    if num >= 100 and num <= 160:
        lt.addLast(genres, 'metal')
        if num >= 110 and num <= 140:
            lt.addLast(genres, 'rock')
            if num >= 120 and num <= 125:
                lt.addLast(genres, 'jazz and funk')
    if num >= 100 and num <= 130:
        lt.addLast(genres, 'pop')
    if num >= 85 and num <= 115:
        lt.addLast(genres, 'hip-hop')
    if num >= 90 and num <= 120:
        lt.addLast(genres, 'chill-out')
    if num >= 70 and num <= 110:
        lt.addLast(genres, 'down-tempo')
    if num >= 60 and num <= 90:
        lt.addLast(genres, 'reggae')
        if num >= 60 and num <= 80:
            lt.addLast(genres, 'r&b')
    return genres


def genresandtracks(lista):
    mapa = mp.newMap(maptype="PROBING", loadfactor=0.5)
    i = it.newIterator(lista)
    while it.hasNext(i):
        events = it.next(i)
        v = it.newIterator(events)
        while it.hasNext(v):
            event = it.next(v)
            tupla = event['tupla']
            genres = event['genres']
            w = it.newIterator(genres)
            while it.hasNext(w):
                genre = it.next(w)
                x = mp.get(mapa, genre)
                if x != None:
                    entry = me.getValue(x)
                    mp.put(entry['events'], tupla, None)
                else:
                    entry = entrygt(genre, tupla)
                    mp.put(mapa, genre, entry)

    return mapa


def entrygt(genre, tupla):
    entry = {'genre': genre, 'events': mp.newMap()}
    mp.put(entry['events'], tupla, None)
    return entry


def orderednums(catalog, tuplas):
    mapafinal = mp.newMap(maptype="PROBING", loadfactor=0.5)
    tracksmap = mp.newMap(maptype="PROBING", loadfactor=0.5)
    i = it.newIterator(tuplas)
    while it.hasNext(i):
        tupla = it.next(i)
        track = tupla[0]
        mp.put(tracksmap, track, None)
        prom = promedio(catalog, track)
        if prom != None:
            num = prom[0]
            par = mp.get(mapafinal, num)
            tup = (track, prom[1])
            if par != None:
                lista = me.getValue(par)
                lt.addLast(lista, tup)
            else:
                lista = lt.newList(datastructure="ARRAY_LIST")
                lt.addLast(lista, tup)
                mp.put(mapafinal, num, lista)

    return mapafinal, tracksmap


def numhts(tracks, catalog):
    mapafinal = mp.newMap(maptype="PROBING", loadfactor=0.5)
    tracksmap = mp.newMap(maptype="PROBING", loadfactor=0.5)
    d = it.newIterator(tracks)
    while it.hasNext(d):
        track = it.next(d)
        mp.put(tracksmap, track)
        x = promedio(catalog, track)
        if x != None:
            numht = x[0]
            prom = x[1]
            par = mp.get(mapafinal, numht)
            if par != None:
                lista = me.getValue(par)
                lt.addLast(lista, (track, prom))
            else:
                lista = lt.newList(datastructure="ARRAY_LIST")
                lt.addLast(lista, (track, prom))
                mp.put(mapafinal, numht, lista)
    return mapafinal, tracksmap


def tempobygenre(genre):
    if genre == 'reggae':
        menor = 60.0
        mayor = 90.0
    elif genre == 'down-tempo':
        menor = 70.0
        mayor = 100.0
    elif genre == 'chill-out':
        menor = 90.0
        mayor = 120.0
    elif genre == 'hip-hop':
        menor = 85.0
        mayor = 115.0
    elif genre == 'jazz and funk':
        menor = 120.0
        mayor = 125.0
    elif genre == 'pop':
        menor = 100.0
        mayor = 130.0
    elif genre == 'r&b':
        menor = 60.0
        mayor = 80.0
    elif genre == 'rock':
        menor = 110.0
        mayor = 140.0
    elif genre == 'metal':
        menor = 100.0
        mayor = 160.0
    return menor, mayor


"""# Funciones para agregar informacion al catalogo
# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento"""
