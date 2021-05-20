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
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
import datetime
from DISClib.Algorithms.Sorting import mergesort as mer
import random
assert cf


"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# ==============================
# Construcción de modelos
# ==============================


def newCatalog():
    catalog = {'sentimentvalues': None, 'events': None, 'content_cateogires':None, 'user_created_at': None}
    catalog['events'] = lt.newList('SINGLE_LINKED', cmpEvents)
    catalog['sentimentvalues'] = mp.newMap(numelements=100000, maptype='PROBING', loadfactor=0.5, comparefunction=cmpHashtags)
    catalog['content_cateogries'] = mp.newMap(numelements=17, maptype='PROBING', loadfactor=0.5, comparefunction=cmpCategories)
    catalog['user_created_at'] = om.newMap(omaptype='RBT',
                                      comparefunction=cmpDates)
    catalog['unique_artists'] = mp.newMap(numelements=50000, maptype='CHAINING', loadfactor=0.5,  comparefunction = cmpCategories)
    catalog['unique_tracks'] = mp.newMap(numelements=50000, maptype='CHAINING', loadfactor=0.5, comparefunction = cmpCategories)
    catalog['genre_dictionary'] = mp.newMap(numelements=100, maptype='PROBING', loadfactor=0.5,  comparefunction=cmpCategories)
    catalog['content_created_at'] = om.newMap(omaptype='RBT',
                                      comparefunction=cmpDates)
                                      # TODO: compare times
    catalog['tracks_hashtag'] = mp.newMap(numelements=100000, maptype='PROBING', loadfactor=0.5,  comparefunction=cmpCategories)
    catalog['content_time'] = om.newMap(omaptype='RBT', comparefunction=cmpTimes)
    catalog['user_times'] = om.newMap(omaptype='RBT', comparefunction=cmpTimes)
    return catalog


# =========================================
# Funciones para agregar info al catalogo
# ==========================================

def addEvent(catalog, event):
    """
    Carga info del archivo content_context a diferentes estructuras
    """
    lt.addLast(catalog['events'], event)
    mp.put(catalog['unique_artists'], event['artist_id'], event)
    mp.put(catalog['unique_tracks'], event['track_id'], event)
    addCategory(catalog, event)
    genreDictionary(catalog)
    contentCreatedAt(catalog, event)
    content_time(catalog, event)
    return catalog


def addCategory(catalog, event): 
    """Arbol por categorias"""
    category_map = catalog['content_cateogries']
    keys = mp.keySet(category_map)
    if lt.size(keys) <= 0: 
        fillHashMap(category_map)
    keys = mp.keySet(category_map)
    for item in lt.iterator(keys): 
        valor_item = float(event[item])

        cate_tree = me.getValue(mp.get(category_map, item))
        if cate_tree is None:
            cate_tree = createCategTree()
            mp.put(category_map, item, cate_tree)

        if om.size(cate_tree) == 0:
            tree_list = lt.newList(datastructure="ARRAY_LIST")
            lt.addLast(tree_list, event)
            om.put(cate_tree, valor_item, tree_list)
        else:
            tree_val = om.get(cate_tree, valor_item)
            if tree_val is None:
                tree_list = lt.newList(datastructure="ARRAY_LIST")
                om.put(cate_tree, valor_item, tree_list)
            else:
                tree_list = me.getValue(tree_val)
            
            lt.addLast(tree_list, event)
    return catalog
            

def fillHashMap(map_cate):
    """HashMap de categorias"""
    event_cols = lt.newList(datastructure='ARRAY_LIST')
    lt.addLast(event_cols, "instrumentalness")
    lt.addLast(event_cols, "liveness")
    lt.addLast(event_cols, "speechiness")
    lt.addLast(event_cols, "danceability")
    lt.addLast(event_cols, "valence")
    lt.addLast(event_cols, "tempo")
    lt.addLast(event_cols, "acousticness")
    lt.addLast(event_cols, "energy")

    # "instrumentalness","liveness","speechiness","danceability","valence","loudness","tempo","acousticness","energy"

    for event in lt.iterator(event_cols): 
        mp.put(map_cate, event,  None)

    return map_cate


def createCategTree(): 
    tree = om.newMap(omaptype='RBT', comparefunction=cmpCategories2)
    return tree


def contentCreatedAt(catalog, event): 
    """Arbol fecha completa"""
    mapDates = catalog["content_created_at"] 
    eventDate = event["created_at"]
    eventDate = datetime.datetime.strptime(eventDate, '%Y-%m-%d %H:%M:%S')
    
    entry = om.get(mapDates, eventDate)
    if entry is None: 
        datentry = lt.newList(datastructure="ARRAY_LIST")
        om.put(mapDates, eventDate, datentry) 
    else:
        datentry = me.getValue(entry)
    
    lt.addLast(datentry, event)
    return catalog


def content_time(catalog, event): 
    """Arbol solo tiempos"""
    mapDates = catalog["content_time"] 
    eventDate = event["created_at"]
    eventDate = datetime.datetime.strptime(eventDate, '%Y-%m-%d %H:%M:%S')
    eventTime = eventDate.time()
    entry = om.get(mapDates, eventTime)
    if entry is None: 
        datentry = lt.newList(datastructure="ARRAY_LIST")
        om.put(mapDates, eventTime, datentry) 
        
    entry = om.get(mapDates, eventTime)  
    datentry = me.getValue(entry)
    
    lt.addLast(datentry, event)
    om.put(mapDates, eventTime, datentry)
    return catalog


def user_time(catalog, event): 
    """Arbol solo tiempos"""
    mapDates = catalog["user_times"] 
    eventDate = event["created_at"]
    eventDate = datetime.datetime.strptime(eventDate, '%Y-%m-%d %H:%M:%S')
    eventTime = eventDate.time()
    entry = om.get(mapDates, eventTime)
    if entry is None: 
        datentry = lt.newList(datastructure="ARRAY_LIST")
        om.put(mapDates, eventTime, datentry) 
    else:
        datentry = me.getValue(entry)
    
    lt.addLast(datentry, event)
    om.put(mapDates, eventTime, datentry)
    return catalog


def addUserInfo(catalog, userInfo): 
    """Arbol fecha completa"""
    mapDates = catalog["user_created_at"] 
    eventDate = userInfo["created_at"]
    eventDate = datetime.datetime.strptime(eventDate, '%Y-%m-%d %H:%M:%S')
    entry = om.get(mapDates, eventDate)
    if entry is None:
        datentry = lt.newList(datastructure="ARRAY_LIST")
        om.put(mapDates, eventDate, datentry) 
    else:
        datentry = me.getValue(entry)
    
    lt.addLast(datentry, userInfo)
    user_time(catalog, userInfo)
    return catalog


def addHashtag(catalog, event): 
    hashtag = event['hashtag'].lower()
    mp.put(catalog["sentimentvalues"], hashtag,  event['vader_avg'])
    return catalog


def genreDictionary(catalog):
    g_dict = catalog['genre_dictionary']
    mp.put(g_dict, 'Reggae', {'min': 60.0, 'max': 90.0})
    mp.put(g_dict, 'Down-tempo', {'min': 70.0, 'max': 100.0})
    mp.put(g_dict, 'Chill-out', {'min': 90.0, 'max': 120.0})
    mp.put(g_dict, 'Hip-hop', {'min': 85.0, 'max': 115.0})
    mp.put(g_dict, 'Jazz and Funk', {'min': 120.0, 'max': 125.0})
    mp.put(g_dict, 'Pop', {'min': 100.0, 'max': 130.0})
    mp.put(g_dict, 'R&B', {'min': 60.0, 'max': 80.0})
    mp.put(g_dict, 'Rock', {'min': 110.0, 'max': 140.0})
    mp.put(g_dict, 'Metal', {'min': 100.0, 'max': 160.0})
    return catalog


# ==============================
# Funciones de Consulta
# ==============================


# ==============================
# REQUERIMIENTO 1
# ==============================
def categoryCaracterization(catalog, categoria, min_range, max_range): 
    category_info = mp.get(catalog['content_cateogries'], categoria)
    category_tree = me.getValue(category_info)
    category_tree['cmpfunction'] = cmpCategories2
    
    list_of_lists = om.values(category_tree, min_range, max_range)
    total = 0
    unique_artists = mp.newMap(numelements=5000, maptype='CHAINING', comparefunction=cmpCategories)
    
    for sub_list in lt.iterator(list_of_lists): 
        for item in lt.iterator(sub_list):
            if checkWithUser(catalog, item): 
                total += 1
                mp.put(unique_artists, item['artist_id'], item)

    artist = mp.size(unique_artists)
    return total, artist


# ==============================
# REQUERIMIENTO 2
# ==============================
def partyMusic(catalog, min_energy, max_energy, min_danceability, max_danceablity): 
    energy_tree = me.getValue(mp.get(catalog['content_cateogries'], 'energy'))

    energy_values = om.values(energy_tree, min_energy, max_energy)

    unique_tracks = mp.newMap(numelements=5000, maptype='CHAINING', comparefunction=cmpCategories)
    final_items = lt.newList(datastructure='ARRAY_LIST')
    for sublist in lt.iterator(energy_values):
        for event in lt.iterator(sublist): 
            if checkWithUser(catalog, event):
                if min_danceability <= float(event['danceability']) <= max_danceablity: 
                    lt.addLast(final_items, event)
                    mp.put(unique_tracks, event['track_id'], event)

    tracks = mp.size(unique_tracks)
    
    return final_items, tracks
              
# ==============================
# REQUERIMIENTO 3
# ==============================
def relaxingMusic(catalog, min_instrumentalness, max_instrumentalness, min_tempo, max_tempo):
    instrumentalness_tree = me.getValue(mp.get(catalog['content_cateogries'], 'instrumentalness'))
    instrumentalness_values = om.values(instrumentalness_tree, min_instrumentalness, max_instrumentalness)

    unique_tracks = mp.newMap(numelements=5000, maptype='CHAINING', comparefunction=cmpCategories)
    final_items = lt.newList(datastructure='ARRAY_LIST')
    for sublist in lt.iterator(instrumentalness_values):
        for event in lt.iterator(sublist): 
            if checkWithUser(catalog, event):
                if min_tempo <= float(event['tempo']) <= max_tempo: 
                    lt.addLast(final_items, event)
                    mp.put(unique_tracks, event['track_id'], event)

    tracks = mp.size(unique_tracks)
    
    return final_items, tracks



def checkWithUser(catalog, event):
    """
    Función que revisa eventos con archivo de usertrackinghashtags
    """
    event_date = event['created_at']
    event_date = datetime.datetime.strptime(event_date, '%Y-%m-%d %H:%M:%S')
    user_events_on_date = om.get(catalog['user_created_at'], event_date)

    for user_event in lt.iterator(me.getValue(user_events_on_date)):
        if (user_event['user_id'] == event['user_id']) and (user_event['track_id'] == event['track_id']):
            return True
    return False


# ==============================
# REQUERIMIENTO 4
# ==============================
def genresStudy(catalog, genres):
    answers_map = mp.newMap(numelements=10, maptype='PROBING', loadfactor=0.5,  comparefunction=cmpCategories)
    tempo_tree = me.getValue(mp.get(catalog['content_cateogries'], 'tempo'))
    for genre in genres:
        ranges = me.getValue(mp.get(catalog['genre_dictionary'], genre))
        tempo_values = om.values(tempo_tree, ranges['min'], ranges['max'])

        unique_artists = mp.newMap(numelements=5000, maptype='CHAINING', comparefunction=cmpCategories)
        final_list = lt.newList(datastructure='ARRAY_LIST')

        for sublist in lt.iterator(tempo_values):
            for event in lt.iterator(sublist): 
                if checkWithUser(catalog, event):
                    lt.addLast(final_list, event)
                    mp.put(unique_artists, event['artist_id'], event)
        
        mp.put(answers_map, genre, {'list': final_list, 'unique_artists': unique_artists})

    return answers_map


def newGenre(catalog, name, min_tempo, max_tempo):
    """
    Crea un nuevo genero y lo agrega al diccionario de generos
    """
    mp.put(catalog['genre_dictionary'], name, {'min': min_tempo, 'max': max_tempo})
    return catalog


# ==============================
# REQUERIMIENTO 5
# ==============================
def genreMostListened(catalog, min_time, max_time): 
    map_dates = catalog["content_time"]
    events_TimeDate = om.values(map_dates, min_time, max_time)
    genre_reps = mp.newMap(numelements=15, maptype='PROBING', comparefunction=cmpCategories)

    for sublist in lt.iterator(events_TimeDate):
        for event in lt.iterator(sublist): 
            if checkWithUserV2(catalog, event):
                tempo = event['tempo']
                track = event['track_id']
                matchTempo(catalog, tempo, genre_reps, track)   
    sort_list = lt.newList(datastructure="ARRAY_LIST", cmpfunction=cmpGenre)
    total = 0
    for genre in lt.iterator(mp.keySet(genre_reps)):
        reps = me.getValue(mp.get(genre_reps, genre))["reps"]
        lt.addLast(sort_list, {"genre": genre, "reps": reps})
        total += reps
    reps_sort = sort_list.copy()
    reps_sort = mer.sort(reps_sort, cmpGenre)
    top_genre = lt.firstElement(reps_sort)["genre"]
    tracks_sort = info_top_genre(catalog, top_genre, genre_reps) 
    return total, top_genre, reps_sort, tracks_sort  


def checkWithUserV2(catalog, event):
    event_date = event['created_at']
    event_date = datetime.datetime.strptime(event_date, '%Y-%m-%d %H:%M:%S')
    user_events_on_date = om.get(catalog['user_times'], event_date.time())

    for user_event in lt.iterator(me.getValue(user_events_on_date)):
        if (user_event['user_id'] == event['user_id']) and (user_event['track_id'] == event['track_id']):
            updateTrackHashtags(catalog, user_event)
            return True
    return False


def updateTrackHashtags(catalog, event):
    entry = mp.get(catalog['tracks_hashtag'], event['track_id'])
    if entry is None:
        hashtags = lt.newList(datastructure="ARRAY_LIST")
        mp.put(catalog['tracks_hashtag'], event['track_id'], hashtags) 
    else:
        hashtags = me.getValue(entry)    
    lt.addLast(hashtags, event['hashtag'].lower())
    mp.put(catalog['tracks_hashtag'], event['track_id'], hashtags)
    return catalog


def matchTempo(catalog, tempo, genre_reps, track):
    genre_map = catalog['genre_dictionary']

    for genre in lt.iterator(mp.keySet(genre_map)):
        ranges = me.getValue(mp.get(genre_map, genre))

        if ranges['min'] <= float(tempo) <= ranges['max']:
            g_reps = mp.get(genre_reps, genre)

            if g_reps is None:
                reps = 0
                # tracks = lt.newList(datastructure='ARRAY_LIST')
                tracks = mp.newMap()
            else:
                reps = me.getValue(g_reps)['reps']
                tracks = me.getValue(g_reps)['tracks']
                
            reps += 1
            # lt.addLast(tracks, track)
            mp.put(tracks, track, 1)
            mp.put(genre_reps, genre, {'reps': reps, 'tracks': tracks})
    return catalog
        

def info_top_genre(catalog, top_genre, genre_reps): 
    top_genre_tracks = me.getValue(mp.get(genre_reps, top_genre))["tracks"]
    top_genre_tracks = mp.keySet(top_genre_tracks)
    list_tracks = lt.newList(datastructure="ARRAY_LIST", cmpfunction=cmpNumHashtags)
    list_final_tracks = lt.newList(datastructure="ARRAY_LIST", cmpfunction=cmpNumHashtags)
    # map_final_tracks = mp.newMap(numelements=5000, maptype='CHAINING', comparefunction=cmpCategories)
    for track in lt.iterator(top_genre_tracks):
        hashtags = me.getValue(mp.get(catalog['tracks_hashtag'], track))
        num_hashtags = lt.size(hashtags)
        # mp.put(map_final_tracks, track, "")

        total_vader = 0 
        for hashtag in lt.iterator(hashtags): 
            vader = mp.get(catalog["sentimentvalues"], hashtag.lower())
            if (vader is not None): 
                vader = me.getValue(vader)
                if (vader != ''):
                    total_vader += float(vader)
            else: 
                num_hashtags -= 1
    
        if num_hashtags > 0:
            average = total_vader/num_hashtags
        else:
            average = 0
        track_info = {'track': track, 'num_hashtags': num_hashtags, 'average': average}
        lt.addLast(list_tracks, track_info)

    for n in range(0, 10):
        """Selecciona 10 videos aleatorios de la lista final, estos se imprimem""" 
        random_pos = random.randint(1,lt.size(list_tracks))
        random_track = lt.getElement(list_tracks, random_pos)
        lt.addLast(list_final_tracks, random_track)
        
    reps_sort = list_final_tracks.copy()
    reps_sort = mer.sort(reps_sort, cmpNumHashtags)

    return reps_sort, lt.size(top_genre_tracks)


# FUNCIONES DE CONSULTA
def getReps(answer):
    totalReps = 0
    for genre in lt.iterator(mp.keySet(answer)):
        totalReps += listSize(me.getValue(mp.get(answer, genre))['list'])
    
    return totalReps
        
def countArtist(catalog):
    # TODO: cargar como hashmap y sacar el size
    return mp.size(catalog['unique_artists'])

def countTracks(catalog):
    # TODO: cargar como hashmap y sacar el size
    return mp.size(catalog['unique_tracks'])


def getCateory(catalog, category): 
    category_info = mp.get(catalog['content_cateogries'], category)
    category_tree = None
    if category_info is not None:
        category_tree = me.getValue(category_info)
    return category_tree


def getGenre(catalog, genre):
    valid_g = mp.get(catalog['genre_dictionary'], genre)
    valid = None
    if valid_g is not None:
        valid = valid_g
    
    return valid


def listSize(lst):
    return lt.size(lst)


def mapSize(mps):
    return mp.size(mps)

# ==============================
# Funciones de Comparacion
# ==============================
def cmpNumHashtags(dict1,dict2):
    reps_1 = dict1["num_hashtags"]
    reps_2 = dict2["num_hashtags"]
    return reps_1 > reps_2


def cmpGenre(dict1,dict2):
    reps_1 = dict1["reps"]
    reps_2 = dict2["reps"]
    return reps_1 > reps_2



def cmpHashtags(hashtag1, hashtag2):
    hashtag2 = hashtag2['key']
    if hashtag1 > hashtag2: 
        return 1
    if hashtag1 < hashtag2: 
        return -1
    else:
        return 0

def cmpEvents(event1, event2):
    if event1 > event2: 
        return 1
    if event1 < event2: 
        return -1
    else:
        return 0

def cmpCategories(cat1, cat2):
    cat2 = cat2['key']
    if cat1 > cat2: 
        return 1
    if cat1 < cat2: 
        return -1
    else:
        return 0    

def cmpCategories2(cat1, cat2):
    if cat1 > cat2: 
        return 1
    if cat1 < cat2: 
        return -1
    else:
        return 0    

def cmpDates(date1, date2):
    """
    Compara dos fechas
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1  

def cmpUnique(artist1, artist2): 
    if artist1 < artist2: 
        return -1
    elif artist1 > artist2: 
        return 1
    else: 
        return 0

def cmpTimes(time1, time2): 
    if time1 > time2:
        return 1
    elif time1 < time2:
        return -1
    else:
        return 0


# datetime.time()¶
# Funciones de ordenamiento
 

