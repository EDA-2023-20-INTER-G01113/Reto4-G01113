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
import time
import csv
import tracemalloc
import json

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
    """
    Crea una instancia del modelo
    """
    control= model.new_data_structs()
    return control
    #TODO: Llamar la función del modelo que crea las estructuras de datos
    pass


# Funciones para la carga de datos

def load_data(control):
    """
    Carga los datos del reto
    """  
    archivo_vertices = open(cf.data_dir + "bogota_vertices.txt","r")
    for linea in archivo_vertices:
        model.add_vertices(linea,control)
    
    file = "comparendos_2019_bogota_vertices.csv"
    file_name = cf.data_dir  + file
    input_file = csv.DictReader(open(file_name, encoding='utf-8'))
    for comparendo in input_file:
        model.añadir_comparendos(comparendo,control)

    file = "estacionpolicia_bogota_vertices.csv"
    file_name = cf.data_dir  + file
    input_file = csv.DictReader(open(file_name, encoding='utf-8'))
    for estacion in input_file:
        model.añadir_estaciones(estacion,control)

    archivo_arcos= open(cf.data_dir + "bogota_arcos.txt","r")
    for arco in archivo_arcos:
        if "#" not in arco:
            model.add_arcos(arco,control)
            model.add_arcos_compa(arco,control)
    total_comparendos=model.data_size(control["comparendos"])
    comparendos= model.get_data_5(control["comparendos"],total_comparendos)
    total_estaciones= model.data_size(control["estaciones"])
    estaciones= model.get_data_5(control["estaciones"],total_estaciones)
    vertices,arcos= model.total_vertices(control)
    arcos_t= model.data_size(control["arcos_list"])
    cinco_ver= model.get_data_5(control["vertices_list"],vertices)
    cinco_arcos=model.get_data_5(control["arcos_list"],arcos_t)
    max_lon,min_lon,max_lat,min_lat= model.limites(control)
    model.sort_lat_long(control)
    return control, total_comparendos,comparendos,total_estaciones,estaciones,vertices,cinco_ver,arcos,cinco_arcos,max_lon,min_lon,max_lat,min_lat


# Funciones de ordenamiento


def sort(control):
    """
    Ordena los datos del modelo
    """
    #TODO: Llamar la función del modelo para ordenar los datos
    pass


# Funciones de consulta sobre el catálogo

def get_data(control, id):
    """
    Retorna un dato por su ID.
    """
    #TODO: Llamar la función del modelo para obtener un dato
    pass


def req_1(control, estacion_inicial_lon, estacion_inicial_lat,estacion_destino_lon, estacion_destino_lat):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    start_time = get_time()
    distancia,path = model.req_1(control, estacion_inicial_lon, estacion_inicial_lat,estacion_destino_lon, estacion_destino_lat)
    end_time = get_time()
    delta_times = delta_time(start_time, end_time)
    return distancia,path, delta_times

def req_2(control,estacion_inicial_lon, estacion_inicial_lat,estacion_destino_lon, estacion_destino_lat):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    start_time = get_time()
    distancia, path= model.req_2(control,estacion_inicial_lon, estacion_inicial_lat,estacion_destino_lon, estacion_destino_lat) 
    end_time = get_time()
    delta_times = delta_time(start_time, end_time)
    return distancia, path, delta_times

def req_3(control,num,localidad,memoria):
    """
    Retorna el resultado del requerimiento 3
    """
    start_time = get_time()
    if memoria:
        tracemalloc.start()
        start_memory = get_memory() 
    total,vertices_fin,arcos,kilometros,costo=model.req_3_auxiliar(control,localidad,num)
    if memoria:
        stop_memory = get_memory()
        tracemalloc.stop()
        delta_m = delta_memory(stop_memory, start_memory)
    else:
        delta_m = None

    end_time = get_time()
    delta_times = delta_time(start_time, end_time)
    return total,vertices_fin,arcos,kilometros,costo,delta_times,delta_m

    # TODO: Modificar el requerimiento 3
    pass


def req_4(control, memflag):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    
    n_comparendos = int(input("Por favor ingrese el número de comparendos más graves que quiere analizar: "))

    start_time = get_time()

    if memflag:
        tracemalloc.start()
        start_memory = get_memory() 

    response = model.req_4(control, n_comparendos)

    if memflag:
        stop_memory = get_memory()
        tracemalloc.stop()
        delta_m = delta_memory(stop_memory, start_memory)
    else:
        delta_m = None

    end_time = get_time()
    diff_time = delta_time(start_time, end_time)
    return response, diff_time, delta_m



def req_5(control):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

def req_6(control, memflag):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    n_comparendos = int(input("Por favor ingrese el número de comparendos más graves que desea atender: "))
    estacion = input("Por favor ingrese la estación desde la cual desea calcular las rutas: ")
    start_time = get_time()

    if memflag:
        tracemalloc.start()
        start_memory = get_memory() 

    paths = model.req_6(control, n_comparendos, estacion)

    if memflag:
        stop_memory = get_memory()
        tracemalloc.stop()
        delta_m = delta_memory(stop_memory, start_memory)
    else:
        delta_m = None

    end_time = get_time()
    diff_time = delta_time(start_time, end_time)
    return paths, diff_time, delta_m


def req_7(control, memflag):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    s_latitude = float(input("Ingrese la latitud del punto inicial: "))
    s_longitude = float(input("Ingrese la longitud del punto inicial: "))
    e_latitude = float(input("Ingrese la latitud del punto final: "))
    e_longitude = float(input("Ingrese la longitud del punto final: "))
    start_time = get_time()

    if memflag:
        tracemalloc.start()
        start_memory = get_memory() 

    results = model.req_7(control, s_latitude, s_longitude, e_latitude, e_longitude)

    if memflag:
        stop_memory = get_memory()
        tracemalloc.stop()
        delta_m = delta_memory(stop_memory, start_memory)
    else:
        delta_m = None

    
    end_time = get_time()
    diff_time = delta_time(start_time, end_time)

    return results, diff_time, delta_m

def req_8(control):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    pass


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed

def get_memory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def delta_memory(stop_memory, start_memory):
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
