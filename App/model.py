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
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as sm
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newCatalog():
    """
    Inicializa el catálogo de artistas. Crea una lista vacia para guardar
    todos los artistas, adicionalmente, crea una lista vacia para las obras. 
    Retorna el catalogo inicializado.
    """
    catalog = {'artists': None,
               'artworks': None,
               'medium': None}
    
    catalog['artists'] = lt.newList("ARRAY_LIST", compareArtistsConstituentID)
    catalog['artworks'] = lt.newList("ARRAY_LIST", compareArtworksObjectID)
    
    """
    A continuacion se crean indices por diferentes criterios
    para llegar a la informacion consultada.  Estos indices no
    replican informacion, solo referencian los libros de la lista
    creada en el paso anterior.
    """

    """
    Este indice crea un map cuya llave es el medio de la obra
    """
    catalog['medium'] = mp.newMap(10000,
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=compareArtworksByMedium)
    return catalog





# Funciones para agregar informacion al catalogo

def addArtwork(catalog, artwork):
    """
    Esta funcion adiciona un libro a la lista de libros,
    adicionalmente lo guarda en un Map usando como llave su Id.
    Adicionalmente se guarda en el indice de autores, una referencia
    al libro.
    Finalmente crea una entrada en el Map de años, para indicar que este
    libro fue publicaco en ese año.
    """
    lt.addLast(catalog['artworks'], artwork)
    addMedium(catalog, artwork["Medium"], artwork)


def addArtist(catalog, artist):
    """
    Adiciona un artista a la lista
    """
    lt.addLast(catalog['artists'], artist)

    
def addMedium(catalog, namemedium, artwork):
    """
    Esta función adiciona un medio.
    """
    mediums = catalog['medium']
    existmedium = mp.contains(mediums, namemedium)
    if existmedium:
        entry = mp.get(mediums, namemedium)
        medium = me.getValue(entry)
    else:
        medium = newMedium(namemedium)
        mp.put(mediums, namemedium, medium)
    lt.addLast(medium['artworks'], artwork)
    

# Funciones para creacion de datos

def newMedium(name):
    """
    Crea una nueva estructura para modelar las obras con un medio
    específico. Se crea una lista para guardar los
    libros de dicho autor.
    """
    medium = {'medium': "",
              "artworks": None}
    medium['name'] = name
    medium['artworks'] = lt.newList('SINGLE_LINKED', compareArtworksByMedium)
    return medium

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista


def compareArtistsConstituentID(id1, id2):
    """
    Compara dos ids de dos artistas
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1


def compareArtworksObjectID(id1, id2):
    """
    Compara dos ids de dos obras
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1




def compareArtworksByMedium(medium, author):
    """
    Compara dos medios de obras. El primero es el medio
    y el segundo un entry de un map
    """
    authentry = me.getKey(author)
    if (medium == authentry):
        return 0
    elif (medium > authentry):
        return 1
    else:
        return -1



def cmpArtworkByDate(artwork1, artwork2):
    """
    Devuelve verdadero (True) si el 'Date' de artwork1 es menor que el de artwork2
    Args:
    artwork1: informacion de la primera obra que incluye su valor 'Date'
    artwork2: informacion de la segunda obra que incluye su valor 'Date'
    """
    print(artwork1["Date"])
    return (str(artwork1["Date"])<str(artwork2["Date"])) and artwork1["Date"] != None and artwork2["Date"] != None


# Funciones de ordenamiento

def sortArtworksByDate(catalog, medio):
    medium = mp.get(catalog['medium'], medio)
    if medium:
        sub_list = me.getValue(medium).copy()
        sorted_list = sm.sort(sub_list, cmpArtworkByDate)
        return sorted_list
