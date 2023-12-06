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
import math
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
    control={
        'camino':  None,
        'camino_min':None,
        }
    
    
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
    control['comparendos_gravedad']=om.newMap(cmpfunction=compare_gravedad)
    control['lista_longitud_ordenada']= lt.newList("ARRAY_LIST")
    control["lista_latitud_ordenada"]=lt.newList("ARRAY_LIST")    
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
    lt.addLast(control["lista_longitud_ordenada"],elementos[1])
    lt.addLast(control["lista_latitud"],elementos[2])
    lt.addLast(control["lista_latitud_ordenada"],elementos[2])
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
    tree_key = linea['TIPO_SERVICIO'],linea['INFRACCION'], linea['GlobalID']
    om.put(control['comparendos_gravedad'], tree_key,linea)
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
""""
def buscar_camino(control, estacion_inicial_lon, estacio_inicial_lat):
    tupla_coord_inicial = (estacion_inicial_lon,estacio_inicial_lat)
    if not om.contains(control["geograficas"],tupla_coord_inicial):
        r = "La coordenada no se encuentra"
    else: 
         id_inicio = control["geograficas"][tupla_coord_inicial]
         control['camino']= bfs.BreadhtFisrtSearch(control['malla_vial'], id_inicio)
         r = control
    return r
    
    k_v = om.get(control["geograficas"],tupla_coord_inicial)
    print(k_v)
    id_inicio = control["geograficas"][tupla_coord_inicial]
    print(id_inicio)
    #print(control["geograficas"])
    #id_inicio = control["geograficas"][tupla_coord_inicial]
    control['camino']= bfs.BreadhtFisrtSearch(control['malla_vial'], id_inicio)
    return control
    """
    

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

def calcular_distancia_min(control, tupla_coord):
    #print(control.keys())
    tabla = control['geograficas']
    lst_tabla_key = mp.keySet(tabla)
    arbol_distancias = om.newMap(omaptype='BST',cmpfunction=compare_distancia_min)
    
    for cada in lt.iterator(lst_tabla_key):
        coord_2 = cada
        #print(coord_2)
        distancia = haversine(tupla_coord,coord_2,unit=Unit.KILOMETERS, normalize=False, check=True)
        mp.put(arbol_distancias, distancia, coord_2)
    
    distancia_min = om.minKey(arbol_distancias)
    k_v_distancia_min = om.get(arbol_distancias,distancia_min)
    coordenada_aprox = me.getValue(k_v_distancia_min)
    
    return coordenada_aprox

def req_1(control, estacion_inicial_lon, estacion_inicial_lat,estacion_destino_lon, estacion_destino_lat):
    """
    Función que soluciona el requerimiento 1
    """
    tupla_coord_inicial = (estacion_inicial_lon,estacion_inicial_lat)
    tupla_coord_destino = (estacion_destino_lon,estacion_destino_lat)
    
    tabla = control["geograficas"]
    
    #id_ruta_final = lt.newList("ARRAY_LIST")
    if not om.contains(tabla,tupla_coord_inicial):
        aprox_inicial = calcular_distancia_min(control,tupla_coord_inicial)        
        id_inicio= me.getValue(mp.get(tabla,aprox_inicial))
        distancia = haversine(aprox_inicial,tupla_coord_destino,unit=Unit.KILOMETERS, normalize=False, check=True)
    
    if not om.contains(tabla,tupla_coord_destino):
        aprox_destino = calcular_distancia_min(control,tupla_coord_destino)
        id_destino = me.getValue(mp.get(tabla,aprox_destino))
        distancia = haversine(aprox_destino,tupla_coord_inicial,unit=Unit.KILOMETERS, normalize=False, check=True)
                
    else:
        id_inicio= me.getValue(mp.get(tabla,tupla_coord_inicial))
        id_destino = me.getValue(mp.get(tabla,tupla_coord_destino))
        distancia = haversine(tupla_coord_inicial,tupla_coord_destino,unit=Unit.KILOMETERS, normalize=False, check=True)
    #for cada in lt.iterator(id_ruta_final):
    control['camino']= dfs.DepthFirstSearch(control['malla_vial'], id_inicio)
    path = dfs.pathTo(control['camino'], id_destino)
    
    return distancia, path



def req_2(control, estacion_inicial_lon, estacion_inicial_lat,estacion_destino_lon, estacion_destino_lat ):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    tupla_coord_inicial = (estacion_inicial_lon,estacion_inicial_lat)
    tupla_coord_destino = (estacion_destino_lon,estacion_destino_lat)
    
    tabla = control["geograficas"]

    if not om.contains(tabla,tupla_coord_inicial):
        aprox_inicial = calcular_distancia_min(control,tupla_coord_inicial)        
        id_inicio= me.getValue(mp.get(tabla,aprox_inicial))
        distancia = haversine(aprox_inicial,tupla_coord_destino,unit=Unit.KILOMETERS, normalize=False, check=True)
    
    if not om.contains(tabla,tupla_coord_destino):
        aprox_destino = calcular_distancia_min(control,tupla_coord_destino)
        id_destino = me.getValue(mp.get(tabla,aprox_destino))
        distancia = haversine(aprox_destino,tupla_coord_inicial,unit=Unit.KILOMETERS, normalize=False, check=True)

    else:
        id_inicio= me.getValue(mp.get(tabla,tupla_coord_inicial))
        id_destino = me.getValue(mp.get(tabla,tupla_coord_destino))
        distancia = haversine(tupla_coord_inicial,tupla_coord_destino,unit=Unit.KILOMETERS, normalize=False, check=True)
        
    control['camino_min']= bfs.BreadhtFisrtSearch(control['malla_vial'], id_inicio)
    path = bfs.pathTo(control['camino_min'], id_destino)
    
    return distancia, path
    


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



def req_4(data_structs,n_comparendos):
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4
    comparendos = lt.newList("ARRAY_LIST")
    new_graph = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=n_comparendos*2,
                                              cmpfunction=compares_1)
    tree_size = om.size(data_structs['comparendos_gravedad'])
    for i in range(tree_size-n_comparendos,tree_size):
        key = om.select(data_structs['comparendos_gravedad'],i)
        k_v = om.get(data_structs['comparendos_gravedad'],key)
        comparendo = me.getValue(k_v)
        lt.addLast(comparendos, comparendo)
    
    max_key = om.maxKey(data_structs['comparendos_gravedad'])
    k_v = om.get(data_structs['comparendos_gravedad'], max_key)
    max_comparendo = me.getValue(k_v)
    lt.addLast(comparendos, max_comparendo)

    for comparendo in lt.iterator(comparendos):
        gr.insertVertex(new_graph, comparendo['VERTICES'])
    
    for vertex1 in lt.iterator(gr.vertices(new_graph)):
        for vertex2 in lt.iterator(gr.vertices(new_graph)):
            if vertex1!=vertex2 and not lt.isPresent(gr.adjacents(new_graph, vertex1),vertex2):
                dic1=me.getValue(mp.get(data_structs['vertices'],vertex1))
                dic2=me.getValue(mp.get(data_structs['vertices'],vertex2))
                dist = haversine(dic1['datos']['datos'],dic2['datos']['datos'], unit=Unit.KILOMETERS)
                gr.addEdge(new_graph,vertex1,vertex2,dist)
    
    mst_tree = prim.PrimMST(new_graph)
    network_dist = prim.weightMST(new_graph,mst_tree)
    elem = prim.edgesMST(new_graph,mst_tree)['mst']

    route_dic = {'n_nodes':0,
                     'nodes':lt.newList("ARRAY_LIST"),
                     'edges':lt.newList("ARRAY_LIST"),
                     'distance':network_dist}

    route_size = qu.size(elem)
    cycle = 0
    while route_size>0:
        edge_dic = qu.dequeue(elem)
        edge = {'Arco #':cycle, 'Vértice inicial':edge_dic['vertexA'], 'Vértice final': edge_dic['vertexB']}
        lt.addLast(route_dic['edges'], edge)
        if cycle==0:
            lt.addLast(route_dic['nodes'],edge_dic['vertexA'])
            lt.addLast(route_dic['nodes'],edge_dic['vertexB'])
        else:
            vertex_a = edge_dic['vertexA']
            vertex_b = edge_dic['vertexB']
            if not lt.isPresent(route_dic['nodes'], vertex_a):
                lt.addLast(route_dic['nodes'],vertex_a)
            if not lt.isPresent(route_dic['nodes'], vertex_b):
                lt.addLast(route_dic['nodes'],vertex_b)
        cycle+=1
        route_size-=1

    route_dic['n_nodes']=lt.size(route_dic['nodes'])
    route_dic['cost']=round(route_dic['distance']*1000000,3)
    return route_dic
    



def req_5(data_structs):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    pass


def req_6(data_structs, n_comparendos, estacion):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    comparendos = lt.newList("ARRAY_LIST")
    rutas = lt.newList("ARRAY_LIST")
    response = lt.newList("ARRAY_LIST")

    tree_size = om.size(data_structs['comparendos_gravedad'])
    for i in range(tree_size-n_comparendos,tree_size):
        key = om.select(data_structs['comparendos_gravedad'],i)
        k_v = om.get(data_structs['comparendos_gravedad'],key)
        comparendo = me.getValue(k_v)
        lt.addLast(comparendos, comparendo)
    max_key = om.maxKey(data_structs['comparendos_gravedad'])
    k_v = om.get(data_structs['comparendos_gravedad'], max_key)
    max_comparendo = me.getValue(k_v)
    lt.addLast(comparendos, max_comparendo)

    for epo in lt.iterator(data_structs['estaciones']):
        if estacion in epo['EPODESCRIP']:
            vert_epo = epo['VERTICES']
    routes = djk.Dijkstra(data_structs['malla_vial'],vert_epo)
    
    for comparendo in lt.iterator(comparendos):
        path = djk.pathTo(routes, comparendo['VERTICES'])
        lt.addLast(rutas, path)
    
    for elem in lt.iterator(rutas):
        route_dic = {'n_nodes':0,
                     'nodes':lt.newList("ARRAY_LIST"),
                     'edges':lt.newList("ARRAY_LIST"),
                     'distance':0}
        route_size = st.size(elem)
        cycle = 0
        while route_size>0:
            edge_dic = st.pop(elem)
            route_dic['distance']+=edge_dic['weight']
            edge = f"{edge_dic['vertexA']} - {edge_dic['vertexB']}"
            lt.addLast(route_dic['edges'], edge)
            if cycle==0:
                lt.addLast(route_dic['nodes'],edge_dic['vertexA'])
                lt.addLast(route_dic['nodes'],edge_dic['vertexB'])
            else:
                lt.addLast(route_dic['nodes'],edge_dic['vertexB'])
            cycle+=1
            route_size-=1
        route_dic['n_nodes']=lt.size(route_dic['nodes'])
        lt.addLast(response, route_dic)

    return response
def req_7(data_structs, s_latitude, s_longitude, e_latitude, e_longitude):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7

    latitudes = data_structs['lista_latitud_ordenada']
    longitudes = data_structs['lista_longitud_ordenada']

    latitudes_g= data_structs['lista_latitud']
    longitudes_g = data_structs['lista_longitud']

    min_lat = float(lt.firstElement(latitudes))
    max_lat = float(lt.lastElement(latitudes))
    min_long = float(lt.firstElement(longitudes))
    max_long = float(lt.lastElement(longitudes))

    #print(min_lat, max_lat, min_long, max_long)
    if min_lat<=float(s_latitude)<=max_lat and min_long<=float(s_longitude)<=max_long and min_lat<=float(e_latitude)<=max_lat and min_long<=float(e_longitude)<=max_long:
        node_s = None
        minimum_s = math.inf

        node_e = None
        minimum_e = math.inf

        for i in range(1,lt.size(latitudes)+1):
            latitud = float(lt.getElement(latitudes_g,i))
            longitud = float(lt.getElement(longitudes_g, i))
            dist_s = haversine((s_latitude,s_longitude), (latitud,longitud),unit=Unit.KILOMETERS)
            dist_e = haversine((e_latitude,e_longitude), (latitud,longitud), unit=Unit.KILOMETERS)
            
            if node_s == None or dist_s<minimum_s:
                node_s = i
                minimum_s = dist_s
            
            if node_e == None or dist_e<minimum_e:
                node_e = i
                minimum_e = dist_e
        
        routes = djk.Dijkstra(data_structs['malla_vial_comparendos'],str(node_s))
        route = djk.pathTo(routes, str(node_e))

        route_dic = {'n_nodes':0,
                        'nodes':lt.newList("ARRAY_LIST"),
                        'edges':lt.newList("ARRAY_LIST"),
                        'infracciones':0,
                        'distance':0}
        route_size = st.size(route)
        cycle = 0
        while route_size>0:
            edge_dic = st.pop(route)
            edge_dist = gr.getEdge(data_structs['malla_vial'], edge_dic['vertexA'], edge_dic['vertexB'])
            route_dic['distance']+=edge_dist['weight']
            route_dic['infracciones']+=edge_dic['weight']
            edge = f"{edge_dic['vertexA']} - {edge_dic['vertexB']}"
            lt.addLast(route_dic['edges'], edge)
            if cycle==0:
                lt.addLast(route_dic['nodes'],edge_dic['vertexA'])
                lt.addLast(route_dic['nodes'],edge_dic['vertexB'])
            else:
                lt.addLast(route_dic['nodes'],edge_dic['vertexB'])
            cycle+=1
            route_size-=1
        route_dic['n_nodes']=lt.size(route_dic['nodes'])

        return route_dic
    else: 
        return None
    
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

def compare_gravedad(comparendo, comparendo2):
    servicio1= comparendo[0]
    servicio2 = comparendo2[0]
    if servicio1=='Público':
        weight1= 3
    elif servicio1=='Oficial':
        weight1=2
    else:
        weight1= 1
    
    if servicio2=='Público':
        weight2= 3
    elif servicio2=='Oficial':
        weight2=2
    else:
        weight2= 1
    
    if weight1>weight2:
        return 1
    
    elif weight1==weight2 and comparendo[1]>comparendo2[1]:
        return 1
    
    elif weight1==weight2 and comparendo[1]==comparendo2[1] and comparendo[2]>comparendo2[2]:
        return 1

    elif weight1==weight2 and comparendo[1]==comparendo2[1] and comparendo[2]==comparendo2[2]:
        return 0
    else:
        return -1
def sort_criteria_lat_long(data_1, data_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    #TODO: Crear función comparadora para ordenar
    if float(data_1)<float(data_2):
        return True
    return False

def compare_distancia_min(data_1,data_2):
    
    if data_1 > data_2:
        return 1
    elif data_1 == data_2:
        return 0
    else:
        return -1
    
def sort_lat_long(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    merg.sort(data_structs['lista_longitud_ordenada'], sort_criteria_lat_long)
    merg.sort(data_structs['lista_latitud_ordenada'], sort_criteria_lat_long)
