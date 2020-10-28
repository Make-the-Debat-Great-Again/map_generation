import geopandas
import os

from scalebar import scale_bar
import cartopy.crs as ccrs

import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import matplotlib

from shapely.geometry import Polygon

def select_motifs(motifs,list_change,list_attribut,list_transport):
    # Create an empty list
    filter_arr = []
    
    # go through each element in arr
    for m in range(len(motifs)):
        # if the element is higher than 42, set the value to True, otherwise False:
        if (motifs['change'][m] in list_change and motifs['attribut'][m] in list_attribut and motifs['transport'][m] in list_transport):
            filter_arr.append(True)
        else :
            filter_arr.append(False)
    
    newarr = motifs[filter_arr]
    return newarr

#theme = 'développement des trains'
theme = 'développement des pistes cyclables'
#area = 'France'
area = 'Charente'

if (area == 'France'):
    #symbol size
    motif_markersize = 0.2
    gares_markersize = 0.4
    linewidth = 0.5
    #extent
    xmin = -0.15e6
    xmax = 1.5e6
    ymin = 6e6
    ymax = 7.25e6
elif (area == 'Charente'):
    #symbol size
    motif_markersize = 50
    gares_markersize = 100
    linewidth = 3
    #extent
    xmin = 258219.2866
    xmax = 572056.6832
    ymin = 6432794.7987
    ymax = 6615902.6867

# LOAD DATA
print("Loading Data...")
aires_urbaines = geopandas.read_file("aires_urbaines.geojson")
motifs =  geopandas.read_file("motifs_all.geojson")

# URBAN AREA COLOR
aires_urbaines["color"] = aires_urbaines.apply(lambda x: "Pôle" if x.aires_ur_2 not in "Autre multipolarisé;Communes isolées hors influence des pôles;Multipolarisé des grands pôles".split(";") else x.aires_ur_2,axis=1)
def color_(x):
    dic_ = {
        "Autre multipolarisé":1,
        "Communes isolées hors influence des pôles":0,
        "Multipolarisé des grands pôles":2,
        "Pôle":3
    }
    return dic_[x]
aires_urbaines["color"] = aires_urbaines["color"].apply(color_)

print("Plotting...")

# Représentation
ax = plt.axes(projection=ccrs.LambertAzimuthalEqualArea())

print("- Add Urban Area...")
aires_urbaines.plot(column = "color",cmap="Blues",figsize=(40,20),edgecolor="grey",linewidth=0.2,ax=ax)

# Thématiques
if (theme == 'développement des trains'):
    railroad = geopandas.read_file("railroad_fr.geojson")
    
    #gares
    trainstations = geopandas.read_file("trainstations.geojson")
    
    #motifs
    list_change = ['augmenter','construire','créer','développer','hausser']
    list_attribut = ['nombre','fréquence','quantité','rapidité','vitesse',None]
    list_transport = ['ferroviaire','gare','ligne de train','petite ligne','ter','tgv','train','voie de chemin de f']
    motifs = select_motifs(motifs,list_change,list_attribut,list_transport)
    
    print("- Add RailRoad...")
    railroad.plot(ax=ax,color='red',linewidth=linewidth)
    
    print("- Add Train stations...")
    trainstations.plot(ax=ax,markersize=gares_markersize,color="red")
    
    label_lignes = 'voie ferrée'
elif (theme == 'développement des pistes cyclables') :
    bikeway = geopandas.read_file("bikeway_fr.geojson")
    
    #motifs
    list_change = ['augmenter','construire','créer','développer','hausser']
    list_attribut = ['nombre','fréquence','quantité','rapidité','vitesse',None]
    list_transport = ['piste cyclable','voie cyclable','vélo','bande cyclable']
    motifs = select_motifs(motifs,list_change,list_attribut,list_transport)
    
    print("- Add BikeWay...")
    bikeway.plot(ax=ax,color='red',linewidth=linewidth)
    
    label_lignes = 'piste cyclable'
print("- Add Patterns...")
motifs.plot(ax=ax,markersize=motif_markersize,color="orange")

# LABEL
communes = geopandas.read_file("communes_importantes.geojson")
polygon = Polygon([(xmin, ymin), (xmin, ymax), (xmax, ymax), (xmax, ymin)])
communes_clipped = geopandas.clip(communes, polygon)
for idx, row in communes_clipped.iterrows():
    ax.annotate(s=row['nom_commun'], xy=[row['geometry'].representative_point().x,row['geometry'].representative_point().y],horizontalalignment='center')

print("- Add Cities' Names...")

ax.axis("off")

ax.set_xlim((xmin,xmax))
ax.set_ylim((ymin,ymax))


print("- Add Scalebar and North Arrow...")
# SCALE BAR AND NORTH ARROW
scale_bar(ax, [0.1,0.05], 20,text_kwargs=dict(fontsize="22")) # changer fontsize pour la taille de la police

x, y, arrow_length = 0.1, 0.7, 0.05
ax.annotate('N', xy=(x, y), xytext=(x, y-arrow_length),
            arrowprops=dict(facecolor='black', width=5, headwidth=15),
            ha='center', va='center', fontsize=20,
            xycoords=ax.transAxes)

print("- Add Legend...")

# LEGEND
cmap = matplotlib.cm.get_cmap('Blues')
norm = matplotlib.colors.Normalize(vmin=0, vmax=3)

legend_elements = [Line2D([0], [0], color='r', lw=4, label=label_lignes),
                   Line2D([0], [0], marker='o', color='w', label='Motif de '+theme,
                          markerfacecolor='orange', markersize=15),
                   Patch(facecolor="white", edgecolor='white',
                         label='$\\bf{Aires}$ $\\bf{urbaines}$'),
                   Patch(facecolor=cmap(norm(0)), edgecolor='gray',
                         label='Communes isolées hors influence des pôles'),
                   Patch(facecolor=cmap(norm(1)), edgecolor='gray',
                         label='Autre multipolarisé'),
                   Patch(facecolor=cmap(norm(2)), edgecolor='gray',
                         label='Multipolarisé des grands pôles'),
                   Patch(facecolor=cmap(norm(3)), edgecolor='gray',
                         label='Pôle')]

if (theme == 'développement des trains'):
    legend_elements.insert(1,Line2D([0], [0], marker='o', color='w', label='Gares', markerfacecolor='red', markersize=15))

legend = ax.legend(handles=legend_elements, loc='best',title="Légende",fontsize="16") # changer fontsize pour la taille de la police
legend.get_title().set_fontsize('18') # Augmenter ou diminuer valeur pour la taille de la police du titre de la légende

print("DONE !")
# SAVE FIGURE TO PNG
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(40, 20)
fig.savefig('carte1bis.png', dpi=300,bbox_inches="tight")
# SAVE FIGURE TO PDF
#fig.savefig('carte2bis.pdf',bbox_inches='tight')