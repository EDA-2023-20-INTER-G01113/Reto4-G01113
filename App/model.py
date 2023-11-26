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
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.ADT import minpq as mpq
from DISClib.ADT import indexminpq as impq
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import graph as gr
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import bellmanford as bf
from DISClib.Algorithms.Graphs import bfs
from DISClib.Algorithms.Graphs import dfs
from DISClib.Algorithms.Graphs import prim
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import selectionsort as se
from DISClib.Algorithms.Sorting import mergesort as merg
from DISClib.Algorithms.Sorting import quicksort as quk
assert cf
from haversine import haversine, Unit
import json
"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Construccion de modelos


def new_data_structs():
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    control={}
    control["malla_vial"]=  gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=14000,
                                              cmpfunction=compares_1)
    control["vertices"]= mp.newMap(maptype="PROBING",numelements=805249)
    control["arcos"]= mp.newMap(maptype="PROBING")
    control["malla_vial_comparendos"]=  gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=14000,
                                              cmpfunction=compares_1)
    control["lista_longitud"]= lt.newList("ARRAY_LIST")
    control["lista_latitud"]=lt.newList("ARRAY_LIST")
    control["estaciones"]= mp.newMap(maptype="PROBING")
    control["comparendos"]= mp.newMap(maptype="PROBING")

    return control
    #TODO: Inicializar las estructuras de datos
    pass


# Funciones para agregar informacion al modelo
def add_vertices(linea, control):
    #añade cada vertice y a su vez crea un vertice con llave el id del vertice
    mapa_vertices= control["vertices"]
    elementos = linea.split(',')
    lista= {"datos":(float(elementos[1]),float(elementos[2])),"id":elementos[0]}
    mp.put(mapa_vertices,elementos[0],{"datos":lista,"estaciones":mp.newMap(maptype="PROBING"),"comparendos":mp.newMap(maptype="PROBING")})
    lt.addLast(control["lista_longitud"],elementos[1])
    lt.addLast(control["lista_latitud"],elementos[2])
    gr.insertVertex(control["malla_vial"], elementos[0])
    gr.insertVertex(control["malla_vial_comparendos"], elementos[0])

def add_arcos(linea, control):
    grafo= control["malla_vial"]
    mapa_vertices= control["arcos"]  
    elementos = linea.rstrip().split(" ")
    lista=lt.newList("ARRAY_LIST")
    direc_p= me.getValue(mp.get(control["vertices"],elementos[0]))["datos"]["datos"]
    for cada in elementos:
        if cada != elementos[0]:
            direc_siguiente= me.getValue(mp.get(control["vertices"],cada))["datos"]["datos"] 
            distancia=haversine(direc_p,direc_siguiente,unit=Unit.KILOMETERS)
            gr.addEdge(grafo,elementos[0],cada,distancia)
            lt.addLast(lista,cada)
    mp.put(mapa_vertices,elementos[0],lista)

def add_arcos_compa(linea,control):
    grafo= control["malla_vial_comparendos"]
    elementos = linea.rstrip().split(" ")
    for cada in elementos:
        if cada != elementos[0]:
            mapa_de_vertice= me.getValue(mp.get(control["vertices"],cada))["comparendos"]
            cantidad= mp.size(mapa_de_vertice)
            gr.addEdge(grafo,elementos[0],cada,cantidad)

    

def add_estaciones(linea,control):
    mapa= control["estaciones"]
    dimensiones= linea["geometry"]["coordinates"]
    dime= ((dimensiones[0]),(dimensiones[1]))
    lista= mp.valueSet(control["vertices"])
    for cada in lt.iterator(lista):
        dime_2= cada["datos"]["datos"]
        distancia=haversine(dime,dime_2,unit=Unit.KILOMETERS)
        entry = mp.get(mapa, linea["id"])
        if entry is None:
            datentry = om.newMap("BST")
            mp.put(mapa,linea["id"], datentry)
        else:
            datentry = me.getValue(entry)
        om.put(datentry,distancia,cada["datos"]["id"])
    minimo= om.minKey(me.getValue(mp.get(mapa,linea["id"])))
    valor= me.getValue(om.get(me.getValue(mp.get(mapa,linea["id"])),minimo))
    estruct= estructura_estacion(linea)
    mapa_de_vertice= me.getValue(mp.get(control["vertices"],valor))["estaciones"]
    mp.put(mapa_de_vertice,valor,estruct)

def estructura_estacion(estacion):
    control={}
    control["type"]=estacion["type"]
    control["id"]= estacion["id"]
    control["geometry"]= estacion["geometry"]
    return control

def add_comparendos(linea,control):
    mapa=control["comparendos"]
    dimensiones= linea["geometry"]["coordinates"]
    dime= ((dimensiones[0]),(dimensiones[1]))
    lista= mp.valueSet(control["vertices"])
    minimo = None
    for cada in lt.iterator(lista):
        dime_2= cada["datos"]["datos"]
        distancia=haversine(dime,dime_2,unit=Unit.KILOMETERS)
        """ entry = mp.get(mapa, linea["properties"]["OBJECTID"])
        if entry is None:
            datentry = om.newMap("BST")
            mp.put(mapa,linea["properties"]["OBJECTID"], datentry)
        else:
            datentry = me.getValue(entry) """
        if minimo == None or distancia<minimo:
            minimo = distancia
            valor= cada['datos']['id']
        """ om.put(datentry,distancia,cada["datos"]["id"])
    minimo= om.minKey(me.getValue(mp.get(mapa,linea["properties"]["OBJECTID"])))
    valor= me.getValue(om.get(me.getValue(mp.get(mapa,linea["properties"]["OBJECTID"])),minimo)) """
    estruct= estructura_comparendo(linea)
    mapa_de_vertice= me.getValue(mp.get(control["vertices"],valor))["comparendos"]
    mp.put(mapa_de_vertice,valor,estruct)
    print(minimo)

def estructura_comparendo(comparendo):
    control={}
    control["type"]=comparendo["type"]
    control["properties"]={"OBJECTID":comparendo["properties"]["OBJECTID"]}
    control["geometry"]= comparendo["geometry"]
    return control

    




def add_data(data_structs, data):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    pass


# Funciones para creacion de datos

def new_data(id, info):
    """
    Crea una nueva estructura para modelar los datos
    """
    #TODO: Crear la función para estructurar los datos
    pass


# Funciones de consulta

def get_data(data_structs, id):
    """
    Retorna un dato a partir de su ID
    """
    #TODO: Crear la función para obtener un dato de una lista
    pass


def data_size(data_structs):
    """
    Retorna el tamaño de la lista de datos
    """
    #TODO: Crear la función para obtener el tamaño de una lista
    pass


def req_1(data_structs):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1
    pass


def req_2(data_structs):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    pass


def req_3(data_structs):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
    pass


def req_4(data_structs):
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4
    pass


def req_5(data_structs):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    pass


def req_6(data_structs):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    pass


def req_7(data_structs):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    pass


def req_8(data_structs):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    pass


# Funciones utilizadas para comparar elementos dentro de una lista

def compare(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    #TODO: Crear función comparadora de la lista
    pass

# Funciones de ordenamiento
def compares_1(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1


def sort_criteria(data_1, data_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    #TODO: Crear función comparadora para ordenar
    pass


def sort(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    pass
