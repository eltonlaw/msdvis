import os
import numpy as np
import sys
import pandas as pd
import sqlite3
sys.path.append("./MSongsDB/PythonSrc")
import hdf5_getters
import multiprocessing


def get_song_data(categories,path="./MillionSongSubset/data",write=False,write_path="./temp/song_data.csv",start_i=0,end_i=10000):
    """ Pulls data from all h5 files on the provided path and all it's child nodes 

    Parameters 
    ---------
    categories: List/Strings
        Strings are specific keywords. For an example of available categories: http://labrosa.ee.columbia.edu/millionsong/pages/example-track-description
    path: String,optional
        Path to the h5 data to decode and compile
    write: Boolean,optional
         If true, writes the final compiled pandas Dataframe into a csv file located at "./temp/data.csv"
    write_path: String,optional
        If write = True, it will be the destination of the final compiled pandas Dataframe.
        
    Returns
    ------
    Pandas Dataframe containing categories 

    """
    h5_files = [x   for x in os.walk(path)  if len(x[0]) == 30 ] # There's the conditional to differentiate between different directory structures, anything less than 30 means the path is referencing a parent directory
    data,file_paths= [],[]
    count = 0
    for root,dirs,files in h5_files:
        for f in files:
            file_paths.append(os.path.join(root,f)) 

    for file_path in file_paths[start_i:end_i]:
        h5file = hdf5_getters.open_h5_file_read(file_path)
        datapoint = {}
        for cat in categories: 
            datapoint[cat] = getattr(hdf5_getters,"get_"+cat)(h5file)
        h5file.close()
        data.append(datapoint)

        progress = (count*100.)/10000 # 10 000 datapoints in sample 
        sys.stdout.write("==== Compiling subset of data... [ {:.2f}% ] ==== \r".format(progress))
        sys.stdout.flush()
        count +=1
    df = pd.DataFrame(data)
    if write:
        df.to_csv(write_path)
        print "Subset of data written to"+write_path
    return df

def get_meta_data(files=None,path="./MillionSongSubset/AdditionalFiles",write=False,write_path="./temp/meta_data.csv"):
    """ Dataset provides some summary data in the form of '.txt', '.h5' and '.db' files to help navigate the data 
    
    Parameters
    ----------
    categories: List
        Valid categories: ['subset_artist_location.txt', 'subset_artist_similarity.db', 'subset_artist_term.db', 'subset_msd_summary_file.h5', 'subset_track_metadata.db', 'subset_tracks_per_year.txt', 'subset_unique_artists.txt', 'subset_unique_mbtags.txt', 'subset_unique_terms.txt', 'subset_unique_tracks.txt']

    Returns
    ------
    Vector, each element represents one category
    
    """ 
    # If no specific files are selected, get them all
    if files == None:
        root,dirs,files = [x for x in os.walk(path)][0] 
        ignore = ["LICENSE","README"]
        for ii in ignore:
            files.remove(ii)
    
    data = []
    for f in files:
        file_path = os.path.join(path,f)
        if f.split(".")[1] == "txt":
            datapoint = np.genfromtxt(file_path,delimiter="<SEP>")
            data.append(datapoint)
        elif f.split(".")[1] == "db":
            file_path = os.path.join(path,"subset_artist_similarity.db")
            conn = sqlite3.connect(file_path)
            c = conn.cursor()
            c.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = c.fetchall()
            for table_name in tables:
                c.execute("SELECT * FROM " + str(table_name[0]))
                datapoint = c.fetchall()
                data.append(datapoint)
            conn.close()
        elif f.split(".")[1] == "h5":
            file_path = os.path.join(path,"subset_msd_summary_file.h5")
            h5file = hdf5_getters.open_h5_file_read(file_path)
            data.append(h5file) 
            h5file.close()
