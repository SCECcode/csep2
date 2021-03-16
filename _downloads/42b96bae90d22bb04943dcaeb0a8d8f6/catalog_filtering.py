"""
.. tutorial-catalog-filtering

Catalogs operations
===================

This example demonstrates how to perform standard operations on a catalog. This example requires an internet
connection to access ComCat.

Overview:
    1. Load catalog from ComCat
    2. Create filtering parameters in space, magnitude, and time
    3. Filter catalog using desired filters
    4. Write catalog to standard CSEP format
"""

####################################################################################################################################
# Load required libraries
# -----------------------
#
# Most of the core functionality can be imported from the top-level :mod:`csep` package. Utilities are available from the
# :mod:`csep.utils` subpackage.

import csep
from csep.core import regions
from csep.utils import time_utils, comcat

####################################################################################################################################
# Load catalog
# ------------
#
# PyCSEP provides access to the ComCat web API using :func:`csep.query_comcat`. This function requires a
# :class:`datetime.datetime` to specify the start and end dates.

start_time = csep.utils.time_utils.strptime_to_utc_datetime('2019-01-01 00:00:00.0')
end_time = csep.utils.time_utils.utc_now_datetime()
catalog = csep.query_comcat(start_time, end_time)
print(catalog)

####################################################################################################################################
# Filter to magnitude range
# -------------------------
#
# Use the :meth:`csep.core.catalogs.AbstractBaseCatalog.filter` to filter the catalog. The filter function uses the field
# names stored in the numpy structured array. Standard fieldnames include 'magnitude', 'origin_time', 'latitude', 'longitude',
# and 'depth'.

catalog = catalog.filter('magnitude >= 3.5')
print(catalog)

####################################################################################################################################
# Filter to desired time interval
# -------------------------------
#
# We need to define desired start and end times for the catalog using a time-string format. PyCSEP uses integer times for doing
# time manipulations. Time strings can be converted into integer times using
# :func:`csep.utils.time_utils.strptime_to_utc_epoch`. The :meth:`csep.core.catalog.AbstractBaseCatalog.filter` also
# accepts a list of strings to apply multiple filters.

# create epoch times from time-string formats
start_epoch = csep.utils.time_utils.strptime_to_utc_epoch('2019-07-06 03:19:54.040000')
end_epoch = csep.utils.time_utils.strptime_to_utc_epoch('2019-09-21 03:19:54.040000')

# filter catalog to magnitude ranges and times
filters = [f'origin_time >= {start_epoch}', f'origin_time < {end_epoch}']
catalog = catalog.filter(filters)
print(catalog)

####################################################################################################################################
# Filter to desired spatial region
# --------------------------------
#
# We use a circular spatial region with a radius of 3 average fault lengths as defined by the Wells and Coppersmith scaling
# relationship. PyCSEP provides :func:`csep.utils.spatial.generate_aftershock_region` to create an aftershock region
# based on the magnitude and epicenter of an event.
#
# We use :func:`csep.utils.comcat.get_event_by_id` the ComCat API provided by the USGS to obtain the event information
# from the M7.1 Ridgecrest mainshock.

m71_event_id = 'ci38457511'
event = comcat.get_event_by_id(m71_event_id)
m71_epoch = time_utils.datetime_to_utc_epoch(event.time)

# build aftershock region
aftershock_region = regions.generate_aftershock_region(event.magnitude, event.longitude, event.latitude)

# apply new aftershock region and magnitude of completeness
catalog = catalog.filter_spatial(aftershock_region).apply_mct(event.magnitude, m71_epoch)
print(catalog)


####################################################################################################################################
# Write catalog
# -------------
#
# Use :meth:`csep.core.catalogs.AbstractBaseCatalog.write_ascii` to write the catalog into the comma separated value format.
catalog.write_ascii('2019-11-11-comcat.csv')
