import numpy as np
import pandas as pd
import folium
import geocoder
from folium.plugins import MeasureControl

g = geocoder.ip('me')
#print(g.latlng)

m=folium_map = folium.Map(location=[g.latlng[0],g.latlng[1]], zoom_start=13)

folium.Marker(location=[g.latlng[0],g.latlng[1]]).add_to(folium_map)
folium_map
m.add_child(MeasureControl())