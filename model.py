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
    print "Done. Time elapsed: {0}".format(time.time() - start_time)

def freq_plot(category="year",saved_csv=None):
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
    print "Done. Time elapsed: {0}".format(time.time() - start_time)

def world_plot(saved_csv=None):
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
    print "Done. Time elapsed: {0}".format(time.time() - start_time)

def hist_plot(category="time_signature"):
    pass

def stacked_bar_plot(categories=["end_of_fade_in","duration","start_of_fade_out"],saved_csv=None):
    """ Plots where the song is fading in and out in red and where the song is playing in blue"""
    if saved_csv: 
        df = pd.read_csv(saved_csv)
    else:
        df = get_data(categories,write=True)
    start_time =time.time()

    df_clean = df.dropna(axis=0)
    df_cropped = df_clean[:100]
    ii = np.arange(0,df_cropped.shape[0])

    fade_in = df_cropped[categories[0]]
    fade_out = df_cropped[categories[1]].sub(df_cropped[categories[2]])
    middle = df_cropped[categories[1]].sub(fade_in).sub(fade_out)
    
    width = 0.5
    plt.bar(ii,fade_in,width,color="r")
    plt.bar(ii,middle,width,color="k",bottom=fade_in)
    plt.bar(ii,fade_out,width,color="r",bottom=middle)

    plt.ylim(ymin=-5)
    plt.title("Song duration")
    plt.xlabel("Song Index")
    plt.ylabel("Seconds")

    plt.savefig("fade_in_out.png",bbox_inches="tight")
    plt.clf()
    print "Done. Time elapsed: {0}".format(time.time() - start_time)

def compare_to_average(categories=["year","artist_hotttnesss"],saved_csv=None):
    """ Plots raw data y, average y for each x and finds areas where average y for each x is above/below total average y"""
    if saved_csv: df = pd.read_csv(saved_csv)
    else: df = get_data(categories,write=True)
    start_time = time.time()

    df_clean = df[df != 0].dropna()
    
    f = plt.figure(1)
    ax1 = plt.subplot2grid((2,2),(0,0),colspan=2)
    ax1.scatter(df_clean[categories[0]],df_clean[categories[1]])
    ax1.set_title("Raw Data")

    # For all unique x values, find the average y value 
    X = df_clean[categories[0]].unique() # All unique x values in cleaned dataframe
    xs,avgs = [],[]
    for x_i in X:
        df_x = df_clean[df[categories[0]] == x_i] # df containing all entries with x in categories[0]
        y_values = df_x[categories[1]].values
        avg_y = np.mean(y_values)
        xs.append(x_i)
        avgs.append(avg_y)

    xs_avgs = zip(xs,avgs)
    df_means= pd.DataFrame(xs_avgs,columns=categories)
    df_means.sort_values(by=categories[0],ascending=True,inplace=True)

    cat0 = df_means[categories[0]]
    cat1 = df_means[categories[1]]

    # Average of the raw data averages; average hotness over all years
    cat1_mean= np.mean(avgs)
    cat1_mean_list = np.full(np.shape(cat0),cat1_mean)
    
    # Subplot 2
    ax2 = plt.subplot2grid((2,2),(1,0),colspan=2,sharex=ax1)
    ax2.plot(cat0,cat1,lw=2) # Line of each years averages
    ax2.fill_between(cat0,cat1,cat1_mean,where=(cat1 > cat1_mean),facecolor="g") # Fill above avg hotness with green
    ax2.fill_between(cat0,cat1,cat1_mean,where=(cat1 < cat1_mean),facecolor="r") # Fill below avg hotness with red
    ax2.plot(cat0,cat1_mean_list,"k--") # Plot line of average hotness over all years
    ax2.set_title("Averaged")

    plt.ylabel("Artist Hotness")
    plt.xlabel("Year")
    plt.savefig("averages.png",bbox_inches="tight")
    plt.clf()
    plt.legend()
    print "Done. Time elapsed: {0}".format(time.time() - start_time)

