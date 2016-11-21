import os
import sys
sys.path.append("./MSongsDB/PythonSrc")
import hdf5_getters 
import numpy as np
import pandas as pd
pd.set_option('display.expand_frame_repr', False)

### DATA ###
h5_files = [x   for x in os.walk("./MillionSongSubset/data")  if len(x[0]) == 30 ] # There's the conditional to differentiate between different directory structures, anything less than 30 means the path is referencing a parent directory
data = []

for root,dirs,files in h5_files:
	print "ROOT:",root
	print "FILES:",files
	for f in files:
		print "Loading...",(files.index(f)),'/',len(files)
		
		h5file = hdf5_getters.open_h5_file_read(os.path.join(root,f))
                a_id = hdf5_getters.get_artist_id(h5file)
		a_latitude = hdf5_getters.get_artist_latitude(h5file)
		a_longitude= hdf5_getters.get_artist_longitude(h5file)
                h5file.close()

                datapoint = {"id":a_id,"latitude":a_latitude,"longitude":a_longitude}
                data.append(datapoint)
df = pd.DataFrame(data)
df = df.dropna(axis=0) # Delete rows with now values in lat/long
df = df[df.duplicated()] # Delete duplicates

lat_lon = df.as_matrix(columns=["latitude","longitude"])

# Draw map
print "drawing map..."
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
m = Basemap(projection='mill',
        llcrnrlat =-90,
        llcrnrlon=-180,
        urcrnrlat=90,
        urcrnrlon=180, 
        resolution="c")
m.drawcoastlines()
m.drawcountries(linewidth=1)
m.drawstates()
m.bluemarble()
# Plot artists
print "plotting artist locations..."
for artist_lat,artist_lon in lat_lon:
    x_point,y_point = m(artist_lon,artist_lat)
    m.plot(x_point,y_point,"*",markersize = 10)

plt.title("Artist Locations")
plt.savefig("artist_location.png",bbox_inches="tight")


