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
               'medium': None,
               'nationality': None}
    
    catalog['artists'] = lt.newList("SINGLED_LINKED", compareArtistsConstituentID)
    catalog['artworks'] = lt.newList("SINGLE_LINKED", compareArtworksObjectID)
    
    """
    A continuacion se crean indices por diferentes criterios
    para llegar a la informacion consultada.  Estos indices no
    replican informacion, solo referencian los libros de la lista
    creada en el paso anterior.
    """

    """
    Este indice crea un map cuya llave es el medio de la obra
    """
    catalog['medium'] = mp.newMap(800,
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=compareArtworksByMedium)

    catalog['nationality'] = mp.newMap(100,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   comparefunction=compareArtworksByNationality)
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
    nombresyNacionalidades = encontrarNombresyNacionalidades(artwork["ConstituentID"][1:-1].split(","), catalog)
    artwork["Artists"] = nombresyNacionalidades[0]
    artwork["Nationalities"] = nombresyNacionalidades[1]
    lt.addLast(catalog['artworks'], artwork)
    addMedium(catalog, artwork["Medium"], artwork)
    for i in range(1,lt.size(artwork["Nationalities"])+1):
        addNationality(catalog, lt.getElement(artwork["Nationalities"], i), artwork)
    


def addArtist(catalog, artist):
    """
    Adiciona un artista a la lista
    """
    lt.addLast(catalog['artists'], artist)

    
def addMedium(catalog, namemedium, artwork):
    """
    Esta función adiciona una obra a la lista de un medio.
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



def addNationality(catalog, nameNationality, artwork):
    """
    Esta función adiciona una obra a la lista de una nacionalidad.
    """
    nationalities = catalog['nationality']
    existNationality = mp.contains(nationalities, nameNationality)
    if existNationality:
        entry = mp.get(nationalities, nameNationality)
        nationality = me.getValue(entry)
    else:
        nationality = newNationality(nameNationality)
        mp.put(nationalities, nameNationality, nationality)
    lt.addLast(nationality['artworks'], artwork)



# Funciones para creacion de datos

def newMedium(name):
    """
    Crea una nueva estructura para modelar las obras con un medio
    específico.
    """
    medium = {'name': "",
              "artworks": None}
    medium['name'] = name
    medium['artworks'] = lt.newList('SINGLE_LINKED', compareArtworksByMedium)
    return medium


def newNationality(name):
    """
    Crea una nueva estructura para modelar las obras con una nacionalidad 
    específica.
    """
    nationality = {'name': "",
              "artworks": None}
    nationality['name'] = name
    nationality['artworks'] = lt.newList('SINGLE_LINKED', compareArtworksByNationality)
    return nationality


# Funciones de consulta


def encontrarNombresyNacionalidades(artistas, catalog):
    """
    Encuentra nombres y nacionalidades a partir de sus ID
    """
    nombres = lt.newList(datastructure="ARRAY_LIST")
    nacionalidades = lt.newList(datastructure="ARRAY_LIST")
    for id in artistas:
        encontro = False
        i = 0
        while not encontro and i< lt.size(catalog["artists"]):
            if lt.getElement(catalog["artists"],i)["ConstituentID"] == str(id).strip():
                lt.addLast(nombres, lt.getElement(catalog["artists"],i)["DisplayName"])
                lt.addLast(nacionalidades, lt.getElement(catalog["artists"],i)["Nationality"])
                encontro = True
            i += 1
    return nombres, nacionalidades




def getArtworksByMedium(catalog, namemedium):
    """
    Retorna un medio con sus obras a partir del nombre del medio
    """
    medium = mp.get(catalog['medium'], namemedium)
    if medium:
        return me.getValue(medium)
    return None



def cantObrasNacion(catalog, nacion):
    nacion = mp.get(catalog["nationality"], nacion)
    if nacion:
        result = (me.getValue(nacion))["artworks"]
        return lt.size(result)
    return None



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




def compareArtworksByMedium(medium, medio):
    """
    Compara dos medios de obras. El primero es una cadena
    y el segundo un entry de un map
    """
    llaveMedio = me.getKey(medio)
    if (medium == llaveMedio):
        return 0
    elif (medium > llaveMedio):
        return 1
    else:
        return -1



def compareArtworksByNationality(nationality, nacionalidad):
    """
    Compara dos nacionalidades de obras. El primero es una cadena
    y el segundo un entry de un map
    """
    llaveNacionalidad = me.getKey(nacionalidad)
    if (nationality == llaveNacionalidad):
        return 0
    elif (nationality > llaveNacionalidad):
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
    return artwork1["Date"]<artwork2["Date"] and artwork1["Date"] != None and artwork2["Date"] != None


# Funciones de ordenamiento

def sortArtworksByDate(catalog, medio):
    artworksMedium = getArtworksByMedium(catalog, medio)
    sub_list = artworksMedium["artworks"].copy()
    sorted_list = sm.sort(sub_list, cmpArtworkByDate)
    return sorted_list
