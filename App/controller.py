﻿"""
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
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo

def initCatalog():
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    catalog = model.newCatalog()
    return catalog


# Funciones para la carga de datos

def cargarData(catalog):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    loadArtists(catalog)
    loadArtworks(catalog)


def loadArtists(catalog):
    """
    Carga los artistas del archivo.  Por cada artista se incluye nombre, 
    nacionalidad, genero, año de nacimiento, año de defunción, Wiki QID 
    y ULAN ID.
    """
    artistsfile = cf.data_dir + 'Artists-utf8-small.csv'
    input_file = csv.DictReader(open(artistsfile, encoding='utf-8'))
    for artist in input_file:
        model.addArtist(catalog, artist)


def loadArtworks(catalog):
    """
    Carga las obras del archivo.  Por cada obra se incluye titulo, 
    artista(s), fecha de creación, medio, dimensiones, fecha de 
    adquisición del museo, entre otros.
    """
    artworksfile = cf.data_dir + 'Artworks-utf8-small.csv'
    input_file = csv.DictReader(open(artworksfile, encoding='utf-8'))
    for artwork in input_file:
        model.addArtwork(catalog, artwork)



# Funciones de ordenamiento

def sortArtworksByDate(catalog, medio):
    result = model.sortArtworksByDate(catalog, medio)
    return result


# Funciones de consulta sobre el catálogo
