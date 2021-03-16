===========================
Core Concepts for Beginners
===========================

If you are reading this documentation, there is a good chance that you are developing/evaluating an earthquake forecast or
implementing an experiment at a CSEP testing center. This section will help you understand how we conceptualize forecasts,
evaluations, and earthquake catalogs. These components make up the majority of the PyCSEP package. We also include some
prewritten visualizations along with some utilities that might be useful in your work.

Catalogs
========
Earthquake catalogs are fundamental to both forecasts and evaluations and make up a core component of the PyCSEP package.
At some point you will be working with catalogs if you are evaluating earthquake forecasts.

One major difference between PyCSEP and a project like `ObsPy <https://docs.obspy.org/>`_ is that typical 'CSEP' calculations
operate on an entire catalog at once to perform methods like filtering and binning that are required to evaluate an earthquake
forecast. We provide earthquake catalog classes that follow the interface defined by
:class:`AbstractBaseCatalog <csep.core.catalogs.AbstractBaseCatalog>`.

The catalog data are stored internally as a `structured Numpy array <https://numpy.org/doc/stable/user/basics.rec.html>`_
which effectively treats events contiguously in memory like a c-style struct. This allows us to accelerate calculations
using the vectorized operations provided by Numpy. The necessary attributes for an event to be used
in an evaluation are the spatial location (lat, lon), magnitude, and origin time. Additionally, depth and other identifying
characteristics can be used. The `default storage format <https://scec.usc.edu/scecpedia/CSEP_2_CATALOG_FORMAT>`_ for
an earthquake catalog is an ASCII/utf-8 text file with events stored in CSV format.

The :class:`AbstractBaseCatalog <csep.core.catalogs.AbstractBaseCatalog>` can be extended to accommodate different catalog formats
or input and output routines. For example :class:`UCERF3Catalog <csep.core.catalogs.UCERF3Catalog>` extends this class to deal
with the big-endian storage routine from the `UCERF3-ETAS <https://github.com/opensha/opensha-ucerf3>`_ forecasting model. More
information will be included in the :ref:`catalogs-reference` section of the documentation.

Forecasts
=========

PyCSEP provides objects for interacting with :ref:`earthquake forecasts <earthquake_forecast>`. PyCSEP supports two types
of earthquake forecasts, and provides separate objects for interacting with both. The forecasts share similar
characteristics, but, conceptually, they should be treated differently because they require different types of evaluations.

Both time-independent and time-dependent forecasts are represented using the same PyCSEP forecast objects. Typically, for
time-dependent forecasts, one would create separate forecast objects for each time period. As the name suggests,
time-independent forecasts do not change with time.


Grid-based forecast
-------------------

Grid-based earthquake forecasts are specified by the expected rate of earthquakes within discrete, independent
space-time-magnitude bins. Within each bin, the expected rate represents the parameter of a Poisson distribution. For, details
about the forecast objects visit the :ref:`forecast-reference` section of the documentation.

The forecast object contains three main components: (1) the expected earthquake rates, (2) the
:class:`spatial region <csep.utils.spatial.CartesianGrid2D>` associated with the rates, and (3) the magnitude range
associated with the expected rates. The spatial bins are usually discretized according to the geographical coordinates
latitude and longitude with most previous CSEP spatial regions defining a spatial size of 0.1° x 0.1°. Magnitude bins are
also discretized similarly, with 0.1 magnitude units being a standard choice. PyCSEP does not enforce constraints on the
bin-sizes for both space and magnitude, but the discretion must be regular.


Catalog-based forecast
----------------------

Catalog-based forecasts are specified by families of synthetic earthquake catalogs that are generated through simulation
by probabilistic models. Each catalog represents a stochastic representation of seismicity consistent with the forecasting
model. Probabilistic statements are made by computing statistics (usually by counting) within the family of synthetic catalogs,
which can be as simple as counted the number of events in each catalog. These statistics represent the full-distribution of outcomes as
specified by the forecasting models, thereby allowing for more direct assessments of the models that produce them.

Within PyCSEP catalog forecasts are effectively lists of earthquake catalogs, no different than those obtained from
authoritative sources. Thus, any operation that can be performed on an observed earthquake catalog can be performed on a
synthetic catalog from a catalog-based forecast.

It can be useful to count the numbers of forecasted earthquakes within discrete space-time bins (like those used for
grid-based forecasts). Therefore, it's common to have a :class:`spatial region <csep.utils.spatial.CartesianGrid2D>` and
set of magnitude bins associated with a forecast. Again, the only rules that PyCSEP enforces are that the space-magnitude
regions are regularly discretized.

Evaluations
===========

PyCSEP provides implementations of statistical tests used to evaluate both grid-based and catalog-based earthquake forecasts.
The former use parametric evaluations based on Poisson likelihood functions, while the latter use so-called 'likelihood-free'
evaluations that are computed from empirical distributions provided by the forecasts. Details on the specific implementation
of the evaluations will be provided in the :ref:`evaluation-reference` section.

Every evaluation can be different, but in general, the evaluations need the following information:

1. Earthquake forecast(s)

    * Spatial region
    * Magnitude range

2. Authoritative earthquake catalog

PyCSEP does not produce earthquake forecasts, but provides the ability to represent them using internal data models to
facilitate their evaluation. General advice on how to administer the statistical tests will be provided in the
:ref:`evaluation-reference` section.