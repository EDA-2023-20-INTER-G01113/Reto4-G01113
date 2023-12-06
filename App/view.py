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
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.ADT import graph as gr
from DISClib.DataStructures import mapentry as me
assert cf
from tabulate import tabulate
import traceback
import threading

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def new_controller():
    """
        Se crea una instancia del controlador
    """
    control = controller.new_controller()
    return control
    #TODO: Llamar la función del controlador donde se crean las estructuras de datos
    pass


def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Ejecutar Requerimiento 1")
    print("3- Ejecutar Requerimiento 2")
    print("4- Ejecutar Requerimiento 3")
    print("5- Ejecutar Requerimiento 4")
    print("6- Ejecutar Requerimiento 5")
    print("7- Ejecutar Requerimiento 6")
    print("8- Ejecutar Requerimiento 7")
    print("9- Ejecutar Requerimiento 8")
    print("0- Salir")


def load_data(control):
    """
    Carga los datos
    """
    control, total_comparendos,comparendos,total_estaciones,estaciones,vertices,cinco_ver,arcos,cinco_arcos,max_lon,min_lon,max_lat,min_lat= controller.load_data(control)
    print("El total de comparendos es de: "+ str(total_comparendos))
    print(comparendos)
    print("El total de estaciones es de: "+str(total_estaciones))
    print(estaciones)
    print("El total de vertices cargados en la aplicacion es de : "+str(vertices))
    print(cinco_ver)
    print("El total de arcos cargados en la aplicacion es de : "+str(arcos))
    print(cinco_arcos)
    print("Los limites de la zona geografica son: ")
    print("El máximo de longitud es: "+str(max_lon))
    print("El minimo de longitud es: "+str(min_lon))
    print("El máximo de latitud es: "+str(max_lat))
    print("El minimo de latitud es: "+str(min_lat))
    return control
    #TODO: Realizar la carga de datos
    pass


def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(control, estacion_inicial_lon, estacion_inicial_lat, estacion_destino_lon, estacion_destino_lat):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """

    # TODO: Imprimir el resultado del requerimiento 1
    distancia, path, delta_times= controller.req_1(control, estacion_inicial_lon, estacion_inicial_lat, estacion_destino_lon, estacion_destino_lat)
    if path is not None:
        size = st.size(path)
        print(f'El camino tiene una longitud de: {size}')
        print(f"La distancia entre las dos coordenadas: {distancia}")
        print(f'Tiempo transcurrido: {delta_times} ms.')
        print("IDs de los nodos incluidos: ")
        response = ''
        while size>0:
            elem = st.pop(path)
            response+=f'{elem}, '
            size-=1
        print(response.strip()[:-1])
    else:
        print('No hay camino')

def print_req_2(control, estacion_inicial_lon,estacion_inicial_lat, estacion_destino_lon, estacion_destino_lat):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    distancia, path, delta_times = controller.req_1(control, estacion_inicial_lon, estacion_inicial_lat, estacion_destino_lon, estacion_destino_lat)
    if path is not None:
        size = st.size(path)
        print(f'El camino tiene una longitud de: {size}')
        print(f"La distancia entre las dos coordenadas: {distancia}")
        print(f'Tiempo transcurrido: {delta_times} ms.')
        print("IDs de los nodos incluidos: ")
        response=''
        while size>0:
            elem = st.pop(path)
            response+=f'{elem}, '
            size-=1
        print(response.strip()[:-1])
    else:
        print('No hay camino')

def print_req_3(control,num,localidad,memoria):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    total,vertices,arcos,kilometros,costo,delta_times,meria=controller.req_3(control,num,localidad,memoria)
    print("El tiempo de ejecución fue de :"+str(delta_times))
    print("El total de vertices en la red es de: "+str(total))
    print("Los vertices incluidos son: "+str(vertices))
    print("los arcos incluidos son: "+str(arcos))
    print("Cantidad de kilometros de fibra óptica: "+str(kilometros))
    print("El costo total es de: "+str(costo))
    print("memoria: "+str(meria))
    # TODO: Imprimir el resultado del requerimiento 3
    pass


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    memflag = input("Ingrese si desea recibir datos de memoria (S/N): ")
    if memflag=='S':
        memflag = True
    else:
        memflag = False

    response, diff_time, delta_m = controller.req_4(control, memflag)
    print('\n')
    print(f'Tiempo que tardó el algoritmo: {diff_time}')
    if delta_m:
        print(f'Espacio usado en  memoria: {round(delta_m,3)} [kB]')
    print('\n')
    print(f'Distancia total de la red (km): {round(response["distance"],3)}')
    print(f'Costo total de la red de fibra óptica: {response["cost"]} COP')
    print(f'Número total de nodos: {response["n_nodes"]}\n')


    node_str=''
    for node in lt.iterator(response['nodes']):
        node_str+=f'{node},'
    print(f'{"-"*10} IDs de los nodos incluidos {"-"*10}\n')
    print(node_str[:-1]) 
    print('\n')
    elems = [x for x in lt.iterator(response['edges'])]
    print(f'{"-"*10} Arcos incluídos {"-"*10}\n')
    print(f'# corresponde a la posición de un arco en la ruta.\n')
    print(f'{tabulate(elems,headers="keys",tablefmt="grid")}')

def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    memflag = input("Ingrese si desea recibir datos de memoria (S/N): ")
    if memflag=='S':
        memflag = True
    else:
        memflag = False
    paths, diff_time, delta_m = controller.req_6(control, memflag)
    print('\n')
    print(f'Tiempo que tardó el algoritmo: {diff_time}')
    if delta_m:
        print(f'Espacio usado en  memoria: {round(delta_m,3)} [kB]')
    n_path = 1
    for path in lt.iterator(paths):
        print('\n')
        print(f'{"-"*10} Comparendo #{n_path} {"-"*10}\n')
        print(f'Distancia total del camino (km): {path["distance"]}')
        print(f'Número total de nodos: {path["n_nodes"]}\n')

        node_str=''
        for node in lt.iterator(path['nodes']):
            node_str+=f'{node},'
        print(f'{"-"*10} IDs de los nodos incluidos {"-"*10}\n')
        print(node_str[:-1]) 
        print('\n')
        print(f'{"-"*10} Arcos incluídos {"-"*10}\n')
        edges_str=''
        for edge in lt.iterator(path['edges']):
            edges_str+=f'{edge}, '
        print(edges_str.strip()[:-1])
        n_path+=1


def print_req_7(control):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    memflag = input("Ingrese si desea recibir datos de memoria (S/N): ")
    if memflag=='S':
        memflag = True
    else:
        memflag = False
    path, diff_time, delta_m = controller.req_7(control, memflag)
    print('\n')
    print(f'Tiempo que tardó el algoritmo: {diff_time}')
    if delta_m:
        print(f'Espacio usado en  memoria: {round(delta_m,3)} [kB]')
    if path: 
        print('\n')
        print(f'{"-"*10} Ruta con el menor número de comparendos {"-"*10}\n')
        print(f'Número de comparendos en el camino: {path["infracciones"]}')
        print(f'Distancia total del camino (km): {path["distance"]}')
        print(f'Número total de nodos: {path["n_nodes"]}\n')

        node_str=''
        for node in lt.iterator(path['nodes']):
            node_str+=f'{node},'
        print(f'{"-"*10} IDs de los nodos incluidos {"-"*10}\n')
        print(node_str[:-1]) 
        print('\n')
        print(f'{"-"*10} Arcos incluídos {"-"*10}\n')
        edges_str=''
        for edge in lt.iterator(path['edges']):
            edges_str+=f'{edge}, '
        print(edges_str.strip()[:-1])
    else:
        print('\n')
        print('Por favor asegúrese de ingresar unos puntos que se encuentren dentro del límite de la ciudad.')


def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    pass


# Se crea el controlador asociado a la vista
control = new_controller()

# main del reto
def thread_cycle():
    working= True
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 1:
            print("Cargando información de los archivos ....\n")
            data = load_data(control)
        elif int(inputs) == 2:     
                estacion_inicial_lon = float(input("Ingrese la longitud de la estacion origen: "))
                estacion_inicial_lat = float(input("Ingrese la latitud de la estacion de origen: "))
                estacion_destino_lon = float(input("Ingrese la longitud de la estacion destino: "))
                estacion_destino_lat = float(input("Ingrese la latitud de la estacion destino: "))
                print_req_1(control, estacion_inicial_lon, estacion_inicial_lat, estacion_destino_lon, estacion_destino_lat)
            
        elif int(inputs) == 3:
                estacion_inicial_lon = float(input("Ingrese la longitud de la estacion origen: "))
                estacion_inicial_lat = float(input("Ingrese la latitud de la estacion de origen: "))
                estacion_destino_lon = float(input("Ingrese la longitud de la estacion destino: "))
                estacion_destino_lat = float(input("Ingrese la latitud de la estacion destino: "))
                print_req_2(control, estacion_inicial_lon, estacion_inicial_lat, estacion_destino_lon, estacion_destino_lat)

        elif int(inputs) == 4:
                camaras= int(input("Ingrese el número de camaras que desea instalar: "))
                localidad= input("Ingrese la localidad: ")
                memoria= input("Desea saber la memoria:")
                print_req_3(control, camaras, localidad,memoria)

        elif int(inputs) == 5:
                print_req_4(control)

        elif int(inputs) == 6:
                cant_camaras= 10#int(input("Ingrese la cantidad de camaras que desea comparar: "))
                tipo_vehiculo = "monotocicleta"#str(input("Ingrese el tipo de vehiculo que desea consultar: "))
                print_req_5(control, cant_camaras, tipo_vehiculo)

        elif int(inputs) == 7:
                print_req_6(control)

        elif int(inputs) == 8:
                print_req_7(control)

        elif int(inputs) == 9:
                print_req_8(control)

        elif int(inputs) == 0:
                working = False
                print("\nGracias por utilizar el programa")
            
        else:
                print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)

if __name__ == "__main__":
        """
        Menu principal
        """
        threading.stack_size(67108864)
        sys.setrecursionlimit(2 ** 20)
        thread = threading.Thread(target=thread_cycle)
        thread.start()
