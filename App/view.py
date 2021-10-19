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
    print("7- Encontrar los artistas más prolíficos del museo")
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




def printCronoArtists(artistas):
    """
    Imprime el resultado de listar cronológicamente los artistas 
    que nacieron en un rango de años
    """
    tamanio = lt.size(artistas)
    print("\nNúmero total de artistas en dicho rango: "+str(tamanio)+"\n")
    print("Los primeros y últimos 3 artistas son: \n")
    for i in range(1,4):
        print("Nombre: "+lt.getElement(artistas,i)["DisplayName"])
        print("Año de nacimiento: "+lt.getElement(artistas,i)["BeginDate"])
        print("Año de fallecimiento: "+lt.getElement(artistas,i)["EndDate"])
        print("Nacionalidad: "+lt.getElement(artistas,i)["Nationality"])
        print("Género: "+lt.getElement(artistas,i)["Gender"])
        print("\n")
    print(". . . . . . . . . . . . . . . . . . . . . . . . . . . . . .\n")
    for i in range(-2,1):
        print("Nombre: "+lt.getElement(artistas,tamanio+i)["DisplayName"])
        print("Año de nacimiento: "+lt.getElement(artistas,tamanio+i)["BeginDate"])
        print("Año de fallecimiento: "+lt.getElement(artistas,tamanio+i)["EndDate"])
        print("Nacionalidad: "+lt.getElement(artistas,tamanio+i)["Nationality"])
        print("Género: "+lt.getElement(artistas,tamanio+i)["Gender"])
        print("\n")



def printSortArtworks(ord_artworks):
    """
    Imprime el resultado de listar cronológicamente las obras 
    adquiridas en un rango de fechas
    """
    tamanio = lt.size(ord_artworks[1])
    print("\nNúmero total de obras en el rango cronológico: "+str(tamanio)+"\n")
    print("Número total de obras adquiridas por compra: "+str(ord_artworks[0])+"\n")
    printArtworks(ord_artworks,tamanio)



def printArtworks(ord_artworks, tamanio):
    print("Sus primeras y últimas 3 obras son: \n")
    for i in range(1,4):
        print("Título: "+lt.getElement(ord_artworks[1],i)["Title"])
        print("Artista(s): "+str(lt.getElement(ord_artworks[1],i)["Artists"]["elements"])[1:-1])
        print("Fecha: "+lt.getElement(ord_artworks[1],i)["Date"])
        print("Fecha de adquisición: "+lt.getElement(ord_artworks[1],i)["DateAcquired"])
        print("Medio: "+lt.getElement(ord_artworks[1],i)["Medium"])
        print("Dimensiones: "+lt.getElement(ord_artworks[1],i)["Dimensions"])
        print("\n")
    print(". . . . . . . . . . . . . . . . . . . . . . . . . . . . . .\n")
    for i in range(-2,1):
        print("Título: "+lt.getElement(ord_artworks[1],tamanio+i)["Title"])
        print("Artista(s): "+str(lt.getElement(ord_artworks[1],tamanio+i)["Artists"]["elements"])[1:-1])
        print("Fecha: "+lt.getElement(ord_artworks[1],tamanio+i)["Date"])
        print("Fecha de adquisición: "+lt.getElement(ord_artworks[1],tamanio+i)["DateAcquired"])
        print("Medio: "+lt.getElement(ord_artworks[1],tamanio+i)["Medium"])
        print("Dimensiones: "+lt.getElement(ord_artworks[1],tamanio+i)["Dimensions"])
        print("\n")
        




def printArtworksNacionalidad(result):
    print("\nTOP 10 - Nacionalidades en el MOMA\n")
    print("Nacionalidad : Obras")
    for i in range(1,11): 
        print(lt.getElement(result[0],i)[0]+" : "+str(lt.getElement(result[0],i)[1]))
    print("\nLa nacionalidad con más obras en el MOMA es: ",lt.getElement(result[0],1)[0])
    tamanio = lt.size(result[1])
    printArtworks(result, tamanio)




def printArtistsProlific(res, cantArtist, anioI, anioF):
    print("\nLos ",cantArtist,"artistas más prolíficos entre ",anioI," y ",anioF," son: \n")
    for artist in lt.iterator(res):
        print("Nombre: "+artist[0]["Nombre"])
        print("Año de nacimiento: "+artist[0]["Año"])
        print("Género: "+artist[0]["Género"])
        print("Total de Obras: ",artist[1])
        print("Total de Medios: ",artist[2])
        print("Medio más usado: ",artist[3])
        print("Primeras 5 obras de la técnica mas utilizada: ")
        for obra in lt.iterator(artist[4]):
            print("\n\tTítulo: "+obra["Title"])
            print("\tFecha: "+obra["Date"])
            print("\tFecha de adquisición: "+obra["DateAcquired"])
            print("\tMedio: "+obra["Medium"])
            print("\tDepartamento: "+obra["Department"])
            print("\tClasificación: "+obra["Classification"])
            print("\tDimensiones: "+obra["Dimensions"])
        print("\n")






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
        "printCostoTransDept(result)"
    



    elif int(inputs[0]) == 7:
        cantArtist = int(input("Ingrese el número de artistas que desea en la clasificación: "))
        anioI = int(input("Ingrese el año incial del rango: "))
        anioF = int(input("Ingrese el año final del rango: "))
        result = controller.artistsProlific(catalog, cantArtist, anioI, anioF)
        printArtistsProlific(result, cantArtist, anioI, anioF)
    

    else:
        print("Usted ha salido de la aplicación.")
        sys.exit(0)
sys.exit(0)
