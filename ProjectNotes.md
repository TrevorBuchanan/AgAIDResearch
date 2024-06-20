
# Project Notes:

* Spring wheat crop was planted on the 25th of April
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
The distribution of the yields followed a normal distribution (figure 1.0).
  ![NormalDist.png](/Users/trevorbuchanan/Desktop/AgAIDinternship/Images/NormalDist.png)
In order to fix the issue of there being 
less data points on the extremities for the ML model to train on, minority oversampling was used. The minority 
sampling was done in two ways. Firstly, the data was cut down so that the distribution was level, as shown below.
![CutDist.png](/Users/trevorbuchanan/Desktop/AgAIDinternship/Images/CutDist.png)
Secondly, the distribution was leveled by fabricating minority data.
![BulkDist.png](/Users/trevorbuchanan/Desktop/AgAIDinternship/Images/BulkDist.png)


### Units and labels:
 - Temperatures: Celsius
 - Yield: Bushels/Acre
 - Soil temperature depth: Inches
 - Plant height: Inches
 - Plot area: Square feet
 - IoT: Internet of Things


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


### Model Results Notes:

* spring_ndvi_vi_mean_stacked_model
  * Ends with low costs around 9 and val_loss around 12
  * Performs worse compared to vanilla model when testing on unseen data

* spring_ndvi_vi_mean_vanilla_model
  * Ends with high costs around 30 and value costs around 100
  * Performs relatively well on unseen data

* spring_sr_vi_mean_vanilla_model
  * Ends with high costs around 40 and value costs around 30
  * Performs relatively well (but trained on all data, so no data left to
  tedt performance on unseen data)


	
