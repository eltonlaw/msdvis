# Million Song Dataset Data Exploration

* Dataset retrieved from: http://labrosa.ee.columbia.edu/millionsong/
* HDF5 getter functions provided/taken from: https://github.com/tbertinmahieux/MSongsDB/blob/master/PythonSrc/hdf5_getters.py
* All analysis is on the sample set
* NOTE: Written in python 2.7 due to inconsistencies with the python 3 version of the tables module and the hdf5 getter functions provided by Thierry Bertin-Mahieux.

## Setup

If you want to run the code: 
``` bash
>>> git clone https://github.com/eltonlaw/msd_data_exploration.git
```
Then download the [dataset](https://labrosa.ee.columbia.edu/millionsong/pages/getting-dataset) and move the downloaded and unzipped dataset into the repo

``` bash
>>> mv MillionSongSubset msd_data_exploration/MillionSongSubset
```

Also need to have the hdf5 helper functions from Thierry Bertin-Mahieux's GitHub repo

``` bash
>>> cd msd_data_exploration
>>> git clone https://github.com/tbertinmahieux/MSongsDB
```

Make a temp folder for the output graphs:
``` bash
>>> mkdir temp
```

Your directory should look something like this now:
```
msd_data_exploration
│   grab_data.py
│   MillionSongsSubset
│   model.py
└───MSongsDB
│   │   ...
│   └───Python Src
│       │   hdf5_descriptors.py
│       │   hdf5_getters.py
│       │   ...
|   README.md
|   run.py
|   scrape_categories.py
└───temp
```
Now you should be able to run the analysis with this command:
``` bash
python -m run.py
```

## Initial Analysis
``` python
basic_info(categories=["tempo","duration","key","time_signature","song_hotttnesss"])
```
Print skew, distribution and pairwise correlation for the 5 following categories: tempo, duration, key, time_signature, song_hotttnesss.

### Pairwise Correlations
![correlation](https://cloud.githubusercontent.com/assets/14999531/20969484/27544d5e-bc57-11e6-9b66-f970332594be.png)
<p>The elements tested are linearly independent.</p>

### Distribution
![distribution](https://cloud.githubusercontent.com/assets/14999531/20969483/2747d84e-bc57-11e6-97f2-f3762c45b8d6.png)

### Skew
![skew](https://cloud.githubusercontent.com/assets/14999531/20969485/275640f0-bc57-11e6-8ac2-23b19021db12.png)


## Artist Locations from latitude/longitude 
``` python
world_plot(lat="artist_latitude",lon="artist_longitude")
```
Plot the latitude and longitude of each artist.

![artist location](https://cloud.githubusercontent.com/assets/14999531/20470597/14aa9c6c-af78-11e6-8be5-fabc7a74490a.png)
<p>Most of the datapoints are coming from North America and EU, the subset data is not representative of the population.</p> 

## Normalized % Frequency for each year
``` python
freq_plot(category="year")
```
Plots the normalized frequency of songs for each year in ascending order

![year frequency](https://cloud.githubusercontent.com/assets/14999531/20555335/826f03b0-b12f-11e6-89af-9a5e08b9627e.png)

## Duration of Songs
``` python
stacked_bar_plot(full="duration",head_end="end_of_fade_in",tail_start="start_of_fade_out")
```
Plots the song duration in black and overlays the end of the fade in and start of fade out in red.<


![duration_fade_in-out](https://cloud.githubusercontent.com/assets/14999531/21753100/2ff79590-d5b3-11e6-8485-bff39b356f28.png)


## Average 'artist_hotttnesss' Over Time
``` python
compare_to_average(x_cat="year",y_cat="artist_hotttnesss")
```
Plots raw data y, average y for each x and finds areas where average y for each x is above/below total average 

![Average Artist Hotness Over Time](https://cloud.githubusercontent.com/assets/14999531/21758068/caa63ff4-d605-11e6-8fa0-24ab67a33d79.png)
<p>Each raw datapoint represents a song. The blue line on the bottom represents the average "Artist Hotness" for each year we have raw datapoints for. Because some years are missing in between, the line is sporadic. The dotted black line represents the average of average "Artist Hotness". Green areas represent year ranges where the average for that year is above the average of the average. Red areas represent the opposite, where the average is below the average of the average.</p>

## Segment Max Loudness
``` python
error_bar(categories=["segments_loudness_max","segments_confidence"],data_start=[0,1],sec_i[0,100])
```
Plots error bars for max loudness.

![Error Bar for Max Loudness in each Segment](https://cloud.githubusercontent.com/assets/14999531/21872608/5d305796-d837-11e6-92bb-ba4ce6925b20.png)
<p>The full "segment_loudness_max" array contains 791 values for datapoint 0, this image shows the first 100 and the associated confidence values.</p>

## Dimensionality Reduction
``` python
dr(x_categories=["key","loudness","mode","tempo","year"],y_category=["artist_mbtags","artist_mbtags_count"])
```
Plots dimensions reduced through T-SNE and PCA. 

![PCA](https://cloud.githubusercontent.com/assets/14999531/21970558/5cd4bc9c-db75-11e6-89b3-f0faa08cab50.png)
![TSNE](https://cloud.githubusercontent.com/assets/14999531/21970562/6e2ccd40-db75-11e6-8f79-35dcbb2b0549.png
)
<p>Result of going from 5 dimensions to 2 using the following categories: "key","loudness","mode","tempo","year". Used Principal Component Analysis and t-distributed Stochastic Neighbor Embedding.</p>

# Citations

Thierry Bertin-Mahieux, Daniel P.W. Ellis, Brian Whitman, and Paul Lamere. 
The Million Song Dataset. In Proceedings of the 12th International Society
for Music Information Retrieval Conference (ISMIR 2011), 2011.


## TO DO's
* Setup .tar.gz unzipper
* Currently entire dataset needs to be loaded into memory prior to doing any analysis 
* Write hdf5 helper functions 
