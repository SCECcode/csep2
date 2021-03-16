=====================
Terms and Definitions
=====================

The page contains terms and their definitions (and possible mathematical definitions) that are commonly used throughout the documentation
and CSEP literature.

.. contents:: Table of Contents
    :local:
    :depth: 2


.. _earthquake-catalog:

Earthquake catalog
------------------
List of earthquakes (either tectonic or non-tectonic) defined through their location in space, origin time of the event, and
their magnitude.


.. _earthquake_forecast:

Earthquake Forecast
-------------------
A probabilistic statement about the occurrence of seismicity that can include information about the magnitude and spatial
location. CSEP supports earthquake forecasts expressed as the expected rate of seismicity in disjoint space and magnitude bins
and as families of synthetic earthquake catalogs.

.. _stochastic-event-set:

Stochastic Event Set
--------------------
Collection of synthetic earthquakes (events) that are produced by an earthquake.
A *stochastic event set* consists of *N* events that represent a continuous representation of seismicity that can sample
the uncertainty present within in the forecasting model.

.. _time-dependent-forecast:

Time-dependent Forecast
-----------------------
The forecast changes over time using new information not available at the time the forecast was issued. For example,
epidemic-type aftershock sequence models (ETAS) models can utilize updated using newly observed seismicity to produce
new forecasts consistent with the model.

.. _time-independent-forecast:

Time-independent Forecast
-------------------------
The forecast does not change with time. Time-independent forecasts are generally used for long-term forecasts
needed for probabalistic seismic hazard analysis.
