# AgAID Research Project

### Washington State University

---

**Mentor: Sindhuja Sankaran**

**Research Grad Student Resources**
* Lochana Marasingha
* Chamaporn Paiboonvorachat

By: **Trevor Buchanan**

---

## Project progress summary:
* 06/10/2024 - Familiarization with data and begin to parse
* 06/11/2024 - Continue to parse data and begin create visualizations for it
* 06/12/2024 - Expand and refine visualizations and interpolate between missing 
data with multiple techniques depending on the data type (e.i. vi and temperature 
have very different trajectory paths, so the same interpolation cannot be used 
for both. Furthermore, some information can be filled from other IoT units at the 
site, and other online resources such as weather data)
* 06/13/2024 - Refactor and begin to use time series learning models
* 06/14/2024 - Apply uni-variate time series learning models and work on setting 
* effective parameters for best results
* 06/17/2024 - Attempt to refine parameters of LSTM models and add a stacked LSTM
* 06/18/2024 - Run training tests to refine parameters and training strategy
* 06/20/2024 - Fix issues: 
  * Have training data a testing data be separate between all
  executions (consistent training batch and testing batch)
  * Refactor for organization and clarity
  * Complete all unfinished TODO comments 
* 06/21/2024 - Implement a version of SMOTE (Synthetic Minority Oversampling Technique), further tests of vanilla and stacked
LSTM ML models, further data and ML performance visualizations, and record correlation between VI and yield
* 06/26/2024 - Measure accuracy for models, show variety with results, log training performance, and add correlation at heading date to correlation visualization
* 07/01/2024 - Add winter data correlations to project notes, train winter ML models, add testing and training sizes to project notes
* 07/02/2024 - Fix issues and make advancements:
  * Improve saved model data and better model saving approach
  * Work on weakness-target training
  * Bug and error search; bugs found:
    * Bug fetching predictions where only a few of the predictions would be made, and then the visualizer would fill 
    the rest of the data with the existing values; resulting in skewed accuracy. 
    * Bug where the prediction data would be backwards (according to time, i.e. starting at end, whole data, and 
    ending with beginning (one day of data))
* 07/03/2024 - Log start and end dates of all plots, add ability to normalize any inputs, use r-squared and RMSE
when measuring performance (r-squared not used, but function exists), get all VIs when parsing data and add them
to the visualization (used later for multivariate LSTM model), train models with new changes, further work on weakness-target training
* 07/05/2024 - Bug fixes, train models, add ability to track the best accuracies in testing and training sets and the 
corresponding average of those best accuracies
* 

# References: 
* [1] J. Brownlee, “How to Develop LSTM Models for Time Series Forecasting,” Machine Learning Mastery, Nov. 13, 2018. https://machinelearningmastery.com/how-to-develop-lstm-models-for-time-series-forecasting/

* [2] J. Brownlee, “Gentle Introduction to Models for Sequence Prediction with RNNs,” Machine Learning Mastery, Jul. 16, 2017. https://machinelearningmastery.com/models-sequence-prediction-recurrent-neural-networks/

* [3] C. Olah, “Understanding LSTM Networks,” Github.io, Aug. 27, 2015. https://colah.github.io/posts/2015-08-Understanding-LSTMs/

* [4] Liu, G., Zhong, K., Li, H., Chen, T., Wang Y., 2023b. A state of art review on time series forecasting with machine learning for environmental parameters in agricultural greenhouses. Inf. Process. Agric. https://doi.org/10.1016/j.inpa.2022.10.005.

