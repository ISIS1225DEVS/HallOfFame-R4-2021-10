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


from DISClib.DataStructures.chaininghashtable import valueSet
from os import name

from branca.element import Html
import config as cf
import math
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT.graph import gr
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.DataStructures import linkedlistiterator as lli
from DISClib.Algorithms.Graphs import scc as scc
from DISClib.Algorithms.Graphs import dfs as dfs
from DISClib.Algorithms.Graphs import dijsktra as dji
from DISClib.Algorithms.Graphs import prim as prim
from DISClib.DataStructures import edge as edg
import ipapi
import folium
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""
# Construccion de modelos
def newCatalog():

    catalog = {
               'graph':None,
               'landing_points_map':None,
               'countries':None
               }
    """Grafo cuyos vertices son la cadena <landing_point><cable_name> y los arcos son las distancias entre ellos(km)"""
    catalog['graph'] = gr.newGraph(datastructure='ADJ_LIST',
                                         directed = False,
                                         size= 15000,
                                         comparefunction=compareJointId)

    """Grafo cuyos vertices son los landing point"""
    catalog['marine_graph'] = gr.newGraph(datastructure='ADJ_LIST',
                                         directed = False,
                                         size= 15000,
                                         comparefunction=compareJointId)
    "Grafo igual al principal, pero los pesos siempre son 1"
    catalog["second_graph"]=gr.newGraph(datastructure='ADJ_LIST',
                                         directed = False,
                                         size= 15000,
                                         comparefunction=compareJointId)

    """ Tabla de hash donde la llave es el nombre del landing Point y el valor es su id"""
    catalog["landing_points_by_name"]=mp.newMap(numelements=1300,maptype='PROBING')


    catalog['landing_points_map'] = mp.newMap(numelements=1500,
                                          maptype='PROBING')
    
    catalog['same_landing_point_map']=mp.newMap(numelements=1500,maptype='PROBING')
    

    catalog['countries'] = mp.newMap(numelements=250,
                                          maptype='PROBING')
    
    catalog['landing_by_country_map'] = mp.newMap(numelements=15000,
                                          maptype='PROBING')

    catalog["countries_name"]=lt.newList("ARRAY_LIST")

    catalog["landing_points_name"]=lt.newList("ARRAY_LIST")

    catalog['landing_cable_map'] = mp.newMap(numelements=2500,
                                          maptype='PROBING')
    
    catalog['cable_name_map'] = mp.newMap(numelements=5000,
                                          maptype='PROBING')
    return catalog



# Funciones para agregar informacion al catalogo

def addLandingPoint(catalog, landing_point):
    """
    Agrega a un mapa por llaves landing_point_id y valor la info de ese
    Agrega a un mapa por llaves country y valores listas de landing de este country
    Agrega a un tabla de hash como llave el nombre de la ciudad del landing point y como valor el id de este
    """

    name=landing_point["name"].split(",")
    city_name=name[0].lower()
    country = name[-1].title()
    landing_point['Country'] = country

    mp.put(catalog["landing_points_by_name"],city_name,landing_point["landing_point_id"])
    mp.put(catalog['landing_points_map'],landing_point['landing_point_id'],landing_point)
    lt.addLast(catalog["landing_points_name"],landing_point["landing_point_id"])

    country = landing_point['name'].split(',')
    country = country[-1].lower().strip()
    exists = mp.get(catalog['landing_by_country_map'],country)

    if exists is None: 
        points_list=lt.newList(datastructure="ARRAY_LIST")
        lt.addLast(points_list,landing_point['landing_point_id'])
    else:
        points_list=me.getValue(exists)
        if not lt.isPresent(points_list,landing_point['landing_point_id']):
            lt.addLast(points_list,landing_point['landing_point_id'])

    mp.put(catalog["landing_by_country_map"],country,points_list)

def addMarinePoint(catalog, landing_point):
    """Agrega un vertice al grafo marine_graph cuyo nombre es el id del landing point"""
    name = landing_point['landing_point_id']
    addMarine(catalog,name)

def addMarineCable(catalog,cable):
    """Añade un arco entre 2 vertices cuya distancia es 1
    """
    origin = cable['origin']
    destination= cable['destination']
    gr.addEdge(catalog['marine_graph'],origin, destination,1)

def addCable(catalog, cable):
    """
    Se crean 2 vertices con formato <landing_point><cable_name>

    Se añade el arco entre estos 2 vertices cuyo valor es la distancia entre ellos
    
    Se añade a una tabla de hash una lista que contiene los cables de un mismo landing point por cada landing point diferente 

    diccionario = {  landing_point1: [<landing_point1><cable_name>, <landing_point1><cable_name2>]}
    """
    origin = cable['origin']
    ori_couple = mp.get(catalog['landing_points_map'],origin)
    ori_coor = me.getValue(ori_couple)

    destination = cable['destination']
    des_couple = mp.get(catalog['landing_points_map'],destination)
    des_coor = me.getValue(des_couple)

    distance = haversine(float(ori_coor['latitude']),float(ori_coor['longitude']),float(des_coor['latitude']),float(des_coor['longitude']))

    name_ori = formatVertex(cable['origin'],cable['cable_name'])
    name_des = formatVertex(cable['destination'],cable['cable_name'])

    mp.put(catalog['landing_cable_map'],name_ori,cable) 
    mp.put(catalog['landing_cable_map'],name_ori,cable) 

    addJoint(catalog["graph"],name_ori)
    addJoint(catalog["graph"],name_des)
    addJoint(catalog["second_graph"],name_ori)
    addJoint(catalog["second_graph"],name_des)

    addConnection(catalog["graph"], name_ori, name_des, distance)
    
    addLandingFamily(catalog,cable['origin'],name_ori) 
    addLandingFamily(catalog,cable['destination'],name_des) 

def addLandingConnection(catalog):
    """
    Se añaden arcos entre los vertices que tengan mismo landing point pero diferente cable_name

    La distancia entre los arcos es de 100 metros
    """
    landing_points_list=mp.keySet(catalog["same_landing_point_map"])

    for landing_point in lt.iterator(landing_points_list):
        cable_couple=mp.get(catalog["same_landing_point_map"],landing_point)
        cable_names=me.getValue(cable_couple)
        previous_cable=None
        for cable in lt.iterator(cable_names):
            if previous_cable!=None:
                origin= cable
                destination= previous_cable
                addConnection(catalog["graph"],origin,destination,0.1)
                
            previous_cable=cable
        #Cerrar el ciclo al unir el primero con el ultimo
        cable = lt.firstElement(cable_names)
        origin=cable
        destination=previous_cable
        addConnection(catalog["graph"],origin,destination,0.1)

def addCountryPoint(catalog, country):
    """
    Se crea un vertice con formato <CountryName><CapitalName>
    """
    if country['CountryName'] != "":
        countryname = country['CountryName']+'-'+country['CapitalName']
        country['name'] = countryname
        country['id'] = countryname
        mp.put(catalog['landing_cable_map'],countryname,country)
        addJoint(catalog["graph"], countryname)
        

def addCountry(catalog,country):
    """
    Se añade a una tabla de hash la llave: CountryName, y su valor: Country(caracteristicas del pais cargado)
    """
    mp.put(catalog["countries"],country["CountryName"],country)
    lt.addLast(catalog["countries_name"],country)

def addCountryConnections(catalog,country):
    """
    Por cada pais se añade un arco entre la capital de este y todos los vertices que pertenecen a dicho pais. El peso del arco es la
    distancia entre el landing point y la capital
    """
    country_lat = country["CapitalLatitude"]
    country_lon = country["CapitalLongitude"]

    countries_couple = mp.get(catalog['landing_by_country_map'],country['CountryName'].lower())

    if countries_couple is not None:
        countries_list = me.getValue(countries_couple)

        for landingpoint in lt.iterator(countries_list):
            country_format=country["CountryName"]+'-'+country["CapitalName"]

            info_couple = mp.get(catalog['landing_points_map'],landingpoint)
            info = me.getValue(info_couple)

            landing_lat = info['latitude']
            landing_lon = info['longitude']

            distance = haversine(float(country_lat),float(country_lon),float(landing_lat),float(landing_lon))

            family_couple = mp.get(catalog['same_landing_point_map'],landingpoint)
            family = me.getValue(family_couple)


            for cable in lt.iterator(family):
                addConnection(catalog["graph"], cable, country_format,distance)
                couple_cable = mp.get(catalog['landing_cable_map'],cable)
                info_cable = me.getValue(couple_cable)
                info_cable["CountryName"] = country["CountryName"]
                info_cable["id"] = country_format
                mp.put(catalog['landing_cable_map'],cable,info_cable)
                exists_country = mp.get(catalog['same_landing_point_map'],country_format)

                """
                if exists_country is not None:
                    cables_list = me.getValue(exists_country)
                    lt.addLast(cables_list,cable)
                
                else:
                    cables_list = lt.newList(datastructure='SINGLE_LINKED')
                    lt.addLast(cables_list,cable)
                
                mp.put(catalog['same_landing_point_map'],country_format,cables_list)

            lt.addLast(family,country_format)
            mp.put(catalog["same_landing_point_map"],landingpoint,family)
    """    
    else: 
        minimum = 1000000 
        landind_ward = None
        landing_points = mp.keySet(catalog['landing_points_map'])
        for landing_point in lt.iterator(landing_points):
            info_couple = mp.get(catalog['landing_points_map'],landing_point)
            info = me.getValue(info_couple)

            landing_lat = info['latitude']
            landing_lon = info['longitude']

            distance = haversine(float(country_lat),float(country_lon),float(landing_lat),float(landing_lon))

            if distance < minimum:
                minimum = distance
                landind_ward = landing_point
        
        family_couple = mp.get(catalog['same_landing_point_map'],landind_ward)
        family = me.getValue(family_couple)
        for cable in lt.iterator(family):
            addConnection(catalog["graph"], cable, country['CountryName']+'-'+country['CapitalName'],minimum)
        
        newCable=country["CountryName"]+'-'+country["CapitalName"]       
        lt.addLast(family,newCable)
        mp.put(catalog["same_landing_point_map"],landind_ward,family)

def addCableName(catalog,cable):
    exists = mp.get(catalog['cable_name_map'],cable['cable_name'])
    if exists is not None:
        list = me.getValue(exists)
    else:
        list = lt.newList(datastructure='ARRAY_LIST')
    lt.addLast(list,cable)
    mp.put(catalog['cable_name_map'],cable['cable_name'],list)

def secondGraph(catalog):
    listVertex=gr.vertices(catalog["graph"])
    for vertex in lt.iterator(listVertex):
        if not gr.containsVertex(catalog["second_graph"],vertex):
            gr.insertVertex(catalog["second_graph"],vertex)
        adjacents=gr.adjacents(catalog["graph"],vertex)
        for adjacent in lt.iterator(adjacents):
            if not gr.containsVertex(catalog["second_graph"],adjacent):
                gr.insertVertex(catalog["second_graph"],adjacent)
            gr.addEdge(catalog["second_graph"],vertex,adjacent,1)


# Funciones para creacion de datos

def formatVertex(origin, name):
    format = origin + '-' + name
    return format

def addJoint(graph, vertex):
    if not gr.containsVertex(graph,vertex):
        gr.insertVertex(graph,vertex)

def addMarine(catalog, vertex):
    if not gr.containsVertex(catalog['marine_graph'],vertex):
        gr.insertVertex(catalog['marine_graph'],vertex)

def addConnection(graph, origin, destination, distance):
    edge = gr.getEdge(graph,origin,destination)
    if edge is None:
        gr.addEdge(graph,origin, destination,distance)

def addLandingFamily(catalog,landing_point,format_name):

    same_landing=mp.get(catalog["same_landing_point_map"],landing_point)
    if same_landing is None: 
        cables_list=lt.newList(datastructure="ARRAY_LIST")
        lt.addLast(cables_list,format_name)
    else:
        cables_list=me.getValue(same_landing)
        if not lt.isPresent(cables_list,format_name):
            lt.addLast(cables_list,format_name)
    mp.put(catalog["same_landing_point_map"],landing_point,cables_list)


# Funciones de consulta

def graphSize(graph):
    return gr.numVertices(graph)

def connectionsSize(graph):
    return gr.numEdges(graph)

def countrySize(catalog):
    return lt.size(catalog["countries_name"])

def lastCountry(catalog):
    lastCountry=lt.lastElement(catalog["countries_name"])
    return lastCountry

def firstLandingPoint(catalog):
    firstLanding=lt.firstElement(catalog["landing_points_name"])
    
    couple=mp.get(catalog["landing_points_map"],firstLanding)

    landing_info=me.getValue(couple)

    return landing_info

def mapSize(map):
    return mp.size(map)

def findLandingPoint(catalog,landingPoint):
    """
    Busca en la tabla de hash el id de la ciudad que entra por parametro y lo retorna. Si la ciudad no existe, retorna -1
    """
    landingPoint=landingPoint.lower()

    landingCouple=mp.get(catalog["landing_points_by_name"],landingPoint)

    if landingCouple is not None:
        return me.getValue(landingCouple)
    else:
        return -1

def getCapital(country,catalog):
    capital_couple = mp.get(catalog['countries'],country)
    capital = None
    if capital_couple is not None:
        capital = me.getValue(capital_couple)
        capital = capital["CountryName"]+'-'+capital["CapitalName"]
    return capital

def landingCables(catalog,id_landing):
    landing_map = catalog['same_landing_point_map']
    couple = mp.get(landing_map,id_landing)
    return me.getValue(couple)

def afected(catalog,cables_list):
    #countries = mp.newMap(numelements=100,maptype='PROBING')
    countries_list = lt.newList(datastructure='ARRAY_LIST',cmpfunction=compareCountries)
    for cable in lt.iterator(cables_list):
        adjacents = gr.adjacents(catalog['graph'],cable)
        for adj_vertex in lt.iterator(adjacents):
            landing = adj_vertex.split('-')[0]
            couple = mp.get(catalog['landing_points_map'],landing)
            if couple is not None:
                value = me.getValue(couple)
                country = value['name'].split(',')[-1].title().strip()
                latitude = value['latitude']
                longitude = value['longitude']

                countries = mp.get(catalog['countries'],country)['value']
                latitude_c = countries['CapitalLatitude']
                longitude_c = countries['CapitalLongitude']
                distance = haversine(float(latitude),float(longitude),float(latitude_c),float(longitude_c))
                countries['distance'] =  distance

                if not lt.isPresent(countries_list,countries):
                    lt.addLast(countries_list,countries)

                #mp.put(countries,country,0)
    sa.sort(countries_list,compareDistance)
    return countries_list

def getCableName(catalog,cable_name):

    exists = mp.get(catalog['cable_name_map'],cable_name)
    if exists is not None:
        return me.getValue(exists)
    else:
        return -1



# Funciones utilizadas para comparar elementos dentro de un grafo

def compareJointId(stop, keyvaluestop):
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop >stopcode):
        return 1
    else:
        return -1
        
# Funciones utilizadas para comparar elementos dentro de una lista

def compareDistance(country1,country2):
    return (float(country1['distance'])>float(country2['distance']))

def compareCountries(country1,country2):
    if (float(country1['distance']) == float(country2['distance'])):
        return 0
# Funciones de cracks

def SCC(graph):
    kosa = scc.KosarajuSCC(graph)
    return scc.connectedComponents(kosa),kosa

def areConnected(landing1,landing2,graph):
    kosa = scc.KosarajuSCC(graph)
    return scc.stronglyConnected(kosa,landing1,landing2)

def findInterconnectionCables(catalog):

    vertexs = gr.vertices(catalog['graph'])
    greater = 0
    identifier = None
    counter = 1
    for vertex in lt.iterator(vertexs):
        degree = gr.degree(catalog['graph'],vertex)
        couple = mp.get(catalog['landing_cable_map'],vertex)
        info = me.getValue(couple)
        if degree > greater:
            greater = degree
            identifier = vertex

        if "CountryName" in info:
            print(counter, vertex,info["CountryName"],vertex)
        else:
            print(counter,info['name'],info['CountryName'],info['id'])
        counter += 1
    print("El landing-point mas interconectado es ",identifier," con :",greater," conexiones")
    bonoReq2(catalog,identifier)
    

def dijsktra(graph,source):
    return dji.Dijkstra(graph,source)

def path(dijsktra,countryB):
    return dji.pathTo(dijsktra,countryB)

def mst(graph):
    return prim.PrimMST(graph)

def weight(graph,mst):
    return prim.weightMST(graph,mst)

    
# Funciones para hacer calculos 

def haversine(lat1,lon1,lat2,lon2):
    radius = 6371 # km
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d

#Funciones para los filtros

def wideOfBand(catalog,landing_list,country):
    countries = mp.newMap(maptype='PROBING')
    for cable in lt.iterator(landing_list):
        origin = cable['origin']
        country_origin = mp.get(catalog['landing_points_map'],origin)['value']['Country'].strip()
        users = mp.get(catalog['countries'],country_origin)['value']['Internet users']
        wide = cable['capacityTBPS']
        calculation = (float(wide)/float(users))*1000000
        if country_origin != country:
            mp.put(countries,country_origin,calculation)
    return countries

def tupapi(catalog,ip1,ip2):
    if ip1=="8.8.8.8":
        latitude1=37.417661109182816
        longitude1= -122.08286045229197
        latitude2=float(ipapi.location(ip2)["latitude"])
        longitude2=float(ipapi.location(ip2)["longitude"])
        
    if ip2=="8.8.8.8":
        latitude1=float(ipapi.location(ip1)["latitude"])
        longitude1=float(ipapi.location(ip1)["longitude"])
        latitude2=37.417661109182816
        longitude2= -122.08286045229197
    
    x=mp.valueSet(catalog["landing_points_map"])
    min1=100000000000000
    landing1=""

    min2=100000000000000
    landing2=""
    for landing in lt.iterator(x):
        localLatitude=float(landing["latitude"])
        localLongitude=float(landing["longitude"])

        distance1=haversine(latitude1,longitude1,localLatitude,localLongitude)
        distance2=haversine(latitude2,longitude2,localLatitude,localLongitude)

        if distance1<min1:
            min1=distance1
            landing1=landing["landing_point_id"]
        if distance2<min2:
            min2=distance2
            landing2=landing["landing_point_id"]

    
    list_landingPoint1=mp.get(catalog["same_landing_point_map"],landing1)["value"]
    list_landingPoint2=mp.get(catalog["same_landing_point_map"],landing2)["value"]

    landingPoint1=lt.firstElement(list_landingPoint1)
    landingPoint2=lt.firstElement(list_landingPoint2)

    dikstra=dji.Dijkstra(catalog["second_graph"],landingPoint1)
    path=dji.pathTo(dikstra,landingPoint2)
    return path
    
# Funciones para graficar a lo chupapi muñaño †


def bonoReq1(catalog,id_landing1, id_landing2):
    map = folium.Map(location=[0,0],zoom_start=2)
    value_set = mp.valueSet(catalog['landing_points_map'])
    land1 = mp.get(catalog['landing_points_map'],id_landing1)['value']
    land2 = mp.get(catalog['landing_points_map'],id_landing2)['value']
    for landing_info in lt.iterator(value_set):
        latitude = landing_info['latitude']
        longitude = landing_info['longitude']
        name = landing_info['name']
        folium.Marker([latitude, longitude], popup=name).add_to(map)
    folium.Marker(location=[land1['latitude'],land1['longitude']],popup=land1['name'],icon=folium.Icon(color="red"),).add_to(map)
    folium.Marker(location=[land2['latitude'], land2['longitude']],popup=land2['name'],icon=folium.Icon(color="red"),).add_to(map)
    map.save("bono1.html")

def bonoReq2(catalog,identifier):
    map = folium.Map(location=[0,0],zoom_start=2)
    country = identifier.split('-')[0]
    info = mp.get(catalog['countries'],country)['value']
    latitude = info['CapitalLatitude']
    longitude = info['CapitalLongitude']
    folium.Marker([latitude, longitude],popup = identifier).add_to(map)
    map.save("bono2.html")

def bonoReq3(catalog,path):
    map = folium.Map(location=[0,0],zoom_start=2)
    camineishon = []
    for route in lt.iterator(path):
        vera = route['vertexA'].split('-')[0]
        verb = route['vertexB'].split('-')[0]
        
        if mp.contains(catalog['landing_points_map'],vera):
            info = mp.get(catalog['landing_points_map'],vera)['value']
            tupl = (float(info['latitude']),float(info['longitude']))
            folium.Marker(tupl, popup=vera).add_to(map)
            camineishon.append(tupl)
        else:
            info = mp.get(catalog['countries'],vera)['value']
            tupl = (float(info['CapitalLatitude']),float(info['CapitalLongitude']))
            folium.Marker(tupl, popup=vera).add_to(map)
            camineishon.append(tupl)
        
        if mp.contains(catalog['landing_points_map'],verb):
            info2 = mp.get(catalog['landing_points_map'],verb)['value']
            tupl2 = (float(info2['latitude']),float(info2['longitude']))
            folium.Marker(tupl2, popup=verb).add_to(map)
            camineishon.append(tupl2)
        else:
            info2 = mp.get(catalog['countries'],verb)['value']
            tupl2 = (float(info2['CapitalLatitude']),float(info2['CapitalLongitude']))
            folium.Marker(tupl2, popup=verb).add_to(map)
            camineishon.append(tupl2)
    

    folium.PolyLine(camineishon).add_to(map)
    map.save("bono3.html")

def bonoReq5(catalog,afected,id_landing):
    map = folium.Map(location=[0,0],zoom_start=2)
    for country in lt.iterator(afected):
        latitude = country['CapitalLatitude']
        longitude = country['CapitalLongitude']
        name = country['CountryName']
        folium.Marker((latitude,longitude), popup=name,icon=folium.Icon(color="red")).add_to(map)
    land = mp.get(catalog['landing_points_map'],id_landing)['value']
    folium.Marker((land['latitude'],land['longitude']), popup=land["name"],icon=folium.Icon(color="pink")).add_to(map)
    map.save("bono4.html")

    



    

