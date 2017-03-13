import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
sys.path.append("./")
from grab_data import get_song_data
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA

# Settings for ipython
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

def basic_info(categories=["tempo","duration","key","time_signature","song_hotttnesss"],saved_csv=None):
    """ Prints skew and pairwise correlations of all categories"""
    if saved_csv: 
        df = pd.read_csv(saved_csv)
        df = df[categories]
    else:
        df = get_song_data(categories,write=True)
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
        df = df[categories]
    else:
        df = get_song_data([category],write=True)
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

def world_plot(lat="artist_latitude",lon="artist_longitude",saved_csv=None):
    """ Plots artists location on world map using latitude and longitude 
    
    Parameters
    ---------
    lat: String
        Category to pull latitude data. 
    lon: String
        Category to pull longitude data
    saved_csv: String

    Returns
    -------
    None, saves figure in working directory
    
    
    """
    if saved_csv: 
        df = pd.read_csv(saved_csv)
        df = df[categories]
    else:
        df = get_song_data([lat,lon],write=True)
    start_time = time.time()
    
    df_locs =df[[lat,lon]].dropna(axis=0) # Delete rows with no values in lat/long
    df_locs = df_locs[df_locs.duplicated()] 
    lat_lon = df_locs.as_matrix(columns=[lat,lon])
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

def stacked_bar_plot(full="duration",head_end="end_of_fade_in",tail_start="start_of_fade_out",saved_csv=None):
    """ Creates a stacked plot 
    
    Parameters
    ---------
    full: String
        Data Category Name. Total size of barplot
    head_end: String
        Data Category Name. Bottom portion of stacked bar plot, represents the end value. 
    tail_start: String
        Top portion of stacked bar plot, represents the starting value.

    Returns
    -------
    None, saves figure in working directory

    """
    if saved_csv: 
        df = pd.read_csv(saved_csv)
        df = df["categories"]
    else:
        df = get_song_data([full,head_end,tail_start],write=True)
    start_time =time.time()

    df_clean = df.dropna(axis=0)
    df_cropped = df_clean[:100]
    ii = np.arange(0,df_cropped.shape[0])

    fade_in = df_cropped[head_end]
    fade_out = df_cropped[full].sub(df_cropped[tail_start]) # To get value of start of tail to end of song
    middle = df_cropped[full].sub(fade_in).sub(fade_out) # Full contains head and tail already so we need to subtract the amounts of head and tail to avoid double counting
    
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

def compare_to_average(x_cat="year",y_cat="artist_hotttnesss",saved_csv=None):
    """ Plots raw data y, average y for each x and finds areas where average y for each x is above/below total average y
        
        Parameters
        ----------
        x_cat: String
            X-axis variable. This category will act as the index.
        y_cat: String
            Y-axis variable. This category will be plotted in comparison with it's average
        saved_csv: String

        Returns
        -------
        None, saves figure in working directory

    """

    if saved_csv: 
        df = pd.read_csv(saved_csv)
        df = df[categories]
    else:
        df = get_song_data(categories,write=True)
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

    plt.xlabel("Year")
    plt.ylabel("Artist Hotness")
    plt.savefig("averages.png",bbox_inches="tight")
    plt.clf()
    plt.legend()
    print "Done. Time elapsed: {0}".format(time.time() - start_time)

def error_bar(categories=["segments_loudness_max","segments_confidence"],data_start=[0,1],sec_i=[0,100],saved_csv=None):
    """ Pulls categories from raw data and plots error bar 

    Parameters 
    ---------
    categories: List/Strings (Must be 2D)
        Strings are specific keywords. For a full list of available categories and more information: http://labrosa.ee.columbia.edu/millionsong/pages/example-track-description
        categories[0]: y-value
        categories[1]: y-value error
    data_i: List, optional
        Start/End index value for pulling raw data
        Defaults to [0,1]
    sec_i: List,optional
        Start/End index value for segment to examine in each datapoint
        Defaults to [0, 100]
    saved_csv: String,optional
        Link to .csv file with raw data

    Returns
    ------
    None, saves figures in working directory

    """ 
    if saved_csv: 
        df = pd.read_csv(saved_csv)
        df = df[categories]
    else: 
        df = get_song_data(categories,write=False,end_i=data_i[1])
    start_time = time.time()


    for j in range(data_i[1]):
        f = plt.figure(j)
        plt.title("Song {0}[{1}:{2}]".format(j,sec_i[0],sec_i[1]))
        plt.xlabel("segment")
        plt.ylabel(categories[0])
        x = range(len(df[categories[0]][j]))[sec_i[0]:sec_i[1]]
        y = df[categories[0]][j][sec_i[0]:sec_i[1]]
        y_error = df[categories[1]][j][sec_i[0]:sec_i[1]]

        plt.errorbar(x,y,yerr=y_error,marker="s")
        filename = "error_bar_{0}.png".format(j)
        plt.savefig(filename,bbox_inches="tight")
    plt.clf()
    print "Done. Time elapsed: {0}".format(time.time() - start_time)


def dr(x_categories=["key","loudness","mode","tempo","year"],y_category=["artist_mbtags","artist_mbtags_count"],saved_csv="./temp/song_data.csv"):
    """Dimensionality Reduction using T-SNE and PCA"""
    if saved_csv: df = pd.read_csv(saved_csv)
    else: df = get_song_data(x_categories+y_category,write=True)

    # Clean df
    df_y_clean = df_y[len(df_y[i]) == 0]
    
    # Condense each artist tag into just one entry
    X = df[x_categories].as_matrix()

    start_time = time.time()
    tsne = TSNE(n_components=2,random_state=1)
    X_tsne = tsne.fit_transform(X)

    plt.scatter(np.transpose(X_tsne)[0],np.transpose(X_tsne)[1])
    filename = "tsne.png"
    plt.title("T-SNE")
    plt.savefig(filename,bbox_inches="tight")
    #plt.legend() # To indicate what colors correspond with what colors on the scatterplot
    plt.clf()

    pca = PCA(n_components=2,svd_solver="randomized",random_state=1)
    X_pca = pca.fit_transform(X)

    plt.scatter(np.transpose(data_pca)[0],np.transpose(data_pca)[1],)
    filename = "pca.png"
    plt.title("PCA")
    plt.savefig(filename,bbox_inches="tight")
    plt.clf()
