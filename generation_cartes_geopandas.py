# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 15:23:54 2020

@author: sautot
"""

import geopandas
import os

# Import des données
datadir = 'E:\Documents\Recherche\GDN'

path_airesurb = os.path.join(datadir,'Data_transports','aires_urbaines.shp')
print('chargement de ' + path_airesurb) 
vlayer_airesurb = geopandas.read_file(path_airesurb)

path_motifs = os.path.join(datadir,'Data_transports','cooc_data_withgeoms.csv')
print('chargement de ' + path_motifs)
vlayer_motifs =  geopandas.read_file(path_motifs)

datadirosm = datadir+'/Data_transports/OSM'
vlayer_rail = list()
print('Chargement des fichiers de '+datadirosm)
for f in os.listdir(datadirosm):
    if not os.path.isfile(os.path.join(datadirosm,f)):
        path_osm = os.path.join(datadirosm,f,'gis_osm_railways_free_1.shp')
        vlayer_rail.append(geopandas.read_file(path_osm))

# Représentation
base = vlayer_airesurb.plot(column='aires_ur_2')
vlayer_motifs.plot(ax=base)
vlayer_rail[1].plot(ax=base,color='black')