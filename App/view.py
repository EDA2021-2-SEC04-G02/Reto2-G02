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
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Listar cronológicamente a los artistas")
    print("3- Listar cronológicamente las adquisiciones")
    print("4- Clasificar las obras de un artista por técnica")
    print("5- Clasificar las obras por la nacionalidad de sus creadores")
    print("6- Transportar obras de un departamento")
    print("7- Proponer una nueva exposición en el museo")
    print("0- Salir")




def initCatalog():
    """
    Inicializa el catalogo
    """
    return controller.initCatalog()



def cargarData(catalog):
    """
    Carga la información en la estructura de datos
    """
    controller.cargarData(catalog)






catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalog = initCatalog()
        cargarData(catalog)
        sizeArtists = int(lt.size(catalog['artists']))
        sizeArtworks = int(lt.size(catalog['artworks']))
        print('\nNúmero de artistas cargados: ' + str(sizeArtists))
        print('\nNúmero de obras cargadas: ' + str(sizeArtworks))
        print('\nÚltimos tres artistas cargados: \n')
        """
        i funciona como iterador para obtener los últimos tres elementos de las listas
        """
        i=2
        while i>=0:
            ultArtists = lt.getElement(catalog['artists'],(sizeArtists-i))
            print("-Nombre: "+ultArtists["DisplayName"])
            print("-ID: "+ultArtists["ConstituentID"]+"\n")
            i-=1
        print('Últimas tres obras cargadas: \n')
        """
        i funciona como iterador para obtener los últimos tres elementos de las listas
        """
        i=2
        while i>=0:
            ultArtworks = lt.getElement(catalog['artworks'],(sizeArtworks-i))
            print("-Título: "+ultArtworks["Title"])
            print("-ID: "+ultArtworks["ObjectID"]+"\n")
            i-=1
    
    
    
    elif int(inputs[0]) == 2:

        anioI = int(input("Ingrese el año incial del rango: "))
        anioF = int(input("Ingrese el año final del rango: "))
        result = controller.sortArtists(catalog,anioI,anioF)
        printCronoArtists(result)

        
    
    elif int(inputs[0]) == 3:
        diaI = int(input("Ingrese el día incial del rango: "))
        mesI = int(input("Ingrese el mes incial del rango: "))
        anioI = int(input("Ingrese el año incial del rango: "))
        diaF = int(input("Ingrese el día final del rango: "))
        mesF = int(input("Ingrese el mes final del rango: "))
        anioF = int(input("Ingrese el año final del rango: "))
        result = controller.sortArtworks(catalog, anioI, mesI, diaI, anioF, mesF, diaF)
        printSortArtworks(result)





    elif int(inputs[0]) == 5:

        result = controller.artworksNacionalidad(catalog)
        printArtworksNacionalidad(result)




    elif int(inputs[0]) == 6:
        dept = input("Ingrese el departamente del museo del que quiere conocer el costo de transporte: ")
        result = controller.costoTransDept(catalog, dept)
        printCostoTransDept(result)
    



    elif int(inputs[0]) == 7:
        anioI = int(input("Ingrese el año incial del rango: "))
        anioF = int(input("Ingrese el año final del rango: "))
        area = float(input("Ingrese el área disponible en metros cuadrados: "))
        result = controller.nuevaExpo(catalog,anioI,anioF,area)
        printNuevaExpo(result, catalog)



    else:
        print("Usted ha salido de la aplicación.")
        sys.exit(0)
sys.exit(0)
