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

### HELPER FUNCTIONS ###
def read_csv():
    df = pd.read_csv("./csv/data.csv")

### DATA ###
data.get_data()

def basic_info(df,categories=["tempo","duration","key","time_signature","song_hotness"]):
    print "basic_info() called"
    start_time = time.time()
    df[categories].describe()
    skew = df[categories].skew()
    correlations = df[categories].corr()
    print "Finished. Time elapsed: {0}".format(time.time() - start_time)

def plot_freq(df,category="year"):
    print "plot_freq() called"
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
    print "Finished. Time elapsed: {0}".format(time.time() - start_time)

def plot_world(df):
    print "plot_world() called"
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
