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
from DISClib.ADT.graph import gr
from DISClib.Algorithms.Graphs import dijsktra as dji
import time
import tracemalloc
assert cf

sys.setrecursionlimit(1000000000)


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

connections = 'connections.csv'
landing_points = 'landing_points.csv'
countries = 'countries.csv'

def printMenu():
    print("\nBienvenido")
    print("1- Inicializar el catalogo")
    print("2- Cargar información en el catálogo")
    print("3- Requerimiento 1")
    print("4- Requerimiento 2")
    print("5- Requerimiento 3")
    print("6- Requerimiento 4")
    print("7- Requerimiento 5")
    print("8- Requerimiento 6")
    print("9- Requerimiento 7")
    print("10- Requerimiento 8")


catalog = None


def getTime():
    return float(time.perf_counter()*1000)

def getMemory():
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

def memoryTime(start,start_time, start_memory):
    if start == True:
        delta_time = -1.0
        delta_memory = -1.0

        tracemalloc.start()

        start_time = getTime()
        start_memory = getMemory()
        return start_time,  start_memory
    else: 
        stop_memory = getMemory()
        stop_time = getTime()
        tracemalloc.stop()

        delta_time = stop_time - start_time
        delta_memory = deltaMemory(start_memory, stop_memory)

        return delta_time,delta_memory

"""
Menu principal
"""

while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalog = controller.initCatalog()

    elif int(inputs[0]) == 2:
        delta_time = -1.0
        delta_memory = -1.0
        tracemalloc.start()
        start_time = getTime()
        start_memory = getMemory()

        controller.loadData(catalog,connections,landing_points,countries)
        lastCountry=controller.lastCountry(catalog)
        firstLanding=controller.firstLandingPoint(catalog)

        stop_memory = getMemory()
        stop_time = getTime()
        tracemalloc.stop()
        delta_time = stop_time - start_time
        delta_memory = deltaMemory(start_memory, stop_memory)     

        print("Cantidad total de vertices: " , controller.graphSize(catalog['graph']))
        print("Cantidad total de arcos: ",controller.connectionsSize(catalog['graph']))
        print("Cantidad total de Landing Points : " , controller.mapSize(catalog['landing_points_map']))
        print("Cantidad de paises: ", controller.countrySize(catalog))
        print("\nLanding Point: ", firstLanding["landing_point_id"])
        print("Ubicación: ", firstLanding["name"])
        print("Latitud: ",firstLanding["latitude"])
        print("Longitud: ",firstLanding["longitude"])
        print("\nPais: ",lastCountry["CountryName"])
        print("Población: ",lastCountry["Population"])
        print("Usuarios de internet : ",lastCountry["Internet users"])
        print("\nTiempo gastado: ", delta_time," ms")
        print("Memoria utilizada: ", delta_memory, " kb")

    elif int(inputs[0])==3:
        
        landing1=input("Escriba el nombre del primer landing point: ")
        landing2=input("Escriba el nombre del segundo landing point: ")

        delta_time = -1.0
        delta_memory = -1.0
        tracemalloc.start()
        start_time = getTime()
        start_memory = getMemory()

        id_landing1=str(controller.findLandingPoint(catalog,landing1))
        id_landing2=controller.findLandingPoint(catalog,landing2)
        
        if id_landing1!=-1 and id_landing2!=-1:

            conectados=controller.areConnected(id_landing1,id_landing2,catalog['marine_graph'])
            scc = controller.SCC(catalog['graph'])

            stop_memory = getMemory()
            stop_time = getTime()
            tracemalloc.stop()
            delta_time = stop_time - start_time
            delta_memory = deltaMemory(start_memory, stop_memory)
            
            if conectados:
                print("Los dos landing points estan conectados")
            else:
                print("Los dos landing points no estan conectados")
            
            controller.bonoReq1(catalog,id_landing1, id_landing2)
            
        else:
            print("No hay ningun landing point con el nombre que acaba de especificar")

        print("Cantidad de componentes conectados: ",scc[0])
        print("\nTiempo gastado: ", delta_time," ms")
        print("Memoria utilizada: ", delta_memory, " kb")
        
    elif int(inputs[0])==4:
        delta_time = -1.0
        delta_memory = -1.0
        tracemalloc.start()
        start_time = getTime()
        start_memory = getMemory()

        controller.findInterconnectionCables(catalog)

        stop_memory = getMemory()
        stop_time = getTime()
        tracemalloc.stop()
        delta_time = stop_time - start_time
        delta_memory = deltaMemory(start_memory, stop_memory)

        print("\nTiempo gastado: ", delta_time," ms")
        print("Memoria utilizada: ", delta_memory, " kb")

    elif int(inputs[0])==5:
        countryA = (input("Escriba el nombre el primer pais: ")).title()
        countryB = (input("Escriba el nombre el segundo pais: ")).title()

        delta_time = -1.0
        delta_memory = -1.0
        tracemalloc.start()
        start_time = getTime()
        start_memory = getMemory()

        countryA = controller.getCapital(countryA,catalog)
        countryB = controller.getCapital(countryB,catalog)

        if (countryA and countryB) != None:
            dijsktra = controller.dijsktra(catalog['graph'],countryA)
            path = controller.path(dijsktra,countryB)

            stop_time = getTime()
            tracemalloc.stop()
            delta_time = stop_time - start_time
            delta_memory = deltaMemory(start_memory, stop_memory)
            
            for route in lt.iterator(path):
                print(route['vertexA'],"->",route['vertexB']," : ",route['weight'])
            print("Distancia total: ",dji.distTo(dijsktra,countryB))
            controller.bonoReq3(catalog,path)
            print("\nTiempo gastado: ", delta_time," ms")
            print("Memoria utilizada: ", delta_memory, " kb")

        else:
            print("Bueno panita, pls, escribe bien, o a lo mejor ese pais no existe")

    elif int(inputs[0])==6:
        delta_time = -1.0
        delta_memory = -1.0
        tracemalloc.start()
        start_time = getTime()
        start_memory = getMemory()

        mst = controller.mst(catalog['graph'])
        weight = controller.weight(catalog['graph'],mst)

        stop_time = getTime()
        tracemalloc.stop()
        delta_time = stop_time - start_time
        delta_memory = deltaMemory(start_memory, stop_memory)

        print("La cantidad de nodos de la red de expansion minima es: " ,mp.size(mst['marked']))
        print("La distancia total de la red de expansion minima es de: ",weight,"km")
        print("\nTiempo gastado: ", delta_time," ms")
        print("Memoria utilizada: ", delta_memory, " kb")

    elif int(inputs[0])==7:
        landing=input("Escriba el nombre del landing point: ")

        delta_time = -1.0
        delta_memory = -1.0
        tracemalloc.start()
        start_time = getTime()
        start_memory = getMemory()

        id_landing=str(controller.findLandingPoint(catalog,landing))
        if id_landing != -1:
            cables_list = controller.landingCables(catalog,id_landing)
            afected = controller.afected(catalog,cables_list)

            stop_time = getTime()
            tracemalloc.stop()
            delta_time = stop_time - start_time
            delta_memory = deltaMemory(start_memory, stop_memory)

            print("La cantidad de paises afectados es: ",lt.size(afected))
            print("La lista de paises afectados es la siguiente: ")
            for country in lt.iterator(afected):
                print(country['CountryName'],"->",country['distance'])
            print("\nTiempo gastado: ", delta_time," ms")
            print("Memoria utilizada: ", delta_memory, " kb")
            controller.bonoReq5(catalog,afected,id_landing)
        else:
            print("Hermanit@, tal vez ese nombre no sea el correcto")
    
    elif int(inputs[0])==8:
        country = input("Escriba el nombre del pais: ").title()
        cable_name = input("Escriba el nombre del cable: ")

        delta_time = -1.0
        delta_memory = -1.0
        tracemalloc.start()
        start_time = getTime()
        start_memory = getMemory()

        landing_list = controller.getCableName(catalog,cable_name)
        if landing_list != -1:
            wideband = controller.wideOfBand(catalog,landing_list,country)
            keys = mp.keySet(wideband)

            stop_time = getTime()
            tracemalloc.stop()
            delta_time = stop_time - start_time
            delta_memory = deltaMemory(start_memory, stop_memory)

            for con in lt.iterator(keys):
                value = mp.get(wideband,con)['value']
                print(con," - Se puede garantizar un ancho de banda de: ",round(value,3)," Mbps")
            print("\nTiempo gastado: ", delta_time," ms")
            print("Memoria utilizada: ", delta_memory, " kb")
        else: 
            print("Mano, ese nombre de cable no existe")

    elif int(inputs[0])==9:
        ip1=input("Ingresa la primera dirección ip, papi: ")
        ip2=input("Ingresa la segunda dirección ip, papi/mami: ")

        delta_time = -1.0
        delta_memory = -1.0
        tracemalloc.start()
        start_time = getTime()
        start_memory = getMemory()

        path=controller.tupapi(catalog,ip1,ip2)
        counter=0

        stop_time = getTime()
        tracemalloc.stop()
        delta_time = stop_time - start_time
        delta_memory = deltaMemory(start_memory, stop_memory)

        for route in lt.iterator(path):
            print(route['vertexA'],"->",route['vertexB']," : ",route['weight'])
            counter+=1
        print("La cantidad de saltos que se deben realizar son : ",counter)
        print("\nTiempo gastado: ", delta_time," ms")
        print("Memoria utilizada: ", delta_memory, " kb")
    

    else:
        sys.exit(0)

sys.exit(0)


