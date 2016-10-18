import os
import sys
sys.path.append("./MSongsDB/PythonSrc")
pd.set_option('display.expand_frame_repr', False)
import hdf5_getters 
import numpy as np
import pandas as pd

### DATA ###
h5_files = [x   for x in os.walk("./MillionSongSubset/data")  if len(x[0]) == 30 ] # There's the conditional to differentiate between different directory structures, anything less than 30 means the path is referencing a parent directory
data = []

for root,dirs,files in h5_files:
	for f in files:
		h5file = hdf5_getters.open_h5_file_read(os.path.join(root,f))
		mbtags=hdf5_getters.get_artist_mbtags(h5file)
		similar_artists=hdf5_getters.get_similar_artists(h5file)
		energy = hdf5_getters.get_energy(h5file)
		artist_hottness = hdf5_getters.get_artist_hotttnesss(h5file)
		h5file.close()
		datapoint = {"mbtags":mbtags,"similar_artists":similar_artists,"energy":energy,"artist_hottness":artist_hottness}
		data.append(datapoint)

df = pd.DataFrame(data)

print ""
print df 

