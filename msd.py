import os
import sys
import pandas as pd
sys.path.append("./MSongsDB/PythonSrc")
import hdf5_getters

def get_data(categories,path="./MillionSongSubset/data",write=False,write_path="./temp/data.csv",start_i=0,end_i=10000):
    """ Pulls data from all h5 files on the provided path and all it's child nodes 

    Parameters 
    ---------
    categories: List/Strings
        Strings are specific keywords. For a full list of available categories and more information: http://labrosa.ee.columbia.edu/millionsong/pages/example-track-description
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
