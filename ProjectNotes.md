
# Project Notes:

**NOTICE:**
This project was originally intended to be a yield prediction program only. The image processing portions were part 
of another project. The code for both is in this project because both took place during the same AgAID research 
internship.

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
![SpringDist.png](ProjectDataImages%2FSpringDist.png)
In order to fix the issue of there being 
less data points on the extremities for the ML model to train on, minority oversampling was used. The minority 
sampling was done in two ways. Firstly, the data was cut down so that the distribution was level, as shown below.
![CutDist.png](ProjectDataImages%2FCutDist.png)
Secondly, the distribution was leveled by fabricating minority data.
![BulkDist.png](ProjectDataImages%2FBulkDist.png)
As an extra frame of reference, below is the winter yield distribution as well:
![WinterDist.png](ProjectDataImages%2FWinterDist.png)
* The way the RMSE is calculated for the error in this project is by getting the RMSE value for the predictions vs 
actual values of yield of each time step (day) for each plot, and then taking the average of those RMSE values for all 
the plots. 

### Units and labels:
 - Temperatures: Celsius
 - Yield: Bushels/Acre (bu/ac)
 - Soil temperature depth: Inches
 - Plant height: Inches
 - Plot area: Square feet
 - IoT: Internet of Things

### Models' Results Notes:


**Saved data sets 1: Trained on raw training data**  
Number of testing sets: 6, Number of training sets: 24

* model_1
  * Spring wheat, [ndvi] target variate, Vanilla LSTM model
  * Model average percent error (testing data): 3.41
  * Model average RMSE (testing data): 3.30 bu/ac
  * Most accurate date (training data): 188 or 2022-07-07 
  * Average accuracy (percent error) at best date (testing data): 0.15
  * Model average percent error (training data): 3.32
  * Model average RMSE (training data): 3.65 bu/ac
  * Most accurate date (training data): 189 or 2022-07-08 
  * Average accuracy (percent error) at best date (training data): 0.23

* model_7
  * Spring wheat, [ndvi] target variate, Stacked LSTM model
  * Model average percent error (testing data): 4.66
  * Model average RMSE (testing data): 3.99 bu/ac
  * Most accurate date (training data): 171 or 2022-06-20 
  * Average accuracy (percent error) at best date (testing data): 1.02
  * Model average percent error (training data): 5.33
  * Model average RMSE (training data): 4.86 bu/ac
  * Most accurate date (training data): 184 or 2022-07-03 
  * Average accuracy (percent error) at best date (training data): 1.34

**Saved data sets 2: Trained on cut training data (form of SMOTE)**  
Number of testing sets: 23, Number of training sets: 7

* model_3
  * Spring wheat, [ndvi] target variate, Vanilla LSTM model
  * Model average percent error (testing data): 10.74
  * Model average RMSE (testing data): 9.56 bu/ac
  * Most accurate date (training data): 171 or 2022-06-20 
  * Average accuracy (percent error) at best date (testing data): 2.19
  * Model average percent error (training data): 2.78
  * Model average RMSE (training data): 3.59 bu/ac
  * Most accurate date (training data): 197 or 2022-07-16 
  * Average accuracy (percent error) at best date (training data): 0.05

* model_9
  * Spring wheat, [ndvi] target variate, Stacked LSTM model 
  * Model average percent error (testing data): 10.20
  * Model average RMSE (testing data): 8.87 bu/ac
  * Most accurate date (training data): 183 or 2022-07-02 
  * Average accuracy (percent error) at best date (testing data): 2.97
  * Model average percent error (training data): 10.37
  * Model average RMSE (training data): 8.28 bu/ac
  * Most accurate date (training data): 184 or 2022-07-03 
  * Average accuracy (percent error) at best date (training data): 4.25



**Saved data sets 3: Trained on bulked training data (form of SMOTE)**   
Number of testing sets: 6, Number of training sets: 49

* model_5
  * Spring wheat, [ndvi] target variate, Vanilla LSTM model 
  * Model average percent error (testing data): 9.43
  * Model average RMSE (testing data): 8.29 bu/ac
  * Most accurate date (training data): 166 or 2022-06-15 
  * Average accuracy (percent error) at best date (testing data): 5.86 
  * Model average percent error (training data): 2.23
  * Model average RMSE (training data): 2.75 bu/ac
  * Most accurate date (training data): 181 or 2022-06-30 
  * Average accuracy (percent error) at best date (training data): 0.17

* model_11
  * Spring wheat, [ndvi] target variate, Stacked LSTM model
  * Model average percent error (testing data): 12.54
  * Model average RMSE (testing data): 10.63 bu/ac
  * Most accurate date (training data): 171 or 2022-06-20 
  * Average accuracy (percent error) at best date (testing data): 5.55
  * Model average percent error (training data): 3.51
  * Model average RMSE (training data): 3.43 bu/ac
  * Most accurate date (training data): 177 or 2022-06-26 
  * Average accuracy (percent error) at best date (training data): 0.76


**Saved data sets 4: Trained on raw training data**  
Number of testing sets: 4, Number of training sets: 16

* model_2
  * Winter wheat, [ndvi] target variate, Vanilla LSTM model
  * Model average percent error (testing data): 22.57
  * Model average RMSE (testing data): 30.35 bu/ac
  * Most accurate date (training data): 156 or 2022-06-05 
  * Average accuracy (percent error) at best date (testing data): 16.28
  * Model average percent error (training data): 4.05
  * Model average RMSE (training data): 5.93 bu/ac
  * Most accurate date (training data): 163 or 2022-06-12 
  * Average accuracy (percent error) at best date (training data): 1.43

* model_8
  * Winter wheat, [ndvi] target variate, Stacked LSTM model
  * Model average percent error (testing data): 20.88
  * Model average RMSE (testing data): 28.16 bu/ac
  * Most accurate date (training data): 148 or 2022-05-28 
  * Average accuracy (percent error) at best date (testing data): 13.85
  * Model average percent error (training data): 6.10
  * Model average RMSE (training data): 8.21 bu/ac
  * Most accurate date (training data): 158 or 2022-06-07 
  * Average accuracy (percent error) at best date (training data): 3.51


**Saved data sets 5: Trained on cut training data (form of SMOTE)**  
Number of testing sets: 13, Number of training sets: 7

* model_4
  * Winter wheat, [ndvi] target variate, Vanilla LSTM model
  * Model average percent error (testing data): 9.20
  * Model average RMSE (testing data): 13.08 bu/ac
  * Most accurate date (training data): 167 or 2022-06-16
  * Average accuracy (percent error) at best date (testing data): 2.96
  * Model average percent error (training data): 7.53
  * Model average RMSE (training data): 10.85 bu/ac
  * Most accurate date (training data): 200 or 2022-07-19
  * Average accuracy (percent error) at best date (training data): 1.33

* model_10
  * Winter wheat, [ndvi] target variate, Stacked LSTM model 
  * Model average percent error (testing data): 15.44
  * Model average RMSE (testing data): 19.36 bu/ac
  * Most accurate date (training data): 147 or 2022-05-27 
  * Average accuracy (percent error) at best date (testing data): 8.02
  * Model average percent error (training data): 4.8
  * Model average RMSE (training data): 7.54 bu/ac
  * Most accurate date (training data): 177 or 2022-06-26 
  * Average accuracy (percent error) at best date (training data): 1.08


**Saved data sets 6: Trained on bulked training data (form of SMOTE)**  
Number of testing sets: 4, Number of training sets: 21

* model_6
  * Winter wheat, [ndvi] target variate, Vanilla LSTM model
  * Model average percent error (testing data): 8.65 
  * Model average RMSE (testing data): 12.94 bu/ac
  * Most accurate date (training data): 160 or 2022-06-09 
  * Average accuracy (percent error) at best date (testing data): 2.87 
  * Model average percent error (training data): 3.62
  * Model average RMSE (training data): 6.56 bu/ac
  * Most accurate date (training data): 183 or 2022-07-02 
  * Average accuracy (percent error) at best date (training data): 0.19

* model_12
  * Winter wheat, [ndvi] target variate, Stacked LSTM model
  * Model average percent error (testing data): 6.68
  * Model average RMSE (testing data): 9.71 bu/ac
  * Most accurate date (training data): 171 or 2022-06-20 
  * Average accuracy (percent error) at best date (testing data): 3.21
  * Model average percent error (training data): 9.46
  * Model average RMSE (training data): 12.69 bu/ac
  * Most accurate date (training data): 163 or 2022-06-12 
  * Average accuracy (percent error) at best date (training data): 4.87

**Saved data sets 7: Trained on raw data**  
Number of testing sets: 6, Number of training sets: 24
* model_13
  * Spring wheat, [cigreen0, cigreen, evi2, gndvi0, gndvi, ndvi, rdvi, savi, sr] target variates, Vanilla LSTM model 
  * Model average percent error (testing data): 12.42
  * Model average RMSE (testing data): 9.62 bu/ac
  * Most accurate date (training data): 168 or 2022-06-17 
  * Average accuracy (percent error) at best date (testing data): 8.13
  * Model average percent error (training data): 2.19
  * Model average RMSE (training data): 2.43 bu/ac
  * Most accurate date (training data): 177 or 2022-06-26 
  * Average accuracy (percent error) at best date (training data): 0.70

* model_15
  * Spring wheat, [cigreen0, cigreen, evi2, gndvi0, gndvi, ndvi, rdvi, savi, sr] target variates, Stacked LSTM model
  * Model average percent error (testing data): 13.50
  * Model average RMSE (testing data): 10.00 bu/ac
  * Most accurate date (training data): 183 or 2022-07-02 
  * Average accuracy (percent error) at best date (testing data): 9.81
  * Model average percent error (training data): 2.87
  * Model average RMSE (training data): 2.87 bu/ac
  * Most accurate date (training data): 188 or 2022-07-07 
  * Average accuracy (percent error) at best date (training data): 0.21


**Saved data sets 8: Trained on raw data**  
Number of testing sets: 4, Number of training sets: 16

* model_14
  * Winter wheat, [cigreen0, cigreen, evi2, gndvi0, gndvi, ndvi, rdvi, savi, sr] target variates, Vanilla LSTM model
  * Model average percent error (testing data): 7.50
  * Model average RMSE (testing data): 9.90 bu/ac
  * Most accurate date (training data): 168 or 2022-06-17 
  * Average accuracy (percent error) at best date (testing data): 0.58
  * Model average percent error (training data): 2.16
  * Model average RMSE (training data): 4.66 bu/ac
  * Most accurate date (training data): 170 or 2022-06-19 
  * Average accuracy (percent error) at best date (training data): 0.03

* model_16
  * Winter wheat, [cigreen0, cigreen, evi2, gndvi0, gndvi, ndvi, rdvi, savi, sr] target variates, Stacked LSTM model
  * Model average percent error (testing data): 7.45
  * Model average RMSE (testing data): 9.86 bu/ac
  * Most accurate date (training data): 148 or 2022-05-28 
  * Average accuracy (percent error) at best date (testing data): 3.49
  * Model average percent error (training data): 7.56
  * Model average RMSE (training data): 10.19 bu/ac
  * Most accurate date (training data): 159 or 2022-06-08 
  * Average accuracy (percent error) at best date (training data): 5.26

### VI to Yield Correlation Notes:
Note: Offset means the amount of days from the beginning of the data collection. Split size is the
duration, in days, of how long the best correlation segment is. 

* Spring full data average VI (ndvi) correlation:
![SpringFullDataVItoYield.png](ProjectDataImages%2FSpringFullDataVItoYield.png)


	Pearson correlation coefficient: 0.30

* Spring best split size (4) and offset (40) VI (ndvi) correlation:
![SpringBestSplitSizeVItoYield.png](ProjectDataImages%2FSpringBestSplitSizeVItoYield.png)


	Pearson correlation coefficient: 0.50

* Spring heading data VI correlation: 
![SpringHeadingDateVItoYield.png](ProjectDataImages%2FSpringHeadingDateVItoYield.png)


	Pearson correlation coefficient: -0.51

* Winter full data average VI (ndvi) correlation:
![WinterFullDataVitoYield.png](ProjectDataImages%2FWinterFullDataVitoYield.png)


	Pearson correlation coefficient: 0.53

* Winter best split size (3) and offset (45) VI (ndvi) correlation:
![WinterBestSplitSizeVItoYield.png](ProjectDataImages%2FWinterBestSplitSizeVItoYield.png)


	Pearson correlation coefficient: 0.58

* Winter heading data VI (ndvi) correlation: 
![WinterHeadingDateVItoYield.png](ProjectDataImages%2FWinterHeadingDateVItoYield.png)


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
End date: 2022-08-05 (156 Julian Calender)
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
Start date: 2022-05-12 (132 Julian Calender)
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


## Object Detection

---

### Image Processing
**Approaches Taken**
* Uniform values mask - Using the fact that the panels' pixel values should be uniform (checks immediate surrounding pixels )
* Contour detection - Finding contours on different levels of processing to validate detection
* Sequential time images - Using the fact that the panel should be located in similar 
locations on the previous and next time points
* Left and Right symmetry - The images have two halves, left NIR, and right RGB. The location of the panel should be
similar for the left and right images because they are taken at the same time from the same location
* Post detection - The panels are all help up by a post, so detecting the post should help show where the panel is
* Edge detection - Using pixel difference of the panels' edges and outside the edges
* Area, width, height - Used to filter possible detected panels to specified size range
* Color channel splits - Using different color channels to find panels
* Duplicate filter - Choosing possible panels found based off of how many bounding rectangles found at that location
* Pixel range filter - Choosing the possible panels that have the lowest pixel range (should be very small because they should be uniform)
* Layered search and filters - Combining panel rect searching levels and filtering levels to get best results

**Usage Example:**



### Machine Learning
* RoboFlow Object Detection Fast
* Custom YOLOv5 m

