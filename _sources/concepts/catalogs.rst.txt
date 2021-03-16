.. _catalogs-reference:

########
Catalogs
########

PyCSEP provides routines for working with and manipulating earthquake catalogs for the purposes of evaluating earthquake
forecasting models.

If you are able to make use of these tools for other reasons, please let us know. We are especially interested in
including basic catalog statistics into this package. If you are interested in helping implement routines like
b-value estimation and catalog completeness that would be much appreciated.

.. contents:: Table of Contents
    :local:
    :depth: 2

************
Introduction
************

PyCSEP catalog basics
=====================

An earthquake catalog contains a collection of seismic events each defined by a set of attributes. PyCSEP implements
a simple event description that is suitable for evaluating earthquake forecasts. In this format, every seismic event is
defined by its location in space (longitude, latitude, and depth), magnitude, and origin time. In addition, each event
can have an optional ``event_id`` as a unique identifier.

PyCSEP provides :class:`csep.core.catalogs.CSEPCatalog` to represent an earthquake catalog. The essential event data are stored in a
`structured NumPy array <https://numpy.org/doc/stable/user/basics.rec.html>`_ with the following data type. ::

    dtype = numpy.dtype([('id', 'S256'),
                         ('origin_time', '<i8'),
                         ('latitude', '<f4'),
                         ('longitude', '<f4'),
                         ('depth', '<f4'),
                         ('magnitude', '<f4')])

Additional information can be associated with an event using the ``id`` field in the structured array in a class member called
``metadata``. The essential event data must be complete meaning that each event should have these attributes defined. The metadata
is more freeform and PyCSEP does not impose any restrictions on the way that event metadata is stored. Only that the metadata
for an event should be accessible using the event ``id``. An example of this could be ::

    catalog = csep.load_catalog('catalog_file.csv')
    event_metadata = catalog.metadata[event_id]

This would load a catalog stored in the PyCSEP .csv format. PyCSEP contains catalog readers for the following formats
(We are also looking to support other catalog formats. Please suggest some or better yet help us write the readers!):

1. CSEP ascii format
2. NDK format (used by the gCMT catalog)
3. INGV gCMT catalog
4. ZMAP format
5. pre-processed JMA format

PyCSEP supports the ability to easily define a custom reader function for a catalog format type that we don't currently support.
If you happen to implement a reader for a new catalog format please check out the
`contribution guidelines <https://github.com/SCECCode/csep2/blob/dev/CONTRIBUTING.md>`_ and make a pull request so
we can include this in the next release.

Catalog as Pandas dataframes
============================

You might be comfortable using Pandas dataframes to manipulate tabular data. PyCSEP provides some routines for accessing
catalogs as a :class:`pandas.DataFrame`. You can use ``df = catalog.to_dataframe(with_datetimes=True)`` to return the
DataFrame representation of the catalog. Using the ``catalog = CSEPCatalog.from_dataframe(df)`` you can return back to the
PyCSEP data model.

.. note::

    Going between a DataFrame and CSEPCatalog is a lossy transformation. It essentially only retains the essential event
    attributes that are defined by the ``dtype`` of the class.



****************
Loading catalogs
****************

Load catalogs from files
========================

You can easily load catalogs in the supported format above using :func:`csep.load_catalog`. This function provides a
top-level function to load catalogs that are currently supported by PyCSEP. You must specify the type of the catalog and
the format you want it to be loaded. The type of the catalog can be: ::

    catalog_type = ('ucerf3', 'csep-csv', 'zmap', 'jma-csv', 'ndk')
    catalog_format = ('csep', 'native')

The catalog type determines which reader :mod:`csep.utils.readers` will be used to load in the file. The default is the
``csep-csv`` type and the ``native`` format. The ``jma-csv`` format can be created using the ``./bin/deck2csv.pl``
Perl script.

.. note::
    The format is important for ``ucerf3`` catalogs, because those are stored as big endian binary numbers by default.
    If you are working with ``ucerf3-etas`` catalogs and would like to convert them into the CSEPCatalog format you can
    use the ``format='csep'`` option when loading in a catalog or catalogs.

Load catalogs from ComCat
=========================

PyCSEP provides top-level functions to load catalogs using ComCat. We incorporated the work done by Mike Hearne and
others from the U.S. Geological Survey into PyCSEP in an effort to reduce the dependencies of this project. The top-level
access to ComCat catalogs can be accessed from :func:`csep.query_comcat`. Some lower level functionality can be accessed
through the :mod:`csep.utils.comcat` module. All credit for this code goes to the U.S. Geological Survey.

:ref:`Here<tutorial-catalog-filtering>` is complete example of accessing the ComCat catalog.

Writing custom loader functions
===============================

You can easily add custom loader functions to import data formats that are not currently included with the PyCSEP tools.
Both :meth:`csep.core.catalogs.CSEPCatalog.load_catalog` and :func:`csep.load_catalog` support an optional argument
called ``loader`` to support these custom data formats.

In the simplest form the function should have the following stub: ::

    def my_custom_loader_function(filename):
        """ Custom loader function for catalog data.

        Args:
            filename (str): path to the file containing the path to the forecast

        Returns:
            eventlist: iterable of event data with the order:
                    (event_id, origin_time, latitude, longitude, depth, magnitude)
        """

        # imagine there is some logic to read in data from filename

        return eventlist

This function can then be passed to :func:`csep.load_catalog` or :meth:`CSEPCatalog.load_catalog<csep.core.catalogs.CSEPCatalog.load_catalog>`
with the ``loader`` keyword argument. The function should be passed as a first-class object like this: ::

    import csep
    my_custom_catalog = csep.load_catalog(filename, loader=my_custom_loader_function)

.. note::
    The origin_time is actually an integer time. We recommend to parse the timing information as a
    :class:`datetime.datetime` object and use the :func:`datetime_to_utc_epoch<csep.utils.time_utils.datetime_to_utc_epoch>`
    function to convert this to an integer time.

Notice, we did not actually call the function but we just passed it as a reference. These functions can also access
web-based catalogs like we implement with the :func:`csep.query_comcat` function. This function doesn't work with either
:func:`csep.load_catalog` or :meth:`CSEPCatalog.load_catalog<csep.core.catalogs.CSEPCatalog.load_catalog>`,
because these are intended for file-based catalogs. Instead, we can create the catalog object directly.
We would do that like this ::

    def my_custom_web_loader(...):
        """ Accesses catalog from online data source.

        There are no requirements on the arguments if you are creating the catalog directly from the class.

        Returns:
            eventlist: iterable of event data with the order:
                (event_id, origin_time, latitude, longitude, depth, magnitude)
        """

        # custom logic to access online catalog repository

        return eventlist

As you might notice, all loader functions are required to return an event-list. This event-list must be iterable and
contain the required event data.

.. note::
    The events in the eventlist should follow the form ::

        eventlist = my_custom_loader_function(...)

        event = eventlist[0]

        event[0] = event_id
        # see note above about using integer times
        event[1] = origin_time
        event[2] = latitude
        event[3] = longitude
        event[4] = depth
        event[5] = magnitude


Once you have a function that returns an eventlist, you can create the catalog object directly. This uses the
:class:`csep.core.catalogs.CSEPCatalog` as an example. ::

    import csep

    eventlist = my_custom_web_loader(...)
    catalog = csep.catalogs.CSEPCatalog(data=eventlist, **kwargs)

The **kwargs represents any other keyword argument that can be passed to
:class:`CSEPCatalog<csep.core.catalogs.CSEPCatalog>`. This could be the ``catalog_id`` or the
:class:`CartesianGrid2D<csep.core.regions.CartesianGrid2D>`.

Including custom event metadata
===============================

Catalogs can include additional metadata associated with each event. Right now, there are no direct applications for
event metadata. Nonetheless, it can be included with a catalog object.

The event metadata should be a dictionary where the keys are the ``event_id`` of the individual events. For example, ::

    event_id = 'my_dummy_id'
    metadata_dict = catalog.metadata[event_id]

Each event meta_data should be a JSON-serializable dictionary or a class that implements the to_dict() and from_dict() methods. This is
required to properly save the catalog files into JSON format and verify whether two catalogs are the same. You can see
the :meth:`to_dict<csep.core.catalogs.CSEPCatalog>` and :meth:`from_dict<csep.core.catalogs.CSEPCatalog>` methods for an
example of how these would work.

***************************
Accessing Event Information
***************************

In order to utilize the low-level acceleration from Numpy, most catalog operations are vectorized. The catalog classes
provide some getter methods to access the essential catalog data. These return arrays of :class:`numpy.ndarray` with the
``dtype`` defined by the class.

.. automodule:: csep.core.catalogs

The following functions return :class:`numpy.ndarrays<numpy.ndarray>` of the catalog information.

.. autosummary::

   CSEPCatalog.event_count
   CSEPCatalog.get_magnitudes
   CSEPCatalog.get_longitudes
   CSEPCatalog.get_latitudes
   CSEPCatalog.get_depths
   CSEPCatalog.get_epoch_times
   CSEPCatalog.get_datetimes
   CSEPCatalog.get_cumulative_number_of_events

The catalog data can be iterated through event-by-event using a standard for-loop. For example, we can do something
like ::

    for event in catalog.data:
        print(
            event['id'],
            event['origin_time'],
            event['latitude'],
            event['longitude'],
            event['depth'],
            event['magnitude']
        )

The keyword for the event tuple are defined by the ``dtype`` of the class. The keywords for
:class:`CSEPCatalog<csep.core.catalogs.CSEPCatalog>` are shown in the snippet directly above. For example, a quick and
dirty plot of the cumulative events over time can be made using the :mod:`matplotlib.pyplot` interface ::

    import csep
    import matplotlib.pyplot as plt

    # lets assume we already loaded in some catalog
    catalog = csep.load_catalog("my_catalog_path.csv")

    # quick and dirty plot
    fig, ax = plt.subplots()
    ax.plot(catalog.get_epoch_times(), catalog.get_cumulative_number_of_events())
    plt.show()

****************
Filtering events
****************

Most of the catalog files (or catalogs accessed via the web) contain more events that are desired for a given use case.
PyCSEP provides a few routines to help filter events out of the catalog. The following methods help to filter out
unwanted events from the catalog.

.. autosummary::

    CSEPCatalog.filter
    CSEPCatalog.filter_spatial
    CSEPCatalog.apply_mct

Filtering events by attribute
=============================

The function :meth:`CSEPCatalog.filter<csep.core.catalogs.CSEPCatalog.filter>` provides the ability to filter events
based on their essential attributes. This function works by parsing filtering strings and applying them using a logical
`and` operation. The catalog strings have the following format ``filter_string = f"{attribute} {operator} {value}"``. The
filter strings represent a statement that would evaluate as `True` after they are applied. For example, the statement
``catalog.filter('magnitude >= 2.5')`` would retain all events in the catalog greater-than-or-equal to magnitude 2.5.

The attributes are determined by the dtype of the catalog, therefore you can filter based on the ``(origin_time, latitude,
longitude, depth, and magnitude).`` Additionally, you can use the attribute ``datetime`` and provide a :class:`datetime.datetime`
object to filter events using the data type.

The filter function can accept a string or a list of filter statements. If the function is called without any arguments
the function looks to use the ``catalog.filters`` member. This can be provided during class instantiation or bound
to the class afterward. :ref:`Here<tutorial-catalog-filtering>` is complete example of how to filter a catalog
using the filtering strings.

Filtering events in space
=========================

You might want to supply a non-rectangular polygon that can be used to filter events in space. This is commonly done
to prepare an observed catalog for forecast evaluation. Right now, this can be accomplished by supplying a
:class:`region<csep.core.regions.CartesianGrid2D>` to the catalog or
:meth:`filter_spatial<csep.core.catalogs.CSEPCatalog.filter_spatial>`. There will be more information about using regions
in the :ref:`user-guide page<regions-reference>` page. The :ref:`catalog filtering<tutorial-catalog-filtering>` contains
a complete example of how to filter a catalog using a user defined aftershock region based on the M7.1 Ridgecrest
mainshock.

Time-dependent magnitude of completeness
========================================

Seismic networks have difficulty recording events immediately after a large event occurs, because the passing seismic waves
from the larger event become mixed with any potential smaller events. Usually when we evaluate an aftershock forecast, we should
account for this time-dependent magnitude of completeness. PyCSEP provides the
:ref:`Helmstetter et al., [2006]<helmstetter-2006>` implementation of the time-dependent magnitude completeness model.

This requires information about an event which can be supplied directly to :meth:`apply_mct<csep.core.catalogs.CSEPCatalog>`.
Additionally, PyCSEP provides access to the ComCat API using :func:`get_event_by_id<csep.utils.comcat.get_event_by_id>`.
An exmaple of this can be seen in the :ref:`filtering catalog tutorial<tutorial-catalog-filtering>`.


**************
Binning Events
**************

Another common task requires binning earthquakes by their spatial locations and magnitudes. This is routinely done when
evaluating earthquake forecasts. Like filtering a catalog in space, you need to provide some information about the region
that will be used for the binning. Please see the :ref:`user-guide page<regions-reference>` for more information about
regions.

.. note::
    We would like to make this functionality more user friendly. If you have suggestions or struggles, please open an issue
    on the GitHub page and we'd be happy to incorporate these ideas into the toolkit.

The following functions allow binning of catalogs using space-magnitude regions.

.. autosummary::

   CSEPCatalog.spatial_counts
   CSEPCatalog.magnitude_counts
   CSEPCatalog.spatial_magnitude_counts

These functions return :class:`numpy.ndarrays<numpy.ndarray>` containing the count of the events determined from the
catalogs. This example shows how to obtain magnitude counts from a catalog.
The index of the ndarray corresponds to the index of the associated space-magnitude region. For example, ::

    import csep
    import numpy

    catalog = csep.load_catalog("my_catalog_file")

    # returns bin edges [2.5, 2.6, ... , 7.5]
    bin_edges = numpy.arange(2.5, 7.55, 0.1)

    magnitude_counts = catalog.magnitude_counts(mag_bins=bin_edges)

In this example, ``magnitude_counts[0]`` is the number of events with 2.5 ≤ M < 2.6. All of the magnitude binning assumes
that the final bin extends to infinity, therefore ``magnitude_counts[-1]`` contains the number of events with
7.5 ≤ M < ∞.