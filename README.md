# Million Song Dataset Data Exploration

* Dataset retrieved from: http://labrosa.ee.columbia.edu/millionsong/
* HDF5 getter functions provided/taken from: https://github.com/tbertinmahieux/MSongsDB/blob/master/PythonSrc/hdf5_getters.py
* Unless otherwise indicated, all analysis is on the sample set
* Written in python 2 due to inconsistencies with the python 3 version of the tables module and the hdf5 getter functions provided by Thierry Bertin-Mahieux.

## Initial Analysis

### Pairwise Correlations

![correlation](https://cloud.githubusercontent.com/assets/14999531/20969484/27544d5e-bc57-11e6-9b66-f970332594be.png)

The elements tested are linearly independent.

### Distribution

![distribution](https://cloud.githubusercontent.com/assets/14999531/20969483/2747d84e-bc57-11e6-97f2-f3762c45b8d6.png)

### Skew

![skew](https://cloud.githubusercontent.com/assets/14999531/20969485/275640f0-bc57-11e6-8ac2-23b19021db12.png)

## Artist Locations from latitude/longitude 

![artist location](https://cloud.githubusercontent.com/assets/14999531/20470597/14aa9c6c-af78-11e6-8be5-fabc7a74490a.png)

Most of the datapoints are coming from North America and EU, the subset data is not representative of the population. 

## Normalized % Frequency for each year
![year frequency](https://cloud.githubusercontent.com/assets/14999531/20555335/826f03b0-b12f-11e6-89af-9a5e08b9627e.png)

In ascending order, the years with the most songs sampled.

## Duration of Songs
![duration_fade_in-out](https://cloud.githubusercontent.com/assets/14999531/21753100/2ff79590-d5b3-11e6-8485-bff39b356f28.png)

Plotted the song duration in black and overlayed the end of the fade in and start of fade out in red.

## Average Artist Hotness Over Time
![Average Artist Hotness Over Time](https://cloud.githubusercontent.com/assets/14999531/21758068/caa63ff4-d605-11e6-8fa0-24ab67a33d79.png)

Each raw datapoint represents a song. The blue line on the bottom represents the average "Artist Hotness" for each year we have raw datapoints for. Because some years are missing in between, the line is sporadic. The dotted black line represents the average of average "Artist Hotness". Green areas represent year ranges where the average for that year is above the average of the average. Red areas represent the opposite, where the average is below the average of the average.

## Segment Max Loudness
![Error Bar for Max Loudness in each Segment](https://cloud.githubusercontent.com/assets/14999531/21872608/5d305796-d837-11e6-92bb-ba4ce6925b20.png)

The full "segment_loudness_max" array contains 791 values for datapoint 0, this image shows the first 100 and the associated confidence values. 

## Dimensionality Reduction
![PCA](https://cloud.githubusercontent.com/assets/14999531/21970558/5cd4bc9c-db75-11e6-89b3-f0faa08cab50.png)
![TSNE](https://cloud.githubusercontent.com/assets/14999531/21970562/6e2ccd40-db75-11e6-8f79-35dcbb2b0549.png
)

Result of going from 5 dimensions to 2 using the following categories: "key","loudness","mode","tempo","year". Used Principal Component Analysis and t-distributed Stochastic Neighbor Embedding.

# Citations

Thierry Bertin-Mahieux, Daniel P.W. Ellis, Brian Whitman, and Paul Lamere. 
The Million Song Dataset. In Proceedings of the 12th International Society
for Music Information Retrieval Conference (ISMIR 2011), 2011.
