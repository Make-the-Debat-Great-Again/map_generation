import geopandas
import os

from scalebar import scale_bar
import cartopy.crs as ccrs

import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import matplotlib

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
    
    #motifs
    list_change = ['augmenter','construire','créer','développer','hausser']
    list_attribut = ['nombre','fréquence','quantité','rapidité','vitesse',None]
    list_transport = ['ferroviaire','gare','ligne de train','petite ligne','ter','tgv','train','voie de chemin de f']
    motifs = select_motifs(motifs,list_change,list_attribut,list_transport)
    
    print("- Add RailRoad...")
    railroad.plot(ax=ax,color='red',linewidth=0.5)
    
    label_lignes = 'voie ferrée'
elif (theme == 'développement des pistes cyclables') :
    bikeway = geopandas.read_file("bikeway_fr.geojson")
    
    #motifs
    list_change = ['augmenter','construire','créer','développer','hausser']
    list_attribut = ['nombre','fréquence','quantité','rapidité','vitesse',None]
    list_transport = ['piste cyclable','voie cyclable','vélo','bande cyclable']
    motifs = select_motifs(motifs,list_change,list_attribut,list_transport)
    
    print("- Add BikeWay...")
    bikeway.plot(ax=ax,color='red',linewidth=0.5)
    
    label_lignes = 'piste cyclable'
print("- Add Patterns...")
motifs.plot(ax=ax,markersize=0.2,color="orange")

ax.axis("off")
ax.set_xlim((-0.15e6,1.5e6))
ax.set_ylim((6e6,7.25e6))


print("- Add Scalebar and North Arrow...")
# SCALE BAR AND NORTH ARROW
scale_bar(ax, [0.6,0.05], 200,text_kwargs=dict(fontsize="22")) # changer fontsize pour la taille de la police

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

legend = ax.legend(handles=legend_elements, loc='right',title="Légende",fontsize="16") # changer fontsize pour la taille de la police
legend.get_title().set_fontsize('18') # Augmenter ou diminuer valeur pour la taille de la police du titre de la légende

print("DONE !")
# SAVE FIGURE TO PDF
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(40, 20)
fig.savefig("carte.pdf",bbox_inches="tight")
