import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
sys.path.append("./")
from msd import get_data

# Settings for ipython
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

### DATA ###

def basic_info(categories=["tempo","duration","key","time_signature","song_hotttnesss"],saved_csv=None):
    """ Prints skew and pairwise correlations of all categories"""
    
    if saved_csv: 
        df = pd.read_csv(saved_csv)
    else:
        df = get_data(categories,write=True)
    start_time = time.time()
    
    df.describe()
    skew = df.skew()
    print skew
    correlations = df.corr()
    print correlations

    txt_header = " ".join(categories)
    np.savetxt("./temp/describe.txt", df.describe().values, fmt='%f',header=txt_header)
    np.savetxt("./temp/skew.txt", skew.values, fmt='%f',header=txt_header)
    np.savetxt("./temp/correlations.txt", correlations.values, fmt='%f',header=txt_header)
    print "Finished. Time elapsed: {0}".format(time.time() - start_time)

def plot_freq(category="year",saved_csv=None):
    """ Plots frequency of category"""
    
    if saved_csv: 
        df = pd.read_csv(saved_csv)
    else:
        df = get_data([category],write=True)
    start_time = time.time()
    
    df_clean= df[df != 0].dropna() # Drop NA values and 0 values
    cat_counts=df_clean[category].value_counts(normalize=True,ascending=True)
    cat_counts.plot(kind="bar")
    title = "Overall Output % by '" + category + "'"
    plt.title(title) 
    plt.tick_params(axis="x",labelsize=6)
    
    filename = category+"_frequency.png"
    plt.savefig(filename,bbox_inches="tight")
    plt.clf()
    print "Finished. Time elapsed: {0}".format(time.time() - start_time)

def plot_world(saved_csv=None):
    """ Plots artists location on world map using latitude and longitude """

    categories=["artist_latitude","artist_longitude"]
    if saved_csv: 
        df = pd.read_csv(saved_csv)
    else:
        df = get_data(categories,write=True)
    start_time = time.time()
    
    df_locs =df[categories].dropna(axis=0) # Delete rows with no values in lat/long
    df_locs = df_locs[df_locs.duplicated()] 
    lat_lon = df_locs.as_matrix(columns=categories)
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
    plt.title("Artist Locations")
    
    plt.savefig("artist_location.png",bbox_inches="tight")
    plt.clf()
    print "Finished. Time elapsed: {0}".format(time.time() - start_time)
