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
import tracemalloc
import time
import config as cf
import sys
import datetime
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.ADT import map as mp
assert cf
import model
from DISClib.DataStructures import mapentry as me
from DISClib.DataStructures import listiterator as it


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Cargar información de eventos")
    print("3- Consultar número de eventos en un rango para una característica de contenido")
    print("4- Consultar canciones de fiesta")
    print("5 - Consultar canciones para estudiar")
    print("6 - Consultar número de canciones para un género")
    print("7 - Indicar el género musical más escuchado en el tiempo")
    print("0- Salir")

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("")
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:

        x=controller.loadData(cont)
        catalog=x[0]
        eventos=catalog['eventos']
        tracks=catalog['hashtagsportrack']

        print('\nSe cargaron '+str(lt.size(eventos))+' eventos de escucha.')
        print('Se cargaron '+str(mp.size(tracks))+' pistas de audio únicas.')
        print('Se cargaron '+str(x[1])+' artistas únicos.\n')
        print('Información de los 5 primeros eventos\n')

        n=1
        while n<=5:
            evento=lt.getElement(eventos,n)
            print('('+str(n)+') || track id: '+evento['track_id']+'|| artist id: '+evento['artist_id']+' || user id: '+evento['user_id']+' || instrumentalness: '+evento['instrumentalness']+' || liveness: '+evento['liveness']+' || speechiness: '+evento['speechiness']+' || danceability: '+evento['danceability']+' || valence: '+evento['valence']+' || loudness '+evento['loudness']+' || tempo: '+evento['tempo']+' || acousticness: '+evento['acousticness']+' || energy: '+evento['energy']+'\n')
            n+=1
        print('Información de los 5 últimos eventos\n')

        m=(lt.size(eventos)-4)
        while m<=lt.size(eventos):
            evento=lt.getElement(eventos,m)
            print('('+str(n)+') || track id: '+evento['track_id']+'|| artist id: '+evento['artist_id']+' || user id: '+evento['user_id']+' || instrumentalness: '+evento['instrumentalness']+' || liveness: '+evento['liveness']+' || speechiness: '+evento['speechiness']+' || danceability: '+evento['danceability']+' || valence: '+evento['valence']+' || loudness '+evento['loudness']+' || tempo: '+evento['tempo']+' || acousticness: '+evento['acousticness']+' || energy: '+evento['energy']+'\n')
            m+=1
            n+=1
        
        

        input('Presione enter para continuar')
        
    elif int(inputs[0])==3:
        minimo=float(input('Ingrese el valor mínimo del rango: '))
        maximo=float(input('Ingrese el valor máximo del rango: '))
        feature=input('Ingrese la característica de contenido: ')
        x=controller.req1(minimo,maximo,feature.lower(),catalog)
        print("Tiempo [ms]: "+f"{x[0]:.3f}"+" ||  "+"Memoria [kB]: "+f"{x[1]:.3f}"+'\n')
        input('Presione enter para continuar')
       

    elif int(inputs[0])==4:
        minenergy=float(input('Valor inferior energy: '))
        maxenergy=float(input('Valor superior energy: '))
        mindance=float(input('Valor inferior danceability: '))
        maxdance=float(input('Valor superior danceability: '))
        x=controller.req2(catalog,minenergy,maxenergy,mindance,maxdance)
        print("\nTiempo [ms]: "+f"{x[0]:.3f}"+" ||  "+"Memoria [kB]: "+f"{x[1]:.3f}"+'\n')
        input('Presione enter para continuar')

    elif int(inputs[0])==5:
        mininstrum=float(input('Valor inferior instrumentalness: '))
        maxinstrum=float(input('Valor superior instrumentalness: '))
        mintempo=float(input('Valor inferior tempo: '))
        maxtempo=float(input('Valor superior tempo: '))
        x=controller.req3(catalog,mininstrum,maxinstrum,mintempo,maxtempo)
        print("\nTiempo [ms]: "+f"{x[0]:.3f}"+" ||  "+"Memoria [kB]: "+f"{x[1]:.3f}"+'\n')
        input('Presione enter para continuar')
    
    elif int(inputs[0])==6:
        delta_time = -1.0
        delta_memory = -1.0

        tracemalloc.start()
        start_time = controller.getTime()
        start_memory = controller.getMemory()

        x=int(input('¿Desea conocer información sobre géneros ya existentes? [0: sí // 1: no]: '))
        if x==0:
            genres=input('¿Cuáles? [escríbalos separados por una coma y espacio. Ej: reggae, hip-hop]: ')
            lista=(genres.lower()).split(', ')
            for genre in lista:
                controller.req4(catalog,genre,None,None)
            print('\n')
        y=int(input('¿Desea conocer información sobre un género no existente? [0: sí // 1: no]: '))
        if y==0:
            name=input('Ingrese el nombre del nuevo género: ')
            minim=float(input('Ingrese el valor mínimo de tempo: '))
            maxim=float(input('Ingrese el valor máximo de tempo: '))
            controller.req4(catalog,name,minim,maxim)
            print('\n')

        stop_memory = controller.getMemory()
        stop_time = controller.getTime()
        tracemalloc.stop()

        delta_time = stop_time - start_time
        delta_memory = controller.deltaMemory(start_memory, stop_memory)
        print("Tiempo [ms]: "+f"{delta_time:.3f}"+" ||  "+"Memoria [kB]: "+f"{delta_memory:.3f}"+'\n')
        input('Presione enter para continuar')

    elif int(inputs[0])==7:
        x=input('Ingrese la hora mínima del rango [en formato H:MM:SS Ej: 0:00:00]: ')
        info=datetime.datetime.strptime(x,'%H:%M:%S')
        time1=info.time()
        y=input('Ingrese la hora máxima del rango [en formato H:MM:SS Ej: 0:00:00]: ')
        info1=datetime.datetime.strptime(y,'%H:%M:%S')
        time2=info1.time()
        x = controller.req5(catalog,time1,time2)

        print("\nTiempo [ms]: "+f"{x[0]:.3f}"+" ||  "+"Memoria [kB]: "+f"{x[1]:.3f}"+'\n')

        input('Presione enter para continuar')



    else:
        sys.exit(0)
sys.exit(0)