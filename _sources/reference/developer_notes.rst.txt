Developer Notes
===============

Last updated: 10 August 2020

Reproducibility Files
---------------------

Store information for reproducibility. This should include the following:
    1. version information (git hash of commit)
    2. forecast filename
    3. evaluation catalog (including necessary information to recreate the filtering properties); maybe just md5
    4. do we need calculation dates?

Evaluation Results
------------------

* Each evaluation should return an evaluation result class that has an associated .plot() method.
* We should be able to .plot() most everything that makes sense including forecasts and evaluation results.

    * How do we .plot() a catalog?
    * Should we .plot() a region?
    * For serialization, we can identify the appropriate class as a string in the class state and use that to create the correct object on load.

Forecast metadata information
-----------------------------

1. Forecast should contain metadata information to identify properties of the forecast

    * Start and end date
    * Spatial region
    * Magnitude bins

Working with GriddedForecasts
-----------------------------

* Right now, we can only spatial counts over the entire magnitude range. What if we wanted to have some control over this?
* Might want to plot above some magnitude threshold or within some incremental threshold.
* Should be able to have a method that returns a new GriddedForecast with specified parameters such as min/max magnitude.

Region information
------------------
* The region information will need to accommodate more complex spaces including 3D areas and those with non-regular grids (e.g.,
  quadtrees or meshes)

