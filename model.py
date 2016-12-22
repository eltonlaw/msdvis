import os
import sys
import time
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
def get_data(path="./MillionSongSubset/data")
    h5_files = [x   for x in os.walk(path)  if len(x[0]) == 30 ] # There's the conditional to differentiate between different directory structures, anything less than 30 means the path is referencing a parent directory
    data = []
    i = 0
    for ii,(root,dirs,files) in enumerate(h5_files):
        #print("ROOT:{}".format(root))
        #print("FILES:{}".format(files))
        for f in files:
            #print("Loading...{}/{}".format(files.index(f),len(files)))
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
            seg_timbre = hdf5_getters.get_segments_timbre(h5file) 
            seg_confidence = hdf5_getters.get_segments_confidence(h5file)
            seg_pitches = hdf5_getters.get_segments_pitches(h5file)
            seg_loudness_max = hdf5_getters.get_segments_loudness_max(h5file)
            seg_start = hdf5_getters.get_segments_start(h5file)

            h5file.close()
            datapoint = {"id":a_id,"latitude":a_latitude,"longitude":a_longitude,
                    "year":song_year,"tempo":tempo,"song_hotness":song_hotness,"tempo":tempo,
                    "time_signature":time_signature,"duration":duration,"key":key}
                    #"seg_timbre":seg_timbre,"seg_confidence":seg_confidence,"seg_pitches":seg_pitches,"seg_loudness_max":seg_loudness_max,"seg_start":seg_start}
            data.append(datapoint)
            progress = (i*100)/10000 # 10 000 datapoints in sample 
            if progress % 0.10 == 0:
                sys.stdout.write("==== Percentage Trained [ {:.2f}% ] ==== \r".format(progress))
                sys.stdout.flush()
            i+=1
    df = pd.DataFrame(data)
    df.to_csv("./csv/data.csv")

def basic_info(df,categories=["tempo","duration","key","time_signature","song_hotness"]):
    print("basic_info() called")
    start_time = time.time()
    df[categories].describe()
    skew = df[categories].skew()
    correlations = df[categories].corr()
    print("Finished. Time elapsed: {0}".format(time.time() - start_time))

def plot_freq(df,category="year"):
    print("plot_freq() called")
    start_time = time.time()
    df_cat= df[df[category] != 0].dropna()
    df_cat = df_year[category]
    cat_counts=df_cat.value_counts(normalize=True,ascending=True)
    cat_counts.plot(kind="bar")
    title = "Overall Output % by '" + category + "'"
    plt.title(title) # Missing data = 53.20% 
    plt.tick_params(axis="x",labelsize=6)
    filename = category+"_frequency.png"
    plt.savefig(filename,bbox_inches="tight")
    plt.clf()
    print("Finished. Time elapsed: {0}".format(time.time() - start_time))

def plot_artist_locations(df):
    print("plot_artist_locations() called")
    start_time = time.time()
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
    print("Finished. Time elapsed: {0}".format(time.time() - start_time))
