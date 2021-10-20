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
import datetime as dt
import math
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
               'date': None,
               'dateAdquirido': None,
               'medium': None,
               'nationality': None,
               'artistaObra': None}
    
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
    catalog['date'] = mp.newMap(150,
                            maptype='CHAINING',
                            loadfactor=4.0,
                            comparefunction=compareArtistsByBeginDate)

    catalog['dateAdquirido'] = mp.newMap(900,
                                    maptype='PROBING',
                                    loadfactor=0.5,
                                    comparefunction=compareArtworksByDate)

    catalog['medium'] = mp.newMap(800,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   comparefunction=compareArtworksByMedium)

    catalog['nationality'] = mp.newMap(100,
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=compareArtworksByNationality)

    catalog['departamento'] = mp.newMap(10,
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=compareArtworksByArtist)

    catalog['artistaObra'] = mp.newMap(2000,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   comparefunction=compareArtworksByArtist)
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
    addDateAdquirido(catalog, artwork["DateAcquired"], artwork)
    addDepartment(catalog, artwork["Department"], artwork)
    for nationality in lt.iterator(artwork["Nationalities"]):
        addNationality(catalog, nationality, artwork)
    for artistObra in lt.iterator(artwork["Artists"]):
        addArtistaObra(catalog, artistObra, artwork)



def addArtist(catalog, artist):
    """
    Adiciona un artista a la lista
    """
    lt.addLast(catalog['artists'], artist)
    addBeginDate(catalog, artist["BeginDate"], artist)



def addBeginDate(catalog, nameDate, artist):
    """
    Esta función adiciona un artista a la lista de una fecha.
    """
    dates = catalog['date']
    existDate = mp.contains(dates, str(nameDate))
    if existDate:
        entry = mp.get(dates, str(nameDate))
        date = me.getValue(entry)
    else:
        date = newDate(str(nameDate))
        mp.put(dates, str(nameDate), date)
    lt.addLast(date['artists'], artist)



def addDateAdquirido(catalog, nameDate, artwork):
    """
    Esta función adiciona un artista a la lista de una fecha.
    """
    dates = catalog['dateAdquirido']
    existDate = mp.contains(dates, str(nameDate))
    if existDate:
        entry = mp.get(dates, str(nameDate))
        date = me.getValue(entry)
    else:
        date = newDateAdquirido(str(nameDate))
        mp.put(dates, str(nameDate), date)
    lt.addLast(date['artworks'], artwork)



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
    if nameNationality == "":
        nameNationality = "Nationality unknown"
    existNationality = mp.contains(nationalities, nameNationality)
    if existNationality:
        entry = mp.get(nationalities, nameNationality)
        nationality = me.getValue(entry)
    else:
        nationality = newNationality(nameNationality)
        mp.put(nationalities, nameNationality, nationality)
    lt.addLast(nationality['artworks'], artwork)


def addDepartment(catalog, nameDepartment, artwork):
    """
    Esta función adiciona una obra a la lista de un departamento.
    """
    departments = catalog['departamento']
    existDepartment = mp.contains(departments, nameDepartment)
    if existDepartment:
        entry = mp.get(departments, nameDepartment)
        department = me.getValue(entry)
    else:
        department = newDepartment(nameDepartment)
        mp.put(departments, nameDepartment, department)
    lt.addLast(department['artworks'], artwork)


def addArtistaObra(catalog, nameArtist, artwork):
    """
    Esta función adiciona una obra a la lista de un artista.
    """
    artistas = catalog['artistaObra']
    existArtist = mp.contains(artistas, nameArtist)
    if existArtist:
        entry = mp.get(artistas, nameArtist)
        artist = me.getValue(entry)
    else:
        artist = newArtistaObra(nameArtist)
        mp.put(artistas, nameArtist, artist)
    lt.addLast(artist['artworks'], artwork)




def addMediumBono(medio, namemedium, artwork):
    """
    Esta función adiciona una obra a la lista de un medio.
    """
    existmedium = mp.contains(medio, namemedium)
    if existmedium:
        entry = mp.get(medio, namemedium)
        medium = me.getValue(entry)
    else:
        medium = newMedium(namemedium)
        mp.put(medio, namemedium, medium)
    lt.addLast(medium['artworks'], artwork)


# Funciones para creacion de datos


def newDate(nameDate):
    """
    Crea una nueva estructura para modelar los artistas con un BeginDate
    específico.
    """
    date = {'name': "",
            "artists": None}
    date['name'] = nameDate
    date['artists'] = lt.newList('SINGLE_LINKED', compareArtistsByBeginDate)
    return date


def newDateAdquirido(nameDate):
    """
    Crea una nueva estructura para modelar las obras con un DateAcquired
    específico.
    """
    date = {'name': "",
            "artworks": None}
    date['name'] = nameDate
    date['artworks'] = lt.newList('SINGLE_LINKED', compareArtworksByDate)
    return date



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



def newDepartment(name):
    """
    Crea una nueva estructura para modelar las obras con un departamento 
    específico.
    """
    department = {'name': "",
              "artworks": None}
    department['name'] = name
    department['artworks'] = lt.newList('SINGLE_LINKED', compareArtworksByNationality)
    return department



def newArtistaObra(name):
    """
    Crea una nueva estructura para modelar las obras con un artista 
    específico.
    """
    artistaObra = {'name': "",
              "artworks": None}
    artistaObra['name'] = name
    artistaObra['artworks'] = lt.newList('SINGLE_LINKED', compareArtworksByNationality)
    return artistaObra



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



def artworksNacionalidad(catalog):
    """
    Req 4: Clasifica las obras por la nacionalidad de sus creadores.
    """
    llaves = mp.keySet(catalog["nationality"])
    lstNacion = lt.newList(datastructure="ARRAY_LIST")
    for key in lt.iterator(llaves):
        tamanio = cantObrasNacion(catalog, key)
        lt.addLast(lstNacion, (key,tamanio))
    ordenada = sm.sort(lstNacion, cmpNacionalidad)
    nacionMayor = lt.getElement(ordenada,1)[0]
    nacion = mp.get(catalog["nationality"], nacionMayor)
    result = (me.getValue(nacion))["artworks"]
    return ordenada, result



def cantObrasNacion(catalog, nacion):
    nacion = mp.get(catalog["nationality"], nacion)
    if nacion:
        result = (me.getValue(nacion))["artworks"]
        return lt.size(result)
    return None





def costoTransDept(catalog, dept):
    """
    Req 5: Calcular el costo para transportar todas las obras de un departamento.
    """
    total = 0
    costoFinal = 0
    pesoFinal = 0
    masCostosas = lt.newList(datastructure="ARRAY_LIST")
    masAntiguas = lt.newList(datastructure="ARRAY_LIST")
    completaCosto = False
    completaAntiguedad = False
    lstDepartamento = mp.get(catalog["departamento"], dept)
    if lstDepartamento:
        result = (me.getValue(lstDepartamento))["artworks"]
        for artwork in lt.iterator(result):
            if dept == artwork["Department"]:
                precioArtwork = precioobra(artwork)
                costoFinal += precioArtwork[0]
                total += 1
                pesoFinal += precioArtwork[1]
                if lt.size(masCostosas) < 5:
                    lt.addLast(masCostosas, [artwork,precioArtwork[0]])
                elif lt.size(masCostosas) == 5 and not completaCosto:
                    sm.sort(masCostosas, cmpCosto)
                    completaCosto = True
                else:
                    i = 5
                    entro1 = False
                    while i > 0 and not entro1:
                        if i == 1:
                            lt.removeLast(masCostosas)
                            lt.insertElement(masCostosas,[artwork,precioArtwork[0]], i)
                            entro1 = True
                        elif precioArtwork[0] <= lt.getElement(masCostosas, i)[1]:
                            entro1 = True
                        elif precioArtwork[0] < lt.getElement(masCostosas, i-1)[1]:
                            lt.removeLast(masCostosas)
                            lt.insertElement(masCostosas, [artwork,precioArtwork[0]], i)
                            entro1 = True
                        else:
                            i -= 1
                if lt.size(masAntiguas) < 5:
                    lt.addLast(masAntiguas, [artwork,precioArtwork[0]])
                elif lt.size(masAntiguas) == 5 and not completaAntiguedad:
                    sm.sort(masAntiguas, cmpArtworkByDateDpt)
                    completaAntiguedad = True
                else:
                    i = 5
                    entro2 = False
                    if artwork["Date"] != "":
                        while i > 0 and not entro2:
                            if i == 1:
                                lt.removeLast(masAntiguas)
                                lt.insertElement(masAntiguas, [artwork,precioArtwork[0]], i)
                                entro2 = True
                            elif artwork["Date"] > lt.getElement(masAntiguas, i)[0]["Date"]:
                                entro2 = True
                            elif artwork["Date"] > lt.getElement(masAntiguas, i-1)[0]["Date"]:
                                lt.removeLast(masAntiguas)
                                lt.insertElement(masAntiguas, [artwork,precioArtwork[0]], i)
                                entro2 = True
                            else:
                                i -= 1
    costoFinal = round(costoFinal,3)
    pesoFinal = round(pesoFinal,2)
    return total, costoFinal, pesoFinal, masAntiguas, masCostosas




def precioobra(artwork):
    """"
    Función auxiliar, encuentra el costo de una obra teniendo en cuenta sus dimensiones.
    """
    pesoObra = 0
    precioObra = 0
    lados = 0
    l1 = 1
    l2 = 1
    l3 = 1
    l4 = 1
    if artwork["Weight (kg)"] != "" and  artwork["Weight (kg)"] != "0":
        precioObra = 72*float(artwork["Weight (kg)"])
        pesoObra += float(artwork["Weight (kg)"])
    if artwork["Depth (cm)"] != "" and artwork["Depth (cm)"] != "0":
        l1 = float(artwork["Depth (cm)"])/100
        lados += 1
    if artwork["Height (cm)"] != "" and artwork["Height (cm)"] != "0":
        l2 = float(artwork["Height (cm)"])/100
        lados += 1
    if artwork["Length (cm)"] != "" and artwork["Length (cm)"] != "0":
        l3 = float(artwork["Length (cm)"])/100
        lados += 1
    if artwork["Width (cm)"] != "" and ["Width (cm)"] != "0":
        l4 = float(artwork["Width (cm)"])/100
        lados += 1
    if artwork["Diameter (cm)"] != "" and artwork["Diameter (cm)"] != "0" and lados <= 1:
        areaDm = (((((float(artwork["Diameter (cm)"])/2)**2)*math.pi)/10000)*l1*l2*l3*l4)
        if areaDm * 72 > precioObra:
            precioObra = areaDm*72
    if artwork["Circumference (cm)"] != "" and artwork["Circumference (cm)"] != "0" and lados <= 1:
        areaCrcn = ((((float(artwork["Circumference (cm)"])**2)/(4*math.pi))/10000)*l1*l2*l3*l4)
        if areaCrcn * 72 > precioObra:
            precioObra = areaCrcn*72
    if lados == 2 or lados == 3:
        areaLados = (l1*l2*l3*l4)
        if areaLados * 72 > precioObra:
            precioObra = areaLados*72
    if precioObra == 0:
        precioObra = 48
    return precioObra, pesoObra






def artistsProlific(catalog, cantArtist, anioI, anioF):
    """
    Req 6: Encuentra los artistas más prolíficos del museo.
    """
    artistasFiltrados = sortArtists(catalog, anioI, anioF)
    lstArtistasObra = lt.newList(datastructure="ARRAY_LIST")
    for key in lt.iterator(artistasFiltrados):
        result = cantObrasyMediosArtista(catalog, key["DisplayName"])
        datosArtist = {"Nombre": key["DisplayName"],
                        "Año": key["BeginDate"],
                        "Género": key["Gender"]}
        tamanio = result[0]
        cantMedios = result[1]
        nombreMedio = result[2]
        listaMedios = result[3]
        lt.addLast(lstArtistasObra, (datosArtist,tamanio,cantMedios,nombreMedio,listaMedios))

    ordenada = sm.sort(lstArtistasObra, cmpArtistasObra)
    res = lt.subList(ordenada,1,cantArtist)
    return res
    



def cantObrasyMediosArtista(catalog, artista):
    """
    Retorna la cantidad de obras del artista, la cantidad de 
    medios utilizados y una pareja llave valor, siendo la 
    llave el medio más usado y la pareja una lista con las obras de 
    ese medio de ese artista
    """
    artist = mp.get(catalog["artistaObra"], artista)
    tamanio = 0
    cantMedios = 0
    listaMedios = []
    nombreMedio = ""
    if artist:
        result = (me.getValue(artist))["artworks"]
        tamanio = lt.size(result)
        medios = mp.newMap(800,
                            maptype='PROBING',
                            loadfactor=0.5,
                            comparefunction=compareArtworksByMedium)
        for obra in lt.iterator(result):
            addMediumBono(medios, obra["Medium"], obra)
        lstObrasMedio = lt.newList(datastructure="ARRAY_LIST")
        for key in lt.iterator(mp.keySet(medios)):
            tamanio2 = cantObrasMedio(medios, key)
            lt.addLast(lstObrasMedio, (key,tamanio2))
        ordenada = sm.sort(lstObrasMedio, cmpObrasMedio)
        cantMedios = lt.size(ordenada)
        mayorMedio = lt.getElement(ordenada, 1)
        res = mp.get(medios, mayorMedio[0])
        if res:
            mayorMedio = me.getValue(res)
            listaMediosTotal = mayorMedio["artworks"]
            if lt.size(listaMediosTotal) < 5:
                listaMedios = lt.subList(listaMediosTotal,1,lt.size(listaMediosTotal))
            else:
                listaMedios = lt.subList(listaMediosTotal,1,5)
            nombreMedio = mayorMedio["name"]
        return tamanio, cantMedios, nombreMedio, listaMedios
    return None, None, None, None



def cantObrasMedio(medios, llave):
    llave = mp.get(medios, llave)
    if llave:
        result = (me.getValue(llave))["artworks"]
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



def compareArtistsByBeginDate(date, fecha):
    """
    Compara dos fechas de artistas. El primero es una cadena
    y el segundo un entry de un map
    """
    llaveFecha = me.getKey(fecha)
    if (date == llaveFecha):
        return 0
    elif (date > llaveFecha):
        return 1
    else:
        return -1


def compareArtworksByDate(date, fecha):
    """
    Compara dos fechas de obras. El primero es una cadena
    y el segundo un entry de un map
    """
    llaveFecha = me.getKey(fecha)
    if (date == llaveFecha):
        return 0
    elif (date > llaveFecha):
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



def cmpCosto(costo1, costo2):
    """
    Devuelve verdadero (True) si costo 1 es manor a costo2
    """
    return costo1[1] < costo2[1]


def compareArtworksByArtist(artist, artista):
    """
    Compara dos artistas de obras. El primero es una cadena
    y el segundo un entry de un map
    """
    llaveArtista = me.getKey(artista)
    if (artist == llaveArtista):
        return 0
    elif (artist > llaveArtista):
        return 1
    else:
        return -1
        


def cmpNacionalidad(nacionalidad1, nacionalidad2):
    """
    Devuelve verdadero (True) si nacionalidad1 es mayor a nacionalidad2.
    """
    return nacionalidad1[1]>nacionalidad2[1]



def cmpArtworkByDate(artwork1, artwork2):
    """
    Devuelve verdadero (True) si el 'Date' de artwork1 es menor que el de artwork2
    Args:
    artwork1: informacion de la primera obra que incluye su valor 'Date'
    artwork2: informacion de la segunda obra que incluye su valor 'Date'
    """
    return artwork1["Date"]<artwork2["Date"] and artwork1["Date"] != None and artwork2["Date"] != None


def cmpArtworkByDateAcquired(artwork1, artwork2):
    """
    Devuelve verdadero (True) si el 'DateAcquired' de artwork1 es menor que el de artwork2
    Args:
    artwork1: informacion de la primera obra que incluye su valor 'DateAcquired'
    artwork2: informacion de la segunda obra que incluye su valor 'DateAcquired'
    """
    return (artwork1)<(artwork2) and artwork1 != None and artwork2 != None


def cmpObrasMedio(medio1, medio2):
    """
    Devuelve verdadero (True) si medio1 es mayor a medio2.
    """
    if medio1[0] == "":
        medio1 = (medio1[0],0)
    if medio2[0] == "":
        medio2 = (medio2[0],0)
    return medio1[1]>medio2[1]


def cmpArtworkByDateDpt(artwork1, artwork2):
    """
    Devuelve verdadero (True) si el 'Date' de artwork1 es menor que el de artwork2
    Args:
    artwork1: informacion de la primera obra que incluye su valor 'Date'
    artwork2: informacion de la segunda obra que incluye su valor 'Date'
    """
    return (str(artwork1[0]["Date"])<str(artwork2[0]["Date"])) and artwork1[0]["Date"] != None and artwork2[0]["Date"] != None


def cmpArtistasObra(artista1, artista2):
    """
    Devuelve verdadero (True) si el artista1 es más prolífico
    que el artista2.
    """
    if artista1 == None or artista1 == "":
        artista1 = [0,0,0]
    if artista2 == None or artista2 == "":
        artista2 = [0,0,0]
    if artista1[1] == None or artista1[1] == "":
        artista1 = (artista1[0],0,artista1[2])
    if artista2[1] == None or artista2[1] == "":
        artista2 = (artista2[0],0,artista2[2])
    if artista1[2] == None or artista1[2] == "":
        artista1 = (artista1[0],artista1[1],0)
    if artista2[2] == None or artista2[2] == "":
        artista2 = (artista2[0],artista2[1],0)
    result = True
    if artista1[1]>artista2[1]:
        result = True
    elif artista1[1]<artista2[1]:
        result = False
    else:
        if artista1[2]>artista2[2]:
            result = True
        elif artista1[2]<artista2[2]:
            result = False
    return result


# Funciones de ordenamiento



def sortArtists(catalog,anioI,anioF):
    """
    Req 1: Ordenar artistas por fecha de nacimiento.
    """
    artistas = lt.newList(datastructure="ARRAY_LIST")
    for anio in range(anioI, anioF+1):
        date = mp.get(catalog["date"], str(anio))
        if date:
            artistsDate = me.getValue(date)['artists']
            for artist in lt.iterator(artistsDate):
                lt.addLast(artistas, artist)
    return artistas



def sortArtworks(catalog, anioI, mesI, diaI, anioF, mesF, diaF):
    """
    Req 2: Ordenar obras por fecha de adquisición.
    """
    obras = lt.newList(datastructure="ARRAY_LIST")
    fechaI = str(dt.datetime(anioI, mesI, diaI))
    fechaF = str(dt.datetime(anioF, mesF, diaF))
    llaves = mp.keySet(catalog["dateAdquirido"])
    llavesFiltradas = lt.newList(datastructure="ARRAY_LIST")
    
    for key in lt.iterator(llaves):
        if key != None and key != "" and fechaI <= key and fechaF >= key:
            lt.addLast(llavesFiltradas, key)

    llavesOrdenadas = sm.sort(llavesFiltradas, cmpArtworkByDateAcquired)
    
    obrasAdq = 0
    for key in lt.iterator(llavesOrdenadas):
        date = mp.get(catalog["dateAdquirido"], str(key))
        artworkDate = me.getValue(date)['artworks']
        for artwork in lt.iterator(artworkDate):
            lt.addLast(obras, artwork)
            if "purchase" in artwork["CreditLine"].lower():
                obrasAdq += 1
    return obrasAdq, obras


