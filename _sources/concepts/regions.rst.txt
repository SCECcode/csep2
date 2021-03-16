.. _regions-reference

#######
Regions
#######

.. automodule:: csep.utils.basic_types

PyCSEP includes commonly used CSEP testing regions and classes that facilitate working with gridded data sets. This
module is early in development and will be a focus of future development.

.. contents:: Table of Contents
    :local:
    :depth: 2

.. :currentmodule:: csep

.. automodule:: csep.core.regions

Practically speaking, earthquake forecasts, especially time-dependent forecasts, treat time differently than space and
magnitude. If we consider a family of monthly forecasts for the state of California for earthquakes with **M** 3.95+,
each of these forecasts would use the same space-magnitude region, even though the time periods are
different. Because the time horizon is an implicit property of the forecast, we do not explicitly consider time in the region
objects provided by PyCSEP. This module contains tools for working with gridded regions in both space and magnitude.

First, we will describe how the spatial regions are handled. Followed by magnitude regions, and how these two aspects
interact with one another.

**************
Region objects
**************

Currently, PyCSEP provides the :class:`CartesianGrid2D<csep.core.regions.CartesianGrid2D>` to handle binning catalogs
and defining regions for earthquake forecasting evaluations. We plan to expand this module in the future to include
more complex spatial regions.

2D Cartesian grids
##################

This section contains information about using 2D cartesian grids.

.. autosummary::

    CartesianGrid2D

.. note::
    We are planning to do some improvements to this module and to expand its capabilities. For example, we would like to
    handle non-regular grids such as a quad-tree. Also, a single Polygon should be able to act as the spatial component
    of the region. These additions will make this toolkit more useful for crafting bespoke experiments and for general
    catalog analysis. Feature requests are always welcome!

The :class:`CartesianGrid2D<csep.core.regions.CartesianGrid2D>` acts as a data structure that can associate a spatial
location (eg., lon and lat) with its corresponding spatial bin. This class is optimized to work with regular grids,
although they do not have to be complete (they can have holes) and they do not have to be rectangular (each row / column
can have a different starting coordinate).

The :class:`CartesianGrid2D<csep.core.regions.CartesianGrid2D>` maintains a list of
:class:`Polygon<csep.core.regions.Polygon>` objects that represent the individual spatial bins from the overall
region. The origin of each polygon is considered to be the lower-left corner (the minimum latitude and minimum longitude).

.. autosummary::

    CartesianGrid2D.num_nodes
    CartesianGrid2D.get_index_of
    CartesianGrid2D.get_location_of
    CartesianGrid2D.get_masked
    CartesianGrid2D.get_cartesian
    CartesianGrid2D.get_bbox
    CartesianGrid2D.midpoints
    CartesianGrid2D.origins
    CartesianGrid2D.from_origins


Creating spatial regions
########################

Here, we describe how the class works starting with the class constructors. ::

    @classmethod
    def from_origins(cls, origins, dh=None, magnitudes=None, name=None):
        """ Convenience function to create CartesianGrid2D from list of polygon origins """

For most applications, using the :meth:`from_origins<csep.core.regions.CartesianGrid2D.from_origins>` function will be
the easiest way to create a new spatial region. The method accepts a 2D :class:`numpy.ndarray` containing the x (lon) and y (lat)
origins of the spatial bin polygons. These should be the complete set of origins. The function will attempt to compute the
grid spacing by comparing the x and y values between adjacent origins. If this does not seem like a reliable approach
for your region, you can explicitly provide the grid spacing (dh) to this method.

When a :class:`CartesianGrid2D<csep.core.regions.CartesianGrid2D>` is created the following steps occur:

    1. Compute the bounding box containing all polygons (2D array)
    2. Create a map between the index of the 2D bounding box and the list of polygons of the region.
    3. Store a boolean flag indicating whether a given cell in the 2D array is valid or not

Once these mapping have been created, we can now associate an arbitrary (lon, lat) point with a spatial cell using the
mapping defined in (2). The :meth:`get_index_of<csep.core.regions.CartesianGrid2D.get_index_of>` accepts a list
of longitudes and latitudes and returns the index of the polygon they are associated with. For instance, this index can
now be used to access a data value stored in another data structure.

***************
Testing Regions
***************

CSEP has defined testing regions that can be used for earthquake forecasting experiments. The following functions in the
:mod:`csep.core.regions` module returns a :class:`CartesianGrid2D<csep.core.regions.CartesianGrid2D>` consistent with
these regions.

.. autosummary::

    california_relm_region
    italy_csep_region
    global_region

****************
Region Utilities
****************

PyCSEP also provides some utilities that can facilitate working with regions. As we expand this module, we will include
functions to accommodate different use-cases.

.. autosummary::

    magnitude_bins
    create_space_magnitude_region
    parse_csep_template
    increase_grid_resolution
    masked_region
    generate_aftershock_region