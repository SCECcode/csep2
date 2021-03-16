"""

.. _grid-forecast-evaluation:

Grid-based Forecast Evaluation
==============================

This example demonstrates how to evaluate a grid-based and time-independent forecast. Grid-based
forecasts assume the variability of the forecasts is Poissonian. Therefore, Poisson-based evaluations
should be used to evaluate grid-based forecasts.

Overview:
    1. Define forecast properties (time horizon, spatial region, etc).
    2. Obtain evaluation catalog
    3. Apply Poissonian evaluations for grid-based forecasts
    4. Store evaluation results using JSON format
    5. Visualize evaluation results
"""

####################################################################################################################################
# Load required libraries
# -----------------------
#
# Most of the core functionality can be imported from the top-level :mod:`csep` package. Utilities are available from the
# :mod:`csep.utils` subpackage.

import csep
from csep.core import poisson_evaluations as poisson
from csep.utils import datasets, time_utils, plots

####################################################################################################################################
# Define forecast properties
# --------------------------
#
# We choose a :ref:`time-independent-forecast` to show how to evaluate a grid-based earthquake forecast using PyCSEP. Note,
# the start and end date should be chosen based on the creation of the forecast. This is important for time-independent forecasts
# because they can be rescale to any arbitrary time period.

start_date = time_utils.strptime_to_utc_datetime('2006-11-12 00:00:00.0')
end_date = time_utils.strptime_to_utc_datetime('2011-11-12 00:00:00.0')

####################################################################################################################################
# Load forecast
# -------------
#
# For this example, we provide the example forecast data set along with the main repository. The filepath is relative
# to the root directory of the package. You can specify any file location for your forecasts.

forecast = csep.load_gridded_forecast(datasets.helmstetter_aftershock_fname,
                                      start_date=start_date,
                                      end_date=end_date,
                                      name='helmstetter_aftershock')

####################################################################################################################################
# Load evaluation catalog
# -----------------------
#
# We will download the evaluation catalog from ComCat (this step requires an internet connection). We can use the ComCat API
# to filter the catalog in both time and magnitude. See the catalog filtering example, for more information on how to
# filter the catalog in space and time manually.

catalog = csep.query_comcat(forecast.start_time, forecast.end_time,
                            min_magnitude=forecast.min_magnitude)
print(catalog)

####################################################################################################################################
# Filter evaluation catalog in space
# ----------------------------------
#
# We need to remove events in the evaluation catalog outside the valid region specified by the forecast.

catalog = catalog.filter_spatial(forecast.region)
print(catalog)

####################################################################################################################################
# Compute Poisson spatial test
# ----------------------------
#
# Simply call the :func:`csep.core.poisson_evaluations.spatial_test` function to evaluate the forecast using the specified
# evaluation catalog. The spatial test requires simulating from the Poisson forecast to provide uncertainty. The verbose
# option prints the status of the simulations to the standard output.

spatial_test_result = poisson.spatial_test(forecast, catalog)

####################################################################################################################################
# Store evaluation results
# ------------------------
#
# PyCSEP provides easy ways of storing objects to a JSON format using :func:`csep.write_json`. The evaluations can be read
# back into the program for plotting using :func:`csep.load_evaluation_result`.

csep.write_json(spatial_test_result, 'example_spatial_test.json')

####################################################################################################################################
# Plot spatial test results
# -------------------------
#
# We provide the function :func:`csep.utils.plotting.plot_poisson_consistency_test` to visualize the evaluation results from
# consistency tests.

ax = plots.plot_poisson_consistency_test(spatial_test_result,
                                        plot_args={'xlabel': 'Spatial likelihood'})
