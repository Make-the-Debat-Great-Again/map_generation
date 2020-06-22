# Librairies
from qgis.core import *
import qgis.utils
import os
from qgis.PyQt import QtGui

#print('import des librairies')

# Import des aires urbaines
datadir = "E:/Documents/Recherche/GDN/Résultats_transports"
path_airesurb = os.path.join(datadir,'cartes','aires_urbaines.shp')

print('chargement de ' + path_airesurb) 
vlayer_airesurb = iface.addVectorLayer(path_airesurb,'','ogr')
if not vlayer_airesurb.isValid() :
    print("erreur : couche non chargee")

# Import des motifs
print('chargement de E:/Documents/Recherche/GDN/Résultats_transports/cooc_data_withgeoms.csv')
uri = "file:///E:/Documents/Recherche/GDN/R%C3%A9sultats_transports/cooc_data_withgeoms.csv?type={}&delimiter={}&detectTypes={}&wktField={}&crs={}&spatialIndex={}&subsetIndex={}&watchFile={}".format("csv",";","yes","geom","EPSG:4326","no","no","no")
vlayer_motifs = iface.addVectorLayer(uri,"motifs","delimitedtext")

# Import d'OSM (rail)
datadirosm = datadir+'/cartes/OSM'
for f in os.listdir(datadirosm):
    if not os.path.isfile(os.path.join(datadirosm,f)):
        path_osm = os.path.join(datadirosm,f,'gis_osm_railways_free_1.shp')
        vlayer_rail = iface.addVectorLayer(path_osm,f,'ogr')

# Symbologie
#expression1 = QgsExpression("""if("aires_ur_2" = 'Communes isolées hors influence des pôles' or "aires_ur_2" = 'Autre multipolarisé' or "aires_ur_2" = 'Multipolarisé des grands pôles' or "aires_ur_2" is null, "aires_ur_2", 'Pôle'""")
#context = QgsExpressionContext()
#context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(vlayer_airesurb))
#with edit(vlayer_airesurb):
#    for f in vlayer_airesurb.getFeatures():
#        context.setFeature(f)
#        f['aires_ur_2'] = expression1.evaluate(context)
#        vlayer_airesurb.updateFeature(f)
#        print(f['aires_ur_2'])
# Ne pas décommenter ci dessus, c'est un gros fail

categorized_renderer = QgsCategorizedSymbolRenderer()
symbol1 = QgsFillSymbol()
symbol1.setColor(QtGui.QColor('#ffffff'))
symbol2 = QgsFillSymbol()
symbol2.setColor(QtGui.QColor('#8aebf8'))
symbol3 = QgsFillSymbol()
symbol3.setColor(QtGui.QColor('#8acef8'))
symbol4 = QgsFillSymbol()
symbol4.setColor(QtGui.QColor('#8ab4f8'))
symbol5 = QgsFillSymbol()
symbol5.setColor(QtGui.QColor('#337aff'))

cat1 = QgsRendererCategory(NULL, symbol1, 'null')
cat2 = QgsRendererCategory('Communes isolées hors influence des pôles', symbol2, 'Communes isolées hors influence des pôles')
cat3 = QgsRendererCategory('Autre multipolarisé', symbol3, 'Autre multipolarisé')
cat4 = QgsRendererCategory('Multipolarisé des grands pôles', symbol4, 'Multipolarisé des grands pôles')
cat5 = QgsRendererCategory('Pôle', symbol5, 'Pôle')

categorized_renderer.addCategory(cat1)
categorized_renderer.addCategory(cat2)
categorized_renderer.addCategory(cat3)
categorized_renderer.addCategory(cat4)
categorized_renderer.addCategory(cat5)

categorized_renderer.setClassAttribute('new_col')
vlayer_airesurb.setRenderer(categorized_renderer)