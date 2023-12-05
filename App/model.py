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
    control["geograficas"]= mp.newMap(maptype="PROBING",numelements=805249)
    control["vertices"]= mp.newMap(maptype="PROBING",numelements=805249)
    control["arcos"]= mp.newMap(maptype="PROBING")
    control["malla_vial_comparendos"]=  gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=14000,
                                              cmpfunction=compares_1)
    control["vertices_list"]= lt.newList("ARRAY_LIST")
    control["arcos_list"]= lt.newList("ARRAY_LIST")
    control["lista_longitud"]= lt.newList("ARRAY_LIST")
    control["lista_latitud"]=lt.newList("ARRAY_LIST")
    control["estaciones"]= lt.newList("ARRAY_LIST")
    control["comparendos"]= lt.newList("ARRAY_LIST")
    control["localidad"]= mp.newMap(maptype="PROBING",numelements=805249)

    return control
    #TODO: Inicializar las estructuras de datos
    pass


# Funciones para agregar informacion al modelo
def add_vertices(linea, control):
    #añade cada vertice y a su vez crea un vertice con llave el id del vertice
    mapa_geo= control["geograficas"]
    mapa_vertices= control["vertices"]
    elementos = linea.split(',')
    lista= {"datos":(float(elementos[1]),float(elementos[2])),"id":elementos[0]}
    mp.put(mapa_vertices,elementos[0],{"datos":lista,"estaciones": lt.newList("ARRAY_LIST"),"comparendos":lt.newList("ARRAY_LIST"),"cantidad":0})
    lt.addLast(control["lista_longitud"],elementos[1])
    lt.addLast(control["lista_latitud"],elementos[2])
    gr.insertVertex(control["malla_vial"], elementos[0])
    gr.insertVertex(control["malla_vial_comparendos"], elementos[0])
    mp.put(mapa_geo,(float(elementos[1]),float(elementos[2])),elementos[0])
    lt.addLast(control["vertices_list"],{"id":elementos[0],"Latitud":elementos[1],"Longitud":elementos[2]})

def añadir_comparendos(linea,control):
    id= linea["VERTICES"]
    peso= me.getValue(mp.get(control["vertices"],id))["cantidad"]
    peso+=1
    comparendos= control["comparendos"]
    lt.addLast(comparendos,linea)
    cada=linea["geometry"]
    mapa= me.getValue(mp.get(control["vertices"],id))["comparendos"]
    lt.addLast(mapa,linea)
    añadir_localidad(linea,control, id)

def formato_comparendos(linea):
    control={}
    control["OBJECTID"]=linea["OBJECTID"]
    control[""]
    return control

def añadir_localidad(linea,control,id):
    mapa= control["localidad"]
    localidad= linea["LOCALIDAD"]
    entry= mp.get(mapa,localidad)
    if entry:
        dataentry= me.getValue(entry)
    else:
        dataentry= {"vertices":lt.newList("ARRAY_LIST"),"grafo": gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=228047,
                                              cmpfunction=compares_1),"lista":lt.newList("ARRAY_LIST")}
        mp.put(mapa,localidad,dataentry)
    l= lt.isPresent(dataentry["vertices"],id)
    if l==0:
        lt.addLast(dataentry["vertices"],id)
        lt.addLast(dataentry["lista"],{"id":id,"total":1})
    ele= lt.getElement(dataentry["lista"],l)
    ele["total"]+=1
    gr.insertVertex(dataentry["grafo"], id)



def añadir_estaciones(linea,control):
    id= linea["VERTICES"]
    peso= me.getValue(mp.get(control["vertices"],id))["estaciones"]
    lt.addLast(peso,linea)
    estaciones= control["estaciones"]
    lt.addLast(estaciones,linea)


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
    lt.addLast(control["arcos_list"],{"id":elementos[0],"adyacentes":lista})
    mp.put(mapa_vertices,elementos[0],lista)

def add_arcos_compa(linea,control):
    grafo= control["malla_vial_comparendos"]
    elementos = linea.rstrip().split(" ")
    for cada in elementos:
        if cada != elementos[0]:
            cantidad= me.getValue(mp.get(control["vertices"],cada))["cantidad"]
            gr.addEdge(grafo,elementos[0],cada,cantidad)

def get_data_5(data_structs,tamano):
    """
    Retorna un dato a partir de su ID
    """
    #TODO: Crear la función para obtener un dato de una lista   
    resultados = lt.newList("ARRAY_LIST")
    lt.addFirst(resultados,lt.firstElement(data_structs))
    for b in range(2,6):
        p = lt.getElement(data_structs, b)
        lt.addLast(resultados, p)
    for b in range (0,5):
        p = lt.getElement(data_structs, (tamano-4+b))
        lt.addLast(resultados, p)
    return resultados
def total_vertices(control):
    grafo=control["malla_vial"]
    vertices=gr.numVertices(grafo)
    arcos= gr.numEdges(grafo)
    return vertices,arcos

def limites(control):
    longitud= control["lista_longitud"]
    latitud= control["lista_longitud"]
    or_lon= merg.sort(longitud,orden_l)
    or_la=merg.sort(latitud,orden_l)
    max_lon= lt.firstElement(or_lon)
    min_lon= lt.lastElement(or_lon)
    max_lat= lt.firstElement(or_la)
    min_lat= lt.lastElement(or_la)
    return max_lon,min_lon,max_lat,min_lat


def orden_l(dato1,dato2):
    if dato1>dato2:
        return True
    else:
        return False

    




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
    return lt.size(data_structs)
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


def req_3(control,localidad,num):
    """
    Función que soluciona el requerimiento 3
    """
    grafo_final= gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=228047,
                                              cmpfunction=compares_1)
    mapa_arcos= control["arcos"]
    mapa_localidad=me.getValue(mp.get(control["localidad"],localidad))
    grafo= mapa_localidad["grafo"]
    lista_vertices= mapa_localidad["vertices"]
    for cada in lt.iterator(lista_vertices):
        arcos= me.getValue(mp.get(mapa_arcos,cada))
        for arco in lt.iterator(arcos):
            i=lt.isPresent(lista_vertices,arco)
            if i!=0:
                direc_p= me.getValue(mp.get(control["vertices"],cada))["datos"]["datos"]
                direc_siguiente= me.getValue(mp.get(control["vertices"],arco))["datos"]["datos"]
                distancia=haversine(direc_p,direc_siguiente,unit=Unit.KILOMETERS)
                gr.addEdge(grafo,arco,cada,distancia)
                gr.addEdge(grafo,cada,arco,distancia)
                
    lista= mapa_localidad["lista"]
    ordenada= merg.sort(lista,comparacion_req3)
    ordenadas=lt.subList(ordenada,1,num)

    lista_de_los_vertices=lt.newList("ARRAY_LIST")
    for ver in lt.iterator(ordenadas):
        gr.insertVertex(grafo_final,ver["id"])
        lt.addLast(lista_de_los_vertices,ver["id"])
    for cada in lt.iterator(lista_de_los_vertices):
        elemento=djk.Dijkstra(grafo,cada)
        i=lt.isPresent(lista_de_los_vertices,cada)
        for numero in range(i+1,num+1):
            vertice=lt.getElement(lista_de_los_vertices,numero)
            peso= djk.distTo(elemento,vertice)
            gr.addEdge(grafo_final,vertice,cada,peso)
    mst=prim.PrimMST(grafo_final)
    kilometros= prim.weightMST(grafo_final,mst)
    elem=prim.edgesMST(grafo_final,mst)["mst"]
    elem_size= qu.size(elem)
    vertices_fin= lt.newList("ARRAY_LIST")
    arcos=lt.newList("ARRAY_LIST")
    while elem_size>0:
        elemento= qu.dequeue(elem)
        lt.addLast(arcos,{"VerticeA":elemento["vertexA"],"VerticeB":elemento["vertexB"]})
        a=lt.isPresent(vertices_fin,elemento["vertexA"])
        b=lt.isPresent(vertices_fin,elemento["vertexB"])
        if a==0:
            lt.addLast(vertices_fin,elemento["vertexA"])
        if b==0:
            lt.addLast(vertices_fin,elemento["vertexB"])
        elem_size-=1
    costo= kilometros*1000000
    total= lt.size(vertices_fin)
    return total,vertices_fin,arcos,kilometros,costo

def comparacion_req3(dato1,dato2):
    if dato1["total"]>dato2["total"]:
        return True
    else:
        return False
    
def req_3_auxiliar(control,localidad,num):
    grafo_final= gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=228047,
                                              cmpfunction=compares_1)
    mapa_localidad=me.getValue(mp.get(control["localidad"],localidad))
    lista= mapa_localidad["lista"]
    ordenada= merg.sort(lista,comparacion_req3)
    ordenadas=lt.subList(ordenada,1,num)
    lista_de_los_vertices=lt.newList("ARRAY_LIST")
    for ver in lt.iterator(ordenadas):
        gr.insertVertex(grafo_final,ver["id"])
        lt.addLast(lista_de_los_vertices,ver["id"])

    for cada in lt.iterator(lista_de_los_vertices):
        i=lt.isPresent(lista_de_los_vertices,cada)
        for numero in range(i+1,num+1):
            vertice=lt.getElement(lista_de_los_vertices,numero)
            direc_p= me.getValue(mp.get(control["vertices"],cada))["datos"]["datos"]
            direc_siguiente= me.getValue(mp.get(control["vertices"],vertice))["datos"]["datos"]
            distancia=haversine(direc_p,direc_siguiente,unit=Unit.KILOMETERS)
            gr.addEdge(grafo_final,vertice,cada,distancia)
    mst=prim.PrimMST(grafo_final)
    kilometros= prim.weightMST(grafo_final,mst)
    elem=prim.edgesMST(grafo_final,mst)["mst"]
    elem_size= qu.size(elem)
    vertices_fin= lt.newList("ARRAY_LIST")
    arcos=lt.newList("ARRAY_LIST")
    while elem_size>0:
        elemento= qu.dequeue(elem)
        lt.addLast(arcos,{"VerticeA":elemento["vertexA"],"VerticeB":elemento["vertexB"]})
        a=lt.isPresent(vertices_fin,elemento["vertexA"])
        b=lt.isPresent(vertices_fin,elemento["vertexB"])
        if a==0:
            lt.addLast(vertices_fin,elemento["vertexA"])
        if b==0:
            lt.addLast(vertices_fin,elemento["vertexB"])
        elem_size-=1
    costo= kilometros*1000000
    total= lt.size(vertices_fin)
    return total,vertices_fin,arcos,kilometros,costo



def req_4(control,localidad):
    """
    Función que soluciona el requerimiento 4
    """
    


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
