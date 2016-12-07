import os
import sys
sys.path.append("./MSongsDB/PythonSrc")
import hdf5_getters 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

### HELPER FUNCTIONS ###
def read_csv():
    df = pd.read_csv("./csv/data.csv")

### DATA ###
h5_files = [x   for x in os.walk("./MillionSongSubset/data")  if len(x[0]) == 30 ] # There's the conditional to differentiate between different directory structures, anything less than 30 means the path is referencing a parent directory
data = []
ii=0
for root,dirs,files in h5_files:
    print "ROOT:",root
    #print "FILES:",files
    for f in files:
        #print "Loading...",(files.index(f)),'/',len(files)
        #if (hdf5_getters.get_num_songs(h5file) > 1): # For certain files with more than one song in it
        h5file = hdf5_getters.open_h5_file_read(os.path.join(root,f))
        a_id = hdf5_getters.get_artist_id(h5file)
        a_latitude = hdf5_getters.get_artist_latitude(h5file)
        a_longitude= hdf5_getters.get_artist_longitude(h5file)
        song_year = hdf5_getters.get_year(h5file)
        song_hotness = hdf5_getters.get_song_hotttnesss(h5file)
        tempo = hdf5_getters.get_tempo(h5file)
        time_signature = hdf5_getters.get_time_signature(h5file)
        duration = hdf5_getters.get_duration(h5file)
        key = hdf5_getters.get_key(h5file)
       # seg_timbre = hdf5_getters.get_segments_timbre(h5file) 
       # seg_confidence = hdf5_getters.get_segments_confidence(h5file)
       # seg_pitches = hdf5_getters.get_segments_pitches(h5file)
       # seg_loudness_max = hdf5_getters.get_segments_loudness_max(h5file)
       # seg_start = hdf5_getters.get_segments_start(h5file)
        h5file.close()
        datapoint = {"id":a_id,"latitude":a_latitude,"longitude":a_longitude,
                "year":song_year,"tempo":tempo,"song_hotness":song_hotness,"tempo":tempo,
                "time_signature":time_signature,"duration":duration,"key":key}
                #"seg_timbre":seg_timbre,"seg_confidence":seg_confidence,"seg_pitches":seg_pitches,"seg_loudness_max":seg_loudness_max,"seg_start":seg_start}
        data.append(datapoint)
df = pd.DataFrame(data)
df.to_csv("./csv/data.csv")

def basic_info()
    df[["tempo","duration","key","time_signature","song_hotness"]].describe()
    skew = df[["tempo","duration","key","time_signature","song_hotness"]].skew()
    correlations = df[["tempo","duration","key","time_signature","song_hotness"]].corr()

def plot_year_freq():
    df_year = df[df.year != 0].dropna()
    df_year = df_year["year"]
    year_counts=df_year.value_counts(normalize=True,ascending=True)
    year_counts.plot(kind="bar")
    plt.title("Overall Output % by Year") # Missing data = 53.20% 
    plt.tick_params(axis="x",labelsize=6)
    plt.savefig("year_frequency.png",bbox_inches="tight")
    plt.clf()

def plot_artist_locations():
    df_locs =df[["latitude","longitude"]].dropna(axis=0) # Delete rows with no values in lat/long
    df_locs = df_locs[df_locs.duplicated()] 
    lat_lon = df_locs.as_matrix(columns=["latitude","longitude"])

    # Draw map
    from mpl_toolkits.basemap import Basemap
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
    for artist_lat,artist_lon in lat_lon:
        x_point,y_point = m(artist_lon,artist_lat)
        m.plot(x_point,y_point,"*",markersize = 10)
    del lat_lon

    plt.title("Artist Locations")
    plt.savefig("artist_location.png",bbox_inches="tight")
    plt.clf()
