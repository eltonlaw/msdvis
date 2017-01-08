# Million Song Dataset Data Exploration

* Dataset retrieved from: http://labrosa.ee.columbia.edu/millionsong/
* HDF5 getter functions provided/taken from: https://github.com/tbertinmahieux/MSongsDB/blob/master/PythonSrc/hdf5_getters.py
* Unless otherwise indicated, all analysis is on the sample set
* Written in python 2 due to inconsistencies with the python 3 version of the tables module and the hdf5 getter functions provided by Thierry Bertin-Mahieux.

## Initial Analysis

### Pairwise Correlations

![correlation](https://cloud.githubusercontent.com/assets/14999531/20969484/27544d5e-bc57-11e6-9b66-f970332594be.png)

### Distribution

![distribution](https://cloud.githubusercontent.com/assets/14999531/20969483/2747d84e-bc57-11e6-97f2-f3762c45b8d6.png)

### Skew

![skew](https://cloud.githubusercontent.com/assets/14999531/20969485/275640f0-bc57-11e6-8ac2-23b19021db12.png)

## Artist Locations from latitude/longitude 

![artist location](https://cloud.githubusercontent.com/assets/14999531/20470597/14aa9c6c-af78-11e6-8be5-fabc7a74490a.png)

## Normalized % Frequency for each year
![year frequency](https://cloud.githubusercontent.com/assets/14999531/20555335/826f03b0-b12f-11e6-89af-9a5e08b9627e.png)

In ascending order, the years with the most songs sampled.

## Duration of Songs
![duration_fade_in-out](https://cloud.githubusercontent.com/assets/14999531/21753100/2ff79590-d5b3-11e6-8485-bff39b356f28.png)

Plotted the song duration in black and overlayed the fade in and out in red.

# Citations

Thierry Bertin-Mahieux, Daniel P.W. Ellis, Brian Whitman, and Paul Lamere. 
The Million Song Dataset. In Proceedings of the 12th International Society
for Music Information Retrieval Conference (ISMIR 2011), 2011.
