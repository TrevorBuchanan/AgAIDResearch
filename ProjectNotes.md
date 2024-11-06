
# Project Notes:

**NOTICE:**
This project was originally intended to be a yield prediction program only. The image processing portions were part 
of another project. The code for both is in this project because both took place during the same AgAID research 
internship.

### Table of Contents:
<!-- TOC -->
* [Project Notes:](#project-notes)
    * [Table of Contents:](#table-of-contents)
  * [Time Series Yield Prediction](#time-series-yield-prediction)
    * [Overview Notes:](#overview-notes)
    * [Units and labels:](#units-and-labels)
    * [Models' Results Notes:](#models-results-notes)
    * [VI to Yield Correlation Notes:](#vi-to-yield-correlation-notes)
    * [Missing Data Points Notes For Winter Wheat:](#missing-data-points-notes-for-winter-wheat)
    * [Missing Data Points Notes For Sping Wheat:](#missing-data-points-notes-for-sping-wheat)
    * [Missing Data Interpolation Techniques:](#missing-data-interpolation-techniques)
    * [Date Ranges](#date-ranges)
  * [Object Detection](#object-detection)
    * [Overview Notes:](#overview-notes-1)
    * [Image Processing](#image-processing)
    * [Machine Learning](#machine-learning)
<!-- TOC -->

## Time Series Yield Prediction

### Overview Notes:
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
NOTE: For quick reference, the best winter wheat model is model 14 which was trained on dataset 8, and the best
spring wheat model is model 1 which was trained on dataset 1. 

**Saved data sets 1: Trained on raw training data**  
Number of testing sets: 6, Number of training sets: 24

* model_1
  * Spring wheat, [ndvi] target variate, Vanilla LSTM model
   * Training Data Results: 
        * Model average percent error: 3.32
        * Model average RMSE: 3.65 bu/ac
        * Most accurate date: 189 Julian or 2022-07-08
        * Average accuracy (percent error) at best date: 0.23
        * Average accuracy (RMSE) at best date: 0.19 bu/ac
   * Testing Data Results:
        * Model average percent error: 3.41
        * Model average RMSE: 3.30 bu/ac
        * Most accurate date: 188 Julian or 2022-07-07
        * Average accuracy (percent error) at best date: 0.15
        * Average accuracy (RMSE) at best date: 0.12 bu/ac


* model_7
  * Spring wheat, [ndvi] target variate, Stacked LSTM model
   * Training Data Results: 
        * Model average percent error: 5.33
        * Model average RMSE: 4.86 bu/ac
        * Most accurate date: 184 Julian or 2022-07-03
        * Average accuracy (percent error) at best date: 1.34
        * Average accuracy (RMSE) at best date: 1.01 bu/ac
   * Testing Data Results:
        * Model average percent error: 4.66
        * Model average RMSE: 3.99 bu/ac
        * Most accurate date: 171 Julian or 2022-06-20
        * Average accuracy (percent error) at best date: 1.02
        * Average accuracy (RMSE) at best date: 0.78 bu/ac


**Saved data sets 2: Trained on cut training data (form of SMOTE)**  
Number of testing sets: 23, Number of training sets: 7

* model_3
  * Spring wheat, [ndvi] target variate, Vanilla LSTM model
   * Training Data Results: 
        * Model average percent error: 2.79
        * Model average RMSE: 3.6 bu/ac
        * Most accurate date: 197 Julian or 2022-07-16
        * Average accuracy (percent error) at best date: 0.05
        * Average accuracy (RMSE) at best date: 0.04 bu/ac
   * Testing Data Results:
        * Model average percent error: 10.74
        * Model average RMSE: 9.56 bu/ac
        * Most accurate date: 171 Julian or 2022-06-20
        * Average accuracy (percent error) at best date: 2.2
        * Average accuracy (RMSE) at best date: 1.88 bu/ac


* model_9
  * Spring wheat, [ndvi] target variate, Stacked LSTM model 
   * Training Data Results: 
        * Model average percent error: 10.37
        * Model average RMSE: 8.28 bu/ac
        * Most accurate date: 184 Julian or 2022-07-03
        * Average accuracy (percent error) at best date: 4.25
        * Average accuracy (RMSE) at best date: 3.06 bu/ac
   * Testing Data Results:
        * Model average percent error: 10.2
        * Model average RMSE: 8.87 bu/ac
        * Most accurate date: 183 Julian or 2022-07-02
        * Average accuracy (percent error) at best date: 2.97
        * Average accuracy (RMSE) at best date: 2.38 bu/ac


**Saved data sets 3: Trained on bulked training data (form of SMOTE)**   
Number of testing sets: 6, Number of training sets: 49

* model_5
  * Spring wheat, [ndvi] target variate, Vanilla LSTM model 
   * Training Data Results: 
        * Model average percent error: 2.23
        * Model average RMSE: 2.75 bu/ac
        * Most accurate date: 181 Julian or 2022-06-30
        * Average accuracy (percent error) at best date: 0.19
        * Average accuracy (RMSE) at best date: 0.15 bu/ac
   * Testing Data Results:
        * Model average percent error: 9.43
        * Model average RMSE: 8.29 bu/ac
        * Most accurate date: 166 Julian or 2022-06-15
        * Average accuracy (percent error) at best date: 5.86
        * Average accuracy (RMSE) at best date: 5.05 bu/ac


* model_11
  * Spring wheat, [ndvi] target variate, Stacked LSTM model
   * Training Data Results: 
        * Model average percent error: 3.51
        * Model average RMSE: 3.43 bu/ac
        * Most accurate date: 177 Julian or 2022-06-26
        * Average accuracy (percent error) at best date: 0.76
        * Average accuracy (RMSE) at best date: 0.55 bu/ac
   * Testing Data Results:
        * Model average percent error: 12.54
        * Model average RMSE: 10.63 bu/ac
        * Most accurate date: 171 Julian or 2022-06-20
        * Average accuracy (percent error) at best date: 5.55
        * Average accuracy (RMSE) at best date: 4.71 bu/ac


**Saved data sets 4: Trained on raw training data**  
Number of testing sets: 4, Number of training sets: 16

* model_2
  * Winter wheat, [ndvi] target variate, Vanilla LSTM model
   * Training Data Results: 
        * Model average percent error: 4.05
        * Model average RMSE: 5.93 bu/ac
        * Most accurate date: 163 Julian or 2022-06-12
        * Average accuracy (percent error) at best date: 1.43
        * Average accuracy (RMSE) at best date: 1.8 bu/ac
   * Testing Data Results:
        * Model average percent error: 22.57
        * Model average RMSE: 30.35 bu/ac
        * Most accurate date: 156 Julian or 2022-06-05
        * Average accuracy (percent error) at best date: 16.28
        * Average accuracy (RMSE) at best date: 21.72 bu/ac


* model_8
  * Winter wheat, [ndvi] target variate, Stacked LSTM model
   * Training Data Results: 
        * Model average percent error: 6.1
        * Model average RMSE: 8.21 bu/ac
        * Most accurate date: 158 Julian or 2022-06-07
        * Average accuracy (percent error) at best date: 3.51
        * Average accuracy (RMSE) at best date: 4.66 bu/ac
   * Testing Data Results:
        * Model average percent error: 20.88
        * Model average RMSE: 28.16 bu/ac
        * Most accurate date: 148 Julian or 2022-05-28
        * Average accuracy (percent error) at best date: 13.85
        * Average accuracy (RMSE) at best date: 18.65 bu/ac


**Saved data sets 5: Trained on cut training data (form of SMOTE)**  
Number of testing sets: 13, Number of training sets: 7

* model_4
  * Winter wheat, [ndvi] target variate, Vanilla LSTM model
   * Training Data Results: 
        * Model average percent error: 7.53
        * Model average RMSE: 10.85 bu/ac
        * Most accurate date: 200 Julian or 2022-07-19
        * Average accuracy (percent error) at best date: 1.33
        * Average accuracy (RMSE) at best date: 1.88 bu/ac
   * Testing Data Results:
        * Model average percent error: 9.2
        * Model average RMSE: 13.08 bu/ac
        * Most accurate date: 167 Julian or 2022-06-16
        * Average accuracy (percent error) at best date: 2.96
        * Average accuracy (RMSE) at best date: 4.01 bu/ac


* model_10
  * Winter wheat, [ndvi] target variate, Stacked LSTM model 
   * Training Data Results: 
        * Model average percent error: 4.81
        * Model average RMSE: 7.54 bu/ac
        * Most accurate date: 177 Julian or 2022-06-26
        * Average accuracy (percent error) at best date: 1.08
        * Average accuracy (RMSE) at best date: 1.52 bu/ac


   * Testing Data Results:
        * Model average percent error: 15.44
        * Model average RMSE: 19.36 bu/ac
        * Most accurate date: 147 Julian or 2022-05-27
        * Average accuracy (percent error) at best date: 8.02
        * Average accuracy (RMSE) at best date: 9.53 bu/ac


**Saved data sets 6: Trained on bulked training data (form of SMOTE)**  
Number of testing sets: 4, Number of training sets: 21

* model_6
  * Winter wheat, [ndvi] target variate, Vanilla LSTM model
   * Training Data Results: 
        * Model average percent error: 3.62
        * Model average RMSE: 6.56 bu/ac
        * Most accurate date: 183 Julian or 2022-07-02
        * Average accuracy (percent error) at best date: 0.19
        * Average accuracy (RMSE) at best date: 0.27 bu/ac
   * Testing Data Results:
        * Model average percent error: 8.65
        * Model average RMSE: 12.94 bu/ac
        * Most accurate date: 160 Julian or 2022-06-09
        * Average accuracy (percent error) at best date: 2.87
        * Average accuracy (RMSE) at best date: 3.98 bu/ac


* model_12
  * Winter wheat, [ndvi] target variate, Stacked LSTM model
   * Training Data Results: 
        * Model average percent error: 9.47
        * Model average RMSE: 12.69 bu/ac
        * Most accurate date: 163 Julian or 2022-06-12
        * Average accuracy (percent error) at best date: 4.87
        * Average accuracy (RMSE) at best date: 6.38 bu/ac
   * Testing Data Results:
        * Model average percent error: 6.68
        * Model average RMSE: 9.71 bu/ac
        * Most accurate date: 171 Julian or 2022-06-20
        * Average accuracy (percent error) at best date: 3.22
        * Average accuracy (RMSE) at best date: 4.45 bu/ac


**Saved data sets 7: Trained on raw data**  
Number of testing sets: 6, Number of training sets: 24
* model_13
  * Spring wheat, [cigreen0, cigreen, evi2, gndvi0, gndvi, ndvi, rdvi, savi, sr] target variates, Vanilla LSTM model 
   * Training Data Results: 
        * Model average percent error: 2.19
        * Model average RMSE: 2.43 bu/ac
        * Most accurate date: 177 Julian or 2022-06-26
        * Average accuracy (percent error) at best date: 0.7
        * Average accuracy (RMSE) at best date: 0.59 bu/ac
   * Testing Data Results:
        * Model average percent error: 12.42
        * Model average RMSE: 9.62 bu/ac
        * Most accurate date: 168 Julian or 2022-06-17
        * Average accuracy (percent error) at best date: 8.13
        * Average accuracy (RMSE) at best date: 6.19 bu/ac


* model_15
  * Spring wheat, [cigreen0, cigreen, evi2, gndvi0, gndvi, ndvi, rdvi, savi, sr] target variates, Stacked LSTM model
   * Training Data Results: 
        * Model average percent error: 2.87
        * Model average RMSE: 2.87 bu/ac
        * Most accurate date: 188 Julian or 2022-07-07
        * Average accuracy (percent error) at best date: 0.21
        * Average accuracy (RMSE) at best date: 0.16 bu/ac
   * Testing Data Results:
        * Model average percent error: 13.5
        * Model average RMSE: 10.0 bu/ac
        * Most accurate date: 183 Julian or 2022-07-02
        * Average accuracy (percent error) at best date: 9.81
        * Average accuracy (RMSE) at best date: 6.96 bu/ac

    
**Saved data sets 8: Trained on raw data**  
Number of testing sets: 4, Number of training sets: 16

* model_14
  * Winter wheat, [cigreen0, cigreen, evi2, gndvi0, gndvi, ndvi, rdvi, savi, sr] target variates, Vanilla LSTM model
  * Training Data Results: 
      * Model average percent error: 3.63
      * Model average RMSE: 6.35 bu/ac
      * Most accurate date: 169 Julian or 2022-06-18
      * Average accuracy (percent error) at best date: 0.17
      * Average accuracy (RMSE) at best date: 0.20 bu/ac
  * Testing Data Results:
      * Model average percent error: 1.61
      * Model average RMSE: 3.11 bu/ac
      * Most accurate date: 172 Julian or 2022-06-21
      * Average accuracy (percent error) at best date: 0.03
      * Average accuracy (RMSE) at best date: 0.04 bu/ac


* model_16
  * Winter wheat, [cigreen0, cigreen, evi2, gndvi0, gndvi, ndvi, rdvi, savi, sr] target variates, Stacked LSTM model
   * Training Data Results: 
        * Model average percent error: 8.07
        * Model average RMSE: 10.75 bu/ac
        * Most accurate date: 159 Julian or 2022-06-08
        * Average accuracy (percent error) at best date: 5.4
        * Average accuracy (RMSE) at best date: 6.96 bu/ac
   * Testing Data Results:
        * Model average percent error: 5.48
        * Model average RMSE: 7.63 bu/ac
        * Most accurate date: 147 Julian or 2022-05-27
        * Average accuracy (percent error) at best date: 2.93
        * Average accuracy (RMSE) at best date: 3.99 bu/ac


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

### Missing Data Interpolation Techniques:
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

### Overview Notes:
* The machine learning object detection portion of this project was done near the end, so the testing of
the models was very limited. 
* The machine learning data was trained on data annotated with RoboFlow and can be found here https://app.roboflow.com/agaid-image-processing/agaid-object-detection/1
* The annotated data set has also been saved to [AnnotatedReferencePanelData](AnnotatedReferencePanelData)
* Although little tested, the machine learning models for object detection performed so much better than the image 
processing object detection that the image processing object detection approach is obsolete.


### Image Processing
**Approaches Taken:**
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

**Final Approach:**
* Get working image (cut down size)
* Split into color channels (RGB and gray)
* For each color channel:
  * Get uniform values mask
  * Get contours 
  * Filter lonelies (Get rid of random noisy pixels )
  * Get valid areas
  * Get bounding rectangles
* Merge all valid rectangles
* Remove duplicates
* Filter rectangles for each color channel 
  * Filter by uniform values (make sure values within rectangle are uniform)
  * Filter by pixel range (panel rectangles should have low pixel range)
  * Filter by edges (find difference between inside edge of rect and outside to make sure rectangle encompasses a panel)
* Remove duplicates
* Return remaining valid rectangles 

**Usage Examples:**
* Correct Result Example:
  ![ImageProcessingCorrect.png](ProjectDataImages%2FImageProcessingCorrect.png)

* Incorrect Result Example:
  ![ImageProcessingIncorrect.png](ProjectDataImages%2FImageProcessingIncorrect.png)


### Machine Learning
* **RoboFlow Object Detection Fast**
* Results:
  * 100% accurate on all test data
  * Example:
	![RoboFlowDetectedEx.jpg](ProjectDataImages%2FRoboFlowDetectedEx.jpg)

* **Custom YOLOv5 m**
* Results:
  * 100% accurate on all test data
  * Example:
	![CustomYOLODetectedEx.png](ProjectDataImages%2FCustomYOLODetectedEx.png)
