Installing PyCSEP
=================

We are working on a ``conda-forge`` recipe and PyPI distribution.
If you plan on contributing to this package, visit the
`contribution guidelines <https://github.com/SCECcode/pycsep/blob/master/CONTRIBUTING.md>`_ for installation instructions.

.. note:: This package requires >=Python 3.7.

The easiest way to install PyCSEP is using ``conda``. It can also be installed using ``pip`` or built from source.

Using Conda
-----------
For most users, you can use ::

    conda install --channel conda-forge pycsep

Using Pip
---------

Before this installation will work, you must **first** install the following system dependencies. The remaining dependencies
should be installed by the installation script. To help manage dependency issues, we recommend using virtual environments
like `virtualenv`.

| Python 3.7 or later (https://python.org)
|
| NumPy 1.10 or later (https://numpy.org)
|     Python package for scientific computing and numerical calculations.
|
| GEOS 3.3.3 or later (https://trac.osgeo.org/geos/)
|     C++ library for processing geometry.
|
| PROJ 4.9.0 or later (https://proj4.org/)
|     Library for cartographic projections.

Example for Ubuntu: ::

    sudo apt-get install libproj-dev proj-data proj-bin
    sudo apt-get install libgeos-dev
    pip install --upgrade pip
    pip install numpy

Example for MacOS: ::

    brew install proj geos
    pip install --upgrade pip
    pip install numpy

Installing from Source
----------------------

Use this approach if you want the most up-to-date code. This creates an editable installation that can be synced with
the latest GitHub commit.

We recommend using virtual environments when installing python packages from source to avoid any dependency conflicts. We prefer
``conda`` as the package manager over ``pip``, because ``conda`` does a good job of handling binary distributions of packages
across multiple platforms. Also, we recommend using the ``miniconda`` installer, because it is lightweight and only includes
necessary pacakages like ``pip`` and ``zlib``.

Using Conda
***********

If you don't have ``conda`` on your machine, download and install `Miniconda <https://docs.conda.io/en/latest/miniconda.html>`_. ::

    git clone https://github.com/SCECcode/pycsep
    cd pycsep
    conda env create -f requirements.yml
    conda activate csep-dev
    # Installs in editor mode with all dependencies
    pip install -e .

Note: If you want to go back to your default environment use the command ``conda deactivate``.

Using Pip / Virtualenv
**********************

We highly recommend using Conda, because this tools helps to manage binary dependencies on Python packages. If you
must use `Virtualenv <https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/>`_
follow these instructions: ::

    git clone https://github.com/SCECcode/pycsep
    cd pycsep
    python -m virtualenv venv
    source venv/bin/activate
    # Installs in editor mode dependencies are installed by conda
    pip install -e .[all]

Note: If you want to go back to your default environment use the command ``deactivate``.

Developers Installation
-----------------------

This shows you how to install a copy of the repository that you can use to create Pull Requests and sync with the upstream
repository. First, fork the repo on GitHub. It will now live at ``https://github.com/<YOUR_GITHUB_USERNAME>/pycsep``.
We recommend using ``conda`` to install the development environment. ::

    git clone https://github.com/<YOUR_GITHUB_USERNAME>/pycsep.git
    cd pycsep
    conda env create -f requirements.yml
    conda activate csep-dev
    pip install -e .
    # Allow sync with default repository
    git remote add upstream https://github.com/SCECCode/pycsep.git

Now you can pull from upstream using ``git pull upstream master`` to keep your copy of the repository in sync with the
latest commits.