
# Project Notes:

* Spring wheat crop was planted on the 25th of April
* The year the data was taken from (2022) held favorable conditions for all crops so crop conditions,
including VI's, were more homogeneous than what is usually expected. The low variance in the VI from 2022's
data may influence the accuracy of the ML models predicting the yield.
* Vegetation index (vi) formula names: cigreen0, cigreen, evi2, gndvi0, gndvi, ndvi, rdvi, savi, sr
* The vi used will only be the 'mean' value for each data point
* Labels in full data and ground truth data: variety_index <-> variety <-> ENTRY | replication_variety <-> BLOC
* The soil temperature measurement used is the 8-inch average
* Winter varieties:
1. Rosalyn
2. Otto
3. Puma
4. Purl
5. Jasper
6. Inspire
7. Piranha CL+
8. Jameson
* Spring varieties:
1. Glee
2. Kelse 
3. Alum
4. Chet
5. Louise
6. Ryan
7. Seahawk
8. Whit
9. Dayn
10. Tekoa
11. Net CL+
12. Jedd
* A form of SMOTE (Synthetic Minority Oversampling Technique) was used to increase ML model performance. 
The distribution of the spring yields followed a normal distribution.
![SpringDist.png](Images%2FSpringDist.png)
In order to fix the issue of there being 
less data points on the extremities for the ML model to train on, minority oversampling was used. The minority 
sampling was done in two ways. Firstly, the data was cut down so that the distribution was level, as shown below.
![CutDist.png](Images%2FCutDist.png)
Secondly, the distribution was leveled by fabricating minority data.
![BulkDist.png](Images%2FBulkDist.png)
As an extra frame of reference, below is the winter yield distribution as well:
![WinterDist.png](Images%2FWinterDist.png)

### Units and labels:
 - Temperatures: Celsius
 - Yield: Bushels/Acre
 - Soil temperature depth: Inches
 - Plant height: Inches
 - Plot area: Square feet
 - IoT: Internet of Things

### Models' Results Notes:

**Data sets 1: Trained on raw training data (saved in saved_data_1.txt)**  
Number of testing sets: 6, Number of training sets: 24  
Average Yield: 78.30

* model_1
  * Spring, NDVI variate, Stacked 
  * Model average percent error (testing data): 5.27
  * Model average RMSE (testing data): 4.78
  * Model average percent error (training data): 4.92
  * Model average RMSE (testing data): 4.56


* spring_ndvi_vi_mean_vanilla_model1
  * Model average percent error (testing data): 
  * Model average percent error (training data):


**Data sets 2: Trained on cut training data (form of SMOTE) (saved in saved_data_2.txt)**  

**Data sets 3: Trained on bulked training data (form of SMOTE) (saved in saved_data_3.txt)**  



### VI to Yield Correlation Notes:
Note: Offset means the amount of days from the beginning of the data collection. Split size is the
duration, in days, of how long the best correlation segment is. 

* Spring full data average VI (ndvi) correlation:
![SpringFullDataVItoYield.png](Images%2FSpringFullDataVItoYield.png)


	Pearson correlation coefficient: 0.30

* Spring best split size (4) and offset (40) VI (ndvi) correlation:
![SpringBestSplitSizeVItoYield.png](Images%2FSpringBestSplitSizeVItoYield.png)


	Pearson correlation coefficient: 0.50

* Spring heading data VI correlation: 
![SpringHeadingDateVItoYield.png](Images%2FSpringHeadingDateVItoYield.png)


	Pearson correlation coefficient: -0.51

* Winter full data average VI (ndvi) correlation:
![WinterFullDataVitoYield.png](Images%2FWinterFullDataVitoYield.png)


	Pearson correlation coefficient: 0.53

* Winter best split size (3) and offset (45) VI (ndvi) correlation:
![WinterBestSplitSizeVItoYield.png](Images%2FWinterBestSplitSizeVItoYield.png)


	Pearson correlation coefficient: 0.58

* Winter heading data VI (ndvi) correlation: 
![WinterHeadingDateVItoYield.png](Images%2FWinterHeadingDateVItoYield.png)


	Pearson correlation coefficient: 0.62

### Missing Data Points Notes For Winter Wheat:
(Dates with * marker are within 2 weeks of heading date)

**Block: 1, Entry: 1 data points length: 68**
* Heading date: 2022-06-19
	* 2022-05-20
	* 2022-05-27
	* 2022-05-29
	* 2022-06-04
	* 2022-06-05
	* *2022-06-07
	* *2022-06-08
	* *2022-06-09
	* *2022-06-11
	* *2022-06-13
	* *2022-07-01
	* 2022-07-07
	* 2022-07-08

**Block: 1, Entry: 2 data points length: 68**
* Heading date: 2022-06-23
	* 2022-05-20
	* 2022-05-27
	* 2022-05-29
	* 2022-06-04
	* 2022-06-05
	* 2022-06-07
	* 2022-06-08
	* 2022-06-09
	* *2022-06-11
	* *2022-06-13
	* *2022-07-01
	* 2022-07-07
	* 2022-07-08

**Block: 1, Entry: 3 data points length: 68**
* Heading date: 2022-06-20
	* 2022-05-20
	* 2022-05-27
	* 2022-05-29
	* 2022-06-04
	* 2022-06-05
	* *2022-06-07
	* *2022-06-08
	* *2022-06-09
	* *2022-06-11
	* *2022-06-13
	* *2022-07-01
	* 2022-07-07
	* 2022-07-08

**Block: 1, Entry: 4 data points length: 68**
* Heading date: 2022-06-20
	* 2022-05-20
	* 2022-05-27
	* 2022-05-29
	* 2022-06-04
	* 2022-06-05
	* *2022-06-07
	* *2022-06-08
	* *2022-06-09
	* *2022-06-11
	* *2022-06-13
	* *2022-07-01
	* 2022-07-07
	* 2022-07-08

**Block: 1, Entry: 5 data points length: 73**
* Heading date: 2022-06-21
	* 2022-05-27
	* 2022-05-29
	* *2022-06-11
	* *2022-06-13
	* 2022-07-22
	* 2022-07-26
	* 2022-07-29

**Block: 1, Entry: 6 data points length: 73**
* Heading date: 2022-06-22
	* 2022-05-27
	* 2022-05-29
	* *2022-06-11
	* *2022-06-13
	* 2022-07-22
	* 2022-07-26
	* 2022-07-29

**Block: 1, Entry: 7 data points length: 73**
* Heading date: 2022-06-18
	* 2022-05-27
	* 2022-05-29
	* *2022-06-11
	* *2022-06-13
	* 2022-07-22
	* 2022-07-26
	* 2022-07-29

**Block: 1, Entry: 8 data points length: 73**
* Heading date: 2022-06-21
	* 2022-05-27
	* 2022-05-29
	* *2022-06-11
	* *2022-06-13
	* 2022-07-22
	* 2022-07-26
	* 2022-07-29

**Block: 2, Entry: 4 data points length: 73**
* Heading date: 2022-06-20
	* 2022-05-25
	* 2022-05-28
	* 2022-05-29
	* 2022-05-30
	* 2022-05-31
	* 2022-06-01
	* *2022-06-11
	* *2022-06-13

**Block: 2, Entry: 5 data points length: 73**
* Heading date: 2022-06-22
	* 2022-05-25
	* 2022-05-28
	* 2022-05-29
	* 2022-05-30
	* 2022-05-31
	* 2022-06-01
	* *2022-06-11
	* *2022-06-13

**Block: 2, Entry: 8 data points length: 73**
* Heading date: 2022-06-22
	* 2022-05-25
	* 2022-05-28
	* 2022-05-29
	* 2022-05-30
	* 2022-05-31
	* 2022-06-01
	* *2022-06-11
	* *2022-06-13

**Block: 2, Entry: 7 data points length: 73**
* Heading date: 2022-06-19
	* 2022-05-25
	* 2022-05-28
	* 2022-05-29
	* 2022-05-30
	* 2022-05-31
	* 2022-06-01
	* *2022-06-11
	* *2022-06-13

**Block: 2, Entry: 2 data points length: 76**
* Heading date: 2022-06-24
	* 2022-05-29
	* *2022-06-11
	* 2022-07-26
	* 2022-07-27
	* 2022-07-28

**Block: 2, Entry: 3 data points length: 76**
* Heading date: 2022-06-18
	* 2022-05-29
	* *2022-06-11
	* 2022-07-26
	* 2022-07-27
	* 2022-07-28

**Block: 2, Entry: 1 data points length: 76**
* Heading date: 2022-06-22
	* 2022-05-29
	* *2022-06-11
	* 2022-07-26
	* 2022-07-27
	* 2022-07-28

**Block: 2, Entry: 6 data points length: 76**
* Heading date: 2022-06-22
	* 2022-05-29
	* *2022-06-11
	* 2022-07-26
	* 2022-07-27
	* 2022-07-28

**Block: 3, Entry: 5 data points length: 68**
* Heading date: 2022-06-21
	* 2022-05-25
	* 2022-05-29
	* 2022-06-04
	* 2022-06-05
	* 2022-06-06
	* 2022-06-07
	* *2022-06-08
	* *2022-06-09
	* *2022-06-10
	* *2022-06-11
	* *2022-06-12
	* *2022-06-13

**Block: 3, Entry: 3 data points length: 68**
* Heading date: 2022-06-20
	* 2022-05-25
	* 2022-05-29
	* 2022-06-04
	* 2022-06-05
	* 2022-06-06
	* *2022-06-07
	* *2022-06-08
	* *2022-06-09
	* *2022-06-10
	* *2022-06-11
	* *2022-06-12
	* *2022-06-13

**Block: 3, Entry: 7 data points length: 68**
* Heading date: 2022-06-20
	* 2022-05-25
	* 2022-05-29
	* 2022-06-04
	* 2022-06-05
	* 2022-06-06
	* *2022-06-07
	* *2022-06-08
	* *2022-06-09
	* *2022-06-10
	* *2022-06-11
	* *2022-06-12
	* *2022-06-13

**Block: 3, Entry: 1 data points length: 68**
* Heading date: 2022-06-22
	* 2022-05-25
	* 2022-05-29
	* 2022-06-04
	* 2022-06-05
	* 2022-06-06
	* 2022-06-07
	* 2022-06-08
	* *2022-06-09
	* *2022-06-10
	* *2022-06-11
	* *2022-06-12
	* *2022-06-13

**Missing all data points for plot Block: 3, Entry: 2**

**Missing all data points for plot Block: 3, Entry: 4**

**Missing all data points for plot Block: 3, Entry: 8**

**Missing all data points for plot Block: 3, Entry: 6**


### Missing Data Points Notes For Sping Wheat:
(Dates with * marker are within 2 weeks of heading date)

**Block: 1, Entry: 9 data points length: 49**
* Heading date: 2022-06-25
	* *2022-06-13
	* *2022-06-14
	* *2022-06-15
	* *2022-06-16
	* *2022-06-17
	* *2022-06-18
	* *2022-06-19
	* *2022-06-20
	* *2022-06-21
	* *2022-06-22
	* *2022-06-23
	* *2022-06-24
	* 2022-07-20

**Block: 1, Entry: 7 data points length: 49**
* Heading date: 2022-06-29
	* 2022-06-13
	* 2022-06-14
	* 2022-06-15
	* *2022-06-16
	* *2022-06-17
	* *2022-06-18
	* *2022-06-19
	* *2022-06-20
	* *2022-06-21
	* *2022-06-22
	* *2022-06-23
	* *2022-06-24
	* 2022-07-20

**Block: 1, Entry: 11 data points length: 49**
* Heading date: 2022-06-30
	* 2022-06-13
	* 2022-06-14
	* 2022-06-15
	* 2022-06-16
	* *2022-06-17
	* *2022-06-18
	* *2022-06-19
	* *2022-06-20
	* *2022-06-21
	* *2022-06-22
	* *2022-06-23
	* *2022-06-24
	* 2022-07-20

**Block: 1, Entry: 3 data points length: 57**
* Heading date: 2022-06-29
	* 2022-06-11
	* 2022-06-13
	* 2022-06-14
	* 2022-08-01

**Block: 1, Entry: 4 data points length: 57**
* Heading date: 2022-06-28
	* 2022-06-11
	* 2022-06-13
	* 2022-06-14
	* 2022-08-01

**Block: 1, Entry: 6 data points length: 57**
* Heading date: 2022-06-25
	* 2022-06-11
	* *2022-06-13
	* *2022-06-14
	* 2022-08-01

**Block: 1, Entry: 8 data points length: 44**
* Heading date: 2022-06-25
	* 2022-06-11
	* *2022-06-13
	* *2022-06-14
	* *2022-06-15
	* 2022-07-21
	* 2022-07-22

**Block: 1, Entry: 12 data points length: 44**
* Heading date: 2022-06-25
	* 2022-06-11
	* *2022-06-13
	* *2022-06-14
	* *2022-06-15
	* 2022-07-21
	* 2022-07-22

**Block: 1, Entry: 2 data points length: 44**
* Heading date: 2022-06-26
	* 2022-06-11
	* *2022-06-13
	* *2022-06-14
	* *2022-06-15
	* 2022-07-21
	* 2022-07-22

**Block: 1, Entry: 5 data points length: 55**
* Heading date: 2022-06-30
	* 2022-06-13
	* 2022-06-15
	* 2022-06-16
	* *2022-06-17
	* *2022-06-25
	* *2022-07-08
	* 2022-07-31

**Block: 1, Entry: 10 data points length: 55**
* Heading date: 2022-07-01
	* 2022-06-13
	* 2022-06-15
	* 2022-06-16
	* 2022-06-17
	* *2022-06-25
	* *2022-07-08
	* 2022-07-31

**Block: 1, Entry: 1 data points length: 55**
* Heading date: 2022-06-24
	* *2022-06-13
	* *2022-06-15
	* *2022-06-16
	* *2022-06-17
	* *2022-06-25
	* 2022-07-08
	* 2022-07-31

**Block: 2, Entry: 11 data points length: 56**
* Heading date: 2022-06-30
	* 2022-06-13
	* 2022-06-14
	* 2022-06-15
	* 2022-06-16
	* *2022-06-17
	* 2022-08-02

**Block: 2, Entry: 7 data points length: 56**
* Heading date: 2022-07-01
	* 2022-06-13
	* 2022-06-14
	* 2022-06-15
	* 2022-06-16
	* 2022-06-17
	* 2022-08-02

**Block: 2, Entry: 4 data points length: 56**
* Heading date: 2022-06-28
	* 2022-06-13
	* 2022-06-14
	* *2022-06-15
	* *2022-06-16
	* *2022-06-17
	* 2022-08-02

**Block: 2, Entry: 9 data points length: 57**
* Heading date: 2022-06-25
	* *2022-06-13
	* *2022-06-14
	* *2022-06-15

**Block: 2, Entry: 6 data points length: 57**
* Heading date: 2022-06-24
	* *2022-06-13
	* *2022-06-14
	* *2022-06-15

**Block: 2, Entry: 8 data points length: 57**
* Heading date: 2022-06-25
	* *2022-06-13
	* *2022-06-14
	* *2022-06-15

**Missing all data points for plot Block: 2, Entry: 12**

**Missing all data points for plot Block: 2, Entry: 5**

**Missing all data points for plot Block: 2, Entry: 3**

**Block: 2, Entry: 10 data points length: 57**
* Heading date: 2022-06-30
	* 2022-06-10
	* 2022-06-11
	* 2022-06-13
	* *2022-07-01
	* *2022-07-02

**Block: 2, Entry: 1 data points length: 57**
* Heading date: 2022-06-26
	* 2022-06-10
	* 2022-06-11
	* *2022-06-13
	* *2022-07-01
	* *2022-07-02

**Block: 2, Entry: 2 data points length: 57**
* Heading date: 2022-06-27
	* 2022-06-10
	* 2022-06-11
	* 2022-06-13
	* *2022-07-01
	* *2022-07-02

**Block: 3, Entry: 2 data points length: 59**
* Heading date: 2022-06-28
	* 2022-06-10
	* 2022-06-11
	* 2022-06-13

**Block: 3, Entry: 11 data points length: 59**
* Heading date: 2022-06-29
	* 2022-06-10
	* 2022-06-11
	* 2022-06-13

**Block: 3, Entry: 3 data points length: 59**
* Heading date: 2022-06-29
	* 2022-06-10
	* 2022-06-11
	* 2022-06-13

**Missing all data points for plot Block: 3, Entry: 12**

**Missing all data points for plot Block: 3, Entry: 9**

**Missing all data points for plot Block: 3, Entry: 4**

**Block: 3, Entry: 7 data points length: 59**
* Heading date: 2022-06-30
	* 2022-06-10
	* 2022-06-11
	* 2022-06-13

**Block: 3, Entry: 1 data points length: 59**
* Heading date: 2022-06-24
	* 2022-06-10
	* *2022-06-11
	* *2022-06-13

**Block: 3, Entry: 5 data points length: 59**
* Heading date: 2022-07-01
	* 2022-06-10
	* 2022-06-11
	* 2022-06-13

**Block: 3, Entry: 10 data points length: 43**
* Heading date: 2022-07-01
	* 2022-06-10
	* 2022-06-11
	* 2022-06-12
	* 2022-06-13
	* 2022-06-14
	* 2022-06-15
	* 2022-06-16
	* 2022-06-17
	* *2022-06-21

**Block: 3, Entry: 8 data points length: 43**
* Heading date: 2022-06-27
	* 2022-06-10
	* 2022-06-11
	* 2022-06-12
	* 2022-06-13
	* *2022-06-14
	* *2022-06-15
	* *2022-06-16
	* *2022-06-17
	* *2022-06-21

**Block: 3, Entry: 6 data points length: 43**
* Heading date: 2022-06-24
	* 2022-06-10
	* *2022-06-11
	* *2022-06-12
	* *2022-06-13
	* *2022-06-14
	* *2022-06-15
	* *2022-06-16
	* *2022-06-17
	* *2022-06-21

### Missing data interpolation techniques
The first technique used to fill the missing data was to pull the data from 
another plot of the same variety. If there was still missing data, then the next technique 
was to pull data from external weather sources nearby (to the site location). If there was still
missing data, then linear interpolation was used.

### Date Ranges

**Spring Date Ranges**  
Plot: Block 1 Variety 9
Start date: 2022-06-05
End date: 2022-08-05
Date range: 62

Plot: Block 1 Variety 7
Start date: 2022-06-05
End date: 2022-08-05
Date range: 62

Plot: Block 1 Variety 11
Start date: 2022-06-05
End date: 2022-08-05
Date range: 62

Plot: Block 1 Variety 3
Start date: 2022-06-06
End date: 2022-08-05
Date range: 61

Plot: Block 1 Variety 4
Start date: 2022-06-06
End date: 2022-08-05
Date range: 61

Plot: Block 1 Variety 6
Start date: 2022-06-06
End date: 2022-08-05
Date range: 61

Plot: Block 1 Variety 8
Start date: 2022-06-05
End date: 2022-07-24
Date range: 50

Plot: Block 1 Variety 12
Start date: 2022-06-05
End date: 2022-07-24
Date range: 50

Plot: Block 1 Variety 2
Start date: 2022-06-05
End date: 2022-07-24
Date range: 50

Plot: Block 1 Variety 5
Start date: 2022-06-05
End date: 2022-08-05
Date range: 62

Plot: Block 1 Variety 10
Start date: 2022-06-05
End date: 2022-08-05
Date range: 62

Plot: Block 1 Variety 1
Start date: 2022-06-05
End date: 2022-08-05
Date range: 62

Plot: Block 2 Variety 11
Start date: 2022-06-05
End date: 2022-08-05
Date range: 62

Plot: Block 2 Variety 7
Start date: 2022-06-05
End date: 2022-08-05
Date range: 62

Plot: Block 2 Variety 4
Start date: 2022-06-05
End date: 2022-08-05
Date range: 62

Plot: Block 2 Variety 9
Start date: 2022-06-07
End date: 2022-08-05
Date range: 60

Plot: Block 2 Variety 6
Start date: 2022-06-07
End date: 2022-08-05
Date range: 60

Plot: Block 2 Variety 8
Start date: 2022-06-07
End date: 2022-08-05
Date range: 60

Plot: Block 2 Variety 10
Start date: 2022-06-05
End date: 2022-08-05
Date range: 62

Plot: Block 2 Variety 1
Start date: 2022-06-05
End date: 2022-08-05
Date range: 62

Plot: Block 2 Variety 2
Start date: 2022-06-05
End date: 2022-08-05
Date range: 62

Plot: Block 3 Variety 2
Start date: 2022-06-05
End date: 2022-08-05
Date range: 62

Plot: Block 3 Variety 11
Start date: 2022-06-05
End date: 2022-08-05
Date range: 62

Plot: Block 3 Variety 3
Start date: 2022-06-05
End date: 2022-08-05
Date range: 62

Plot: Block 3 Variety 7
Start date: 2022-06-05
End date: 2022-08-05
Date range: 62

Plot: Block 3 Variety 1
Start date: 2022-06-05
End date: 2022-08-05
Date range: 62

Plot: Block 3 Variety 5
Start date: 2022-06-05
End date: 2022-08-05
Date range: 62

Plot: Block 3 Variety 10
Start date: 2022-06-05
End date: 2022-07-26
Date range: 52

Plot: Block 3 Variety 8
Start date: 2022-06-05
End date: 2022-07-26
Date range: 52

Plot: Block 3 Variety 6
Start date: 2022-06-05
End date: 2022-07-26
Date range: 52

**Winter Date Ranges**  
Plot: Block 1 Variety 1
Start date: 2022-05-12
End date: 2022-07-31
Date range: 81

Plot: Block 1 Variety 2
Start date: 2022-05-12
End date: 2022-07-31
Date range: 81

Plot: Block 1 Variety 3
Start date: 2022-05-12
End date: 2022-07-31
Date range: 81

Plot: Block 1 Variety 4
Start date: 2022-05-12
End date: 2022-07-31
Date range: 81

Plot: Block 1 Variety 5
Start date: 2022-05-12
End date: 2022-07-30
Date range: 80

Plot: Block 1 Variety 6
Start date: 2022-05-12
End date: 2022-07-30
Date range: 80

Plot: Block 1 Variety 7
Start date: 2022-05-12
End date: 2022-07-30
Date range: 80

Plot: Block 1 Variety 8
Start date: 2022-05-12
End date: 2022-07-30
Date range: 80

Plot: Block 2 Variety 4
Start date: 2022-05-12
End date: 2022-07-31
Date range: 81

Plot: Block 2 Variety 5
Start date: 2022-05-12
End date: 2022-07-31
Date range: 81

Plot: Block 2 Variety 8
Start date: 2022-05-12
End date: 2022-07-31
Date range: 81

Plot: Block 2 Variety 7
Start date: 2022-05-12
End date: 2022-07-31
Date range: 81

Plot: Block 2 Variety 2
Start date: 2022-05-12
End date: 2022-07-31
Date range: 81

Plot: Block 2 Variety 3
Start date: 2022-05-12
End date: 2022-07-31
Date range: 81

Plot: Block 2 Variety 1
Start date: 2022-05-12
End date: 2022-07-31
Date range: 81

Plot: Block 2 Variety 6
Start date: 2022-05-12
End date: 2022-07-31
Date range: 81

Plot: Block 3 Variety 5
Start date: 2022-05-12
End date: 2022-07-30
Date range: 80

Plot: Block 3 Variety 3
Start date: 2022-05-12
End date: 2022-07-30
Date range: 80

Plot: Block 3 Variety 7
Start date: 2022-05-12
End date: 2022-07-30
Date range: 80

Plot: Block 3 Variety 1
Start date: 2022-05-12
End date: 2022-07-30
Date range: 80
