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

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo

def initCatalog():
    return model.newCatalog()

# Funciones para la carga de datos

def loadData(catalog,connections,landing_points,countries):

    landing_points = cf.data_dir + landing_points
    input_file_landing = csv.DictReader(open(landing_points, encoding='utf-8-sig'))

    for landing_point in input_file_landing:
        model.addLandingPoint(catalog, landing_point)
        model.addMarinePoint(catalog, landing_point)
      

    connections = cf.data_dir + connections
    input_file_cable = csv.DictReader(open(connections, encoding='utf-8-sig'))
    lastcable = None

    for cable in input_file_cable:
        model.addCable(catalog, cable)
        model.addMarineCable(catalog,cable)
        model.addCableName(catalog,cable)

    #model.addLandingConnection(catalog)

    countries = cf.data_dir + countries
    input_file_countries = csv.DictReader(open(countries, encoding='utf-8-sig'))

    for country in input_file_countries:
        if country["CountryName"]!="":
            model.addCountryPoint(catalog, country)
            model.addCountry(catalog,country)
            model.addCountryConnections(catalog,country)
            
    model.addLandingConnection(catalog)
    model.secondGraph(catalog)
           

# Funciones de cracks

def SCC(graph):
    return model.SCC(graph)

def areConnected(landing1,landing2,graph):
    return model.areConnected(landing1,landing2,graph)

def dijsktra(graph,source):
    return model.dijsktra(graph,source)

def path(dijsktra,countryB):
    return model.path(dijsktra,countryB)

def mst(graph):
    return model.mst(graph)

def weight(graph,mst):
    return model.weight(graph,mst)

# Funciones de consulta sobre el catálogo

def graphSize(graph):
    return model.graphSize(graph)

def connectionsSize(graph):
    return model.connectionsSize(graph)
def countrySize(catalog):
    return model.countrySize(catalog)

def lastCountry(catalog):
    return model.lastCountry(catalog)

def firstLandingPoint(catalog):
    return model.firstLandingPoint(catalog)

def mapSize(map):
    return model.mapSize(map)

def findLandingPoint(catalog,landingpoint):
    return model.findLandingPoint(catalog,landingpoint)

def findInterconnectionCables(catalog):
    return model.findInterconnectionCables(catalog)

def getCapital(country,catalog):
    return model.getCapital(country,catalog)

def landingCables(catalog,id_landing):
    return model.landingCables(catalog,id_landing)

def afected(catalog,cables_list):
    return model.afected(catalog,cables_list)

def getCableName(catalog,cable_name):
    return model.getCableName(catalog,cable_name)

#Funciones para que Juan Sebastian salga de nuestro pensamiento

def wideOfBand(catalog,landing_list,country):
    return model.wideOfBand(catalog,landing_list,country)

def tupapi(catalog,ip1,ip2):
    return model.tupapi(catalog,ip1,ip2)

#Funciones para bonos

def bonoReq1(catalog,id_landing1, id_landing2):
    model.bonoReq1(catalog,id_landing1, id_landing2)

def bonoReq3(catalog,path):
    model.bonoReq3(catalog,path)

def bonoReq5(catalog,afected,id_landing):
    model.bonoReq5(catalog,afected,id_landing)
