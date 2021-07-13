# Notebook Examples

We recommend you execute these notebooks in the following order.

- [example_01_dfw_demand_data.ipynb](example_01_dfw_demand_data.ipynb) 
This notebook introduces the demand file of vehicles that enter and exit the control plaza from North and South entrances at the Dallas Fort-Worth international Airport (DFW).  This is the data that we are interested in forecasting and has been generously provided by and made public with permission from DFW.

- [example_02_choosing_cross_validation_tests.ipynb](example_02_choosing_cross_validation_tests.ipynb) 
This notebook gives an example of choosing an appropriate cross-validation set for time-series forecasting.  This is a very important step in evaluating algorithms and we discuss the parameters of our input format impact the cross validation test sets.

- [example_03_dataset.ipynb](example_03_dataset.ipynb) builds on the first two notebooks to provide an example of using the Dataset object.  The purpose of this object is to create a consistent interface for utilizing various algorithms.  Each algorithm, of course, will have it's own input required.  The Dataset object is the input for the transformation functions that perform the necessary translation for a specific algorithm.

- [example_04_wavelet_analysis.ipynb](example_04_wavelet_analysis.ipynb).  In this notebook we provide code to perform a wavelet analysis on the data, which in this instance, show very strong daily trends. 

- [example_05_learning_tutorial.ipynb](example_05_learning_tutorial.ipynb).  This final notebook shows an example of how to use our configuration and code to execute a dataset on a variety of algorithms.





