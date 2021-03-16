.. _evaluation-reference:

.. automodule:: csep.core.poisson_evaluations

###########
Evaluations
###########

PyCSEP provides routines to evaluate both gridded and catalog-based earthquake forecasts. This page explains how to use
the forecast evaluation routines and also how to build "mock" forecast and catalog classes to accommodate different
custom forecasts and catalogs.

.. contents:: Table of Contents
    :local:
    :depth: 2

.. :currentmodule:: csep

****************************
Gridded-forecast evaluations
****************************

Grid-based earthquake forecasts assume earthquakes occur in discrete space-time-magnitude bins and their rate-of-
occurrence can be defined using a single number in each magnitude bin. Each space-time-magnitude bin is assumed to be
an independent Poisson random variable. Therefore, we use likelihood-based evaluation metrics to compare these
forecasts against observations.

PyCSEP provides two groups of evaluation metrics for grid-based earthquake forecasts. The first are known as
consistency tests and they verify whether a forecast in consistent with an observation. The second are comparative tests
that can be used to compare the performance of two (or more) competing forecasts.
PyCSEP implements the following evaluation routines for grid-based forecasts. These functions are intended to work with
:class:`GriddedForecasts<csep.core.forecasts.GriddedForecast>` and :class:`CSEPCatalogs`<csep.core.catalogs.CSEPCatalog>`.
Visit the :ref:`catalogs reference<catalogs-reference>` and the :ref:`forecasts reference<forecasts-reference>` to learn
more about to import your forecasts and catalogs into PyCSEP.

.. note::
    Grid-based forecast evaluations act directly on the forecasts and catalogs as they are supplied to the function.
    Any filtering of catalogs and/or scaling of forecasts must be done before calling the function.
    This must be done before evaluating the forecast and should be done consistently between all forecasts that are being
    compared.

See the :ref:`example<grid-forecast-evaluation>` for gridded forecast evaluation for an end-to-end walkthrough on how
to evaluate a gridded earthquake forecast.


Consistency tests
=================

.. autosummary::

   number_test
   magnitude_test
   spatial_test
   likelihood_test
   conditional_likelihood_test


Comparative tests
=================

.. autosummary::

   paired_t_test
   w_test

Publication references
======================

1. Number test (:ref:`Schorlemmer et al., 2007<schorlemmer-2007>`; :ref:`Zechar et al., 2010<zechar-2010>`)
2. Magnitude test (:ref:`Zechar et al., 2010<zechar-2010>`)
3. Spatial test (:ref:`Zechar et al., 2010<zechar-2010>`)
4. Likelihood test (:ref:`Schorlemmer et al., 2007<schorlemmer-2007>`; :ref:`Zechar et al., 2010<zechar-2010>`)
5. Conditional likelihood test (:ref:`Werner et al., 2011<werner-2011>`)
6. Paired t test (:ref:`Rhoades et al., 2011<rhoades-2011>`)
7. Wilcoxon signed-rank test (:ref:`Rhoades et al., 2011<rhoades-2011>`)

**********************************
Catalog-based forecast evaluations
**********************************

Catalog-based forecasts are issued as a family of stochastic event sets (synthetic earthquake catalogs) and can express
the full uncertainty of the forecasting model. Additionally, these forecasts retain the inter-event dependencies that
are lost when using discrete space-time-magnitude grids. This problem can impact the evaluation performance of
time-dependent forecasts like the epidemic type aftershock sequence model (ETAS).

In order to support generative or simulator-based models, we define a suite of consistency tests that compare forecasted
distributions against observations without the use of a parametric likelihood function. These evaluations take advantage
of the fact that the forecast and the observations are both earthquake catalogs. Therefore, we can compute identical
statistics from these catalogs and compare them against one another.

We provide four statistics that probe fundamental aspects of the earthquake forecasts. Please see
:ref:`Savran et al., 2020<savran-2020>` for a complete description of the individual tests. For the implementation
details please follow the links below and see the :ref:`example<catalog-forecast-evaluation>` for catalog-based
forecast evaluation for an end-to-end walk through.

.. automodule:: csep.core.catalog_evaluations

Consistency tests
=================

.. autosummary::

   number_test
   spatial_test
   magnitude_test
   pseudolikelihood_test
   calibration_test

Publication reference
=====================

1. Number test (:ref:`Savran et al., 2020`<savran-2020>`)
2. Spatial test (:ref:`Savran et al., 2020`<savran-2020>`)
3. Magnitude test (:ref:`Savran et al., 2020`<savran-2020>`)
4. Pseudolikelihood test (:ref:`Savran et al., 2020`<savran-2020>`)
5. Calibration test (:ref:`Savran et al., 2020`<savran-2020>`)

****************************
Preparing evaluation catalog
****************************

The evaluations in PyCSEP do not implicitly filter the observed catalogs or modify the forecast data when called. For most
cases, the observation catalog should be filtered according to:
    1. Magnitude range of the forecast
    2. Spatial region of the forecast
    3. Start and end-time of the forecast

Once the observed catalog is filtered so it is consistent in space, time, and magnitude as the forecast, it can be used
to evaluate a forecast. A single evaluation catalog can be used to evaluate multiple forecasts so long as they all cover
the same space, time, and magnitude region.

*********************
Building mock classes
*********************

Python is a duck-typed language which means that it doesn't care what the object type is only that it has the methods or
functions that are expected when that object is used. This can come in handy if you want to use the evaluation methods, but
do not have a forecast that completely fits with the forecast classes (or catalog classes) provided by PyCSEP.

.. note::
    Something about great power and great responsibility... For the most reliable results, write a loader function that
    can ingest your forecast into the model provided by PyCSEP. Mock-classes can work, but should only be used in certain
    circumstances. In particular, they are very useful for writing software tests or to prototype features that can
    be added into the package.

This section will walk you through how to compare two forecasts using the :func:`paired_t_test<csep.core.poisson_evaluations>`
with mock forecast and catalog classes. This sounds much more complex than it really is, and it gives you the flexibility
to use your own formats and interact with the tools provided by PyCSEP.

.. warning::

    The simulation-based Poisson tests (magnitude_test, likelihood_test, conditional_likelihood_test, and spatial_test)
    are optimized to work with forecasts that contain equal-sized spatial bins. If your forecast uses variable sized spatial
    bins you will get incorrect results. If you are working with forecasts that have variable spatial bins, create an
    issue on GitHub because we'd like to implement this feature into the toolkit and we'd love your help.

If we look at the :func:`paired_t_test<csep.core.poisson_evaluations>` we see that it has the following code ::

    def paired_t_test(gridded_forecast1, gridded_forecast2, observed_catalog, alpha=0.05, scale=False):
        """ Computes the t-test for gridded earthquake forecasts.

        Args:
            gridded_forecast_1 (csep.core.forecasts.GriddedForecast): nd-array storing gridded rates, axis=-1 should be the magnitude column
            gridded_forecast_2 (csep.core.forecasts.GriddedForecast): nd-array storing gridded rates, axis=-1 should be the magnitude column
            observed_catalog (csep.core.catalogs.AbstractBaseCatalog): number of observed earthquakes, should be whole number and >= zero.
            alpha (float): tolerance level for the type-i error rate of the statistical test
            scale (bool): if true, scale forecasted rates down to a single day

        Returns:
            evaluation_result: csep.core.evaluations.EvaluationResult
        """

        # needs some pre-processing to put the forecasts in the context that is required for the t-test. this is different
        # for cumulative forecasts (eg, multiple time-horizons) and static file-based forecasts.
        target_event_rate_forecast1, n_fore1 = gridded_forecast1.target_event_rates(observed_catalog, scale=scale)
        target_event_rate_forecast2, n_fore2 = gridded_forecast2.target_event_rates(observed_catalog, scale=scale)

        # call the primative version operating on ndarray
        out = _t_test_ndarray(target_event_rate_forecast1, target_event_rate_forecast2, observed_catalog.event_count, n_fore1, n_fore2,
                              alpha=alpha)

        # prepare evaluation result object
        result = EvaluationResult()
        result.name = 'Paired T-Test'
        result.test_distribution = (out['ig_lower'], out['ig_upper'])
        result.observed_statistic = out['information_gain']
        result.quantile = (out['t_statistic'], out['t_critical'])
        result.sim_name = (gridded_forecast1.name, gridded_forecast2.name)
        result.obs_name = observed_catalog.name
        result.status = 'normal'
        result.min_mw = numpy.min(gridded_forecast1.magnitudes)

Notice that the function expects two forecast objects and one catalog object. The ``paired_t_test`` function calls a
method on the forecast objects named :meth:`target_event_rates<csep.core.forecasts.GriddedForecast.target_event_rates>`
that returns a tuple (:class:`numpy.ndarray`, float) consisting of the target event rates and the expected number of events
from the forecast.

.. note::
    The target event rate is the expected rate for an observed event in the observed catalog assuming that
    the forecast is true. For a simple example, if we forecast a rate of 0.3 events per year in some bin of a forecast,
    each event that occurs within that bin has a target event rate of 0.3 events per year. The expected number of events
    in the forecast can be determined by summing over all bins in the gridded forecast.

We can also see that the ``paired_t_test`` function uses the ``gridded_forecast1.name`` and calls the :func:`numpy.min`
on the ``gridded_forecast1.magnitudes``. Using this information, we can create a mock-class that implements these methods
that can be used by this function.

.. warning::
    If you are creating mock-classes to use with evaluation functions, make sure that you visit the corresponding
    documentation and source-code to make sure that your methods return values that are expected by the function. In
    this case, it expects the tuple (target_event_rates, expected_forecast_count). This will not always be the case.
    If you need help, please create an issue on the GitHub page.

Here we show an implementation of a mock forecast class that can work with the
:func:`paired_t_test<csep.core.poisson_evaluations.paired_t_test>` function. ::

    class MockForecast:

        def __init__(self, data=None, name='my-mock-forecast', magnitudes=(4.95)):

            # data is not necessary, but might be helpful for implementing target_event_rates(...)
            self.data = data
            self.name = name
            # this should be an array or list. it can be as simple as the default argument.
            self.magnitudes = magnitudes

        def target_event_rates(catalog, scale=None):
            """ Notice we added the dummy argument scale. This function stub should match what is called paired_t_test """

            # whatever custom logic you need to return these target event rates given your catalog can go here
            # of course, this should work with whatever catalog you decide to pass into this function

            # this returns the tuple that paired_t_test expects
            return (ndarray_of_target_event_rates, expected_number_of_events)

You'll notice that :func:`paired_t_test<csep.core.poisson_evaluations.paired_t_test>` expects a catalog class. Looking back
at the function definition we can see that it needs ``observed_catalog.event_count`` and ``observed_catalog.name``. Therefore
the mock class for the catalog would look something like this ::

    class MockCatalog:

        def __init__(self, event_count, data=None, name='my-mock-catalog'):

            # this is not necessary, but adding data might be helpful for implementing the
            # logic needed for the target_event_rates(...) function in the MockForecast class.
            self.data = data
            self.name = name
            self.event_count = event_count


Now using these two objects you can call the :func:`paired_t_test<csep.core.poisson_evaluations.paired_t_test>` directly
without having to modify any of the source code. ::

    # create your forecasts
    mock_forecast_1 = MockForecast(some_forecast_data1)
    mock_forecast_2 = MockForecast(some_forecast_data2)

    # lets assume that catalog_data is an array that contains the catalog data
    catalog = MockCatalog(len(catalog_data))

    # call the function using your classes
    eval_result = paired_t_test(mock_forecast_1, mock_forecast_2, catalog)

The only requirement for this approach is that you implement the methods on the class that the calling function expects.
You can add anything else that you need in order to make those functions work properly. This example is about
as simple as it gets.

.. note::

    If you want to use mock-forecasts and mock-catalogs for other evaluations. You can just add the additional methods
    that are needed onto the mock classes you have already built.
