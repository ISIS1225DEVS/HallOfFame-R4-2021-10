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
 """

from datetime import datetime
import config as cf
import model
import csv
from DISClib.DataStructures import listiterator as it
from DISClib.ADT import orderedmap as om
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import list as lt
from DISClib.Algorithms.Sorting import mergesort as mrge
import tracemalloc
import time


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # catalog es utilizado para interactuar con el modelo
    catalog = model.newCatalog()
    return catalog


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento de datos en los modelos
# ___________________________________________________

def loadData(catalog):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    
    file3=cf.data_dir+'sentiment_values.csv'
    input_file3=csv.DictReader(open(file3, encoding="utf-8"),delimiter=",")
    for hashtag in input_file3:
        if hashtag['vader_avg']!='':
            model.addhashtag(catalog,hashtag['hashtag'],hashtag['vader_avg'])

    file1=cf.data_dir+'user_track_hashtag_timestamp-small.csv'
    input_file1 = csv.DictReader(open(file1, encoding="utf-8"),delimiter=",")
    for event in input_file1:
        model.addpromtrack(catalog,event)

    file2=cf.data_dir + 'context_content_features-small.csv'
    input_file2 = csv.DictReader(open(file2, encoding="utf-8"),delimiter=",")
    
    artists=mp.newMap(numelements=11000)
    for event in input_file2:
        model.addevent(catalog,event)
        mp.put(artists,event['artist_id'],None)

    return catalog,mp.size(artists)

def req1(menor,mayor,feature,catalog):
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    events = om.values(catalog[feature],menor,mayor)
    num_events = model.numevents(events)
    num_artists = (model.artists(events,None))[0]

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    print('\n'+(feature.capitalize())+' is between '+str(menor)+' and '+str(mayor)+'\nTotal of reproduction: '+str(num_events)+'\nTotal of unique artists: '+str(num_artists)+'\n')

    return delta_time, delta_memory

def req2(catalog,min_en,max_en,min_dan,max_dan):
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    listadeentries1 = om.values(catalog["energy"],min_en,max_en)
    mapa1 = model.mapaeventos(listadeentries1)
    listadeentries2=om.values(catalog["danceability"],min_dan,max_dan)
    tracksencomun=model.tracksencomun(mapa1,listadeentries2)
    print('\nEnergy is between '+str(min_en)+' and '+str(max_en))
    print('Danceability is between '+str(min_dan)+' and '+str(max_dan))
    print('Total of unique tracks in events: '+str(tracksencomun[0]))
    print('\n--- Unique track_id ---')
    lista=tracksencomun[1]
    i=it.newIterator(lista)
    x=1
    while it.hasNext(i):
        tupla=it.next(i)
        features=tupla[1]
        print('Track '+str(x)+': '+tupla[0]+' with energy of '+str(features[0])+' and danceability of '+str(features[1]))
        x+=1

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return delta_time, delta_memory


def req3(catalog,min_inst,max_inst,min_temp,max_temp):
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    listadeentries1 = om.values(catalog['instrumentalness'],min_inst,max_inst)
    mapa1 = model.mapaeventos(listadeentries1)
    listadeentries2=om.values(catalog['tempo'],min_temp,max_temp)
    tracksencomun=model.tracksencomun(mapa1,listadeentries2)
    print('\Instrumentalness is between '+str(min_inst)+' and '+str(max_inst))
    print('Tempo is between '+str(min_temp)+' and '+str(max_temp))
    print('Total of unique tracks in events: '+str(tracksencomun[0]))
    print('\n--- Unique track_id ---')
    lista=tracksencomun[1]
    i=it.newIterator(lista)
    x=1
    while it.hasNext(i):
        tupla=it.next(i)
        features=tupla[1]
        print('Track '+str(x)+': '+tupla[0]+' with instrumentalness of '+str(features[0])+' and tempo of '+str(features[1]))
        x+=1

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return delta_time, delta_memory


def req4(catalog,genre,minimo,maximo):
 
    mapa = catalog["tempo"]

    if minimo==None and maximo==None:
        x=model.tempobygenre(genre)
        menor=x[0]
        mayor=x[1]
    else:
        menor=minimo
        mayor=maximo

    events = om.values(mapa,menor,mayor)
    num_events = model.numevents(events)
    artists=(model.artists(events,10))
    numartists=artists[0]
    listartists=artists[1]

    print('\n======= '+genre.upper()+' ========'+'\nFor '+genre+' the tempo is between '+str(menor)+' and '+str(mayor)+'\n'+genre+' reproductions: '+str(num_events)+' with '+str(numartists)+' different artists'+'\n\n---- Some artists for '+genre+' -----\n')
    i=it.newIterator(listartists)
    n=1
    while it.hasNext(i):
        artist=it.next(i)
        print('Artist '+str(n)+': '+artist)
        n+=1
    
   


def req5(catalog,minim,maxim):
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    mapa=mp.newMap(maptype="PROBING",loadfactor=0.5)
    mapafinal=mp.newMap()
    total=0
    mayor=None
    mayorkey=0
    lista=om.values(catalog['time'],minim,maxim)
    mapa=model.genresandtracks(lista)
    genres=mp.keySet(mapa)
    i=it.newIterator(genres)
    while it.hasNext(i):
        genre=it.next(i)
        x=mp.get(mapa,genre)
        entry=me.getValue(x)
        eventos=mp.size(entry['events'])
        mp.put(mapafinal,eventos,genre)
        total+=eventos

    numevents=mp.keySet(mapafinal)
    ordered=mrge.sort(numevents,cmpnums)
    i=it.newIterator(ordered)
    n=1
    while it.hasNext(i):
        key=it.next(i)
        par=mp.get(mapafinal,key)
        value=me.getValue(par)
        if n==1:
            mayor=value
            mayorkey=key
        print('TOP '+str(n)+': '+value.capitalize()+' with '+str(key)+' reps')
        n+=1

    pareja=mp.get(mapa,mayor)
    entry=me.getValue(pareja)
    tuplas=mp.keySet(entry['events'])
    x=model.orderednums(catalog, tuplas)
    mapanums=x[0]
    print('\nThe TOP GENRE is '+mayor.capitalize()+' with '+str(mayorkey)+' reproductions')
    print('========== '+mayor.upper()+' SENTIMENT ANALYSIS ==========')
    print(mayor.capitalize()+' has '+str(mp.size(x[1]))+' unique tracks')


    listanums=lt.newList(datastructure='ARRAY_LIST')
    llavesnums=(mp.keySet(mapanums))
   
    n = it.newIterator(llavesnums)
    m=1
    while it.hasNext(n):
        num=it.next(n)
        lt.addLast(listanums,num)
    mergednums=mrge.sort(listanums,cmpnums)
    centinela=True
    d=it.newIterator(mergednums)
    while it.hasNext(d) and centinela==True:
        num=it.next(d)
        par=mp.get(mapanums,num)
        listatuplas=me.getValue(par)
        t=it.newIterator(listatuplas)
        while it.hasNext(t) and centinela==True:
            tupla=it.next(t)
            print('TOP '+str(m)+' track: '+tupla[0]+' with '+str(num)+' hashtags and VADER = '+str(tupla[1]))
            m+=1
            if m>10:
                centinela=False

    print('\n')
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    
    return delta_time, delta_memory


def getTime():
    return float(time.perf_counter()*1000)


def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(start_memory, stop_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory

def cmpnums(num1,num2):
    return(num1>num2)