Installation notes
==================

Install the freeimage library
-----------------------------

The :mod:`jicimagelib` package depends on
`freeimage <http://freeimage.sourceforge.net/>`_ to open image file.

On Linux bases system freeimage can usually be installed using the package
manager.  For example on Fedora it can be installed using the command below.

::

    sudo yum install freeimage

On Macs it can be installed using `homebrew <http://brew.sh/>`_ using the
command below.

::

    brew install freeimage


Install the Python package dependencies
---------------------------------------

The :mod:`jicimagelib` package depends on a number of other scientific Python
packages. These can be installed using
`pip <https://pypi.python.org/pypi/pip>`_.

::

    pip install numpy
    pip install scipy
    pip install scikit-image

Although the :mod:`jicimage` package does not depend on it you may also want to
install the IPython notebook as :mod:`jicimagelib` has been designed to work
well with it, for example by providing the ability to view
:class:`jicimagelib.image.Image` and :class:`jicimagelib.image.ProxyImage`
objects as images in the IPython notebook.

::

    pip install "ipython[notebook]"



Install the BioFormats command line tools
-----------------------------------------

The :mod:`jicimagelib` package does not explicitly depend on the BioFormats
command line tools. However, they are needed if you want to be able to work
with microscopy files.

Download the `bftools.zip
<http://downloads.openmicroscopy.org/latest/bio-formats5.0/artifacts/bftools.zip>`_
file from the `openmicroscopy website
<http://www.openmicroscopy.org/site/support/bio-formats5.0/users/comlinetools/>`_.

Unzip the ``bftools.zip`` file into a memorable location for example a
directory named ``tools``.

::

    mkdir ~/tools
    mv ~/Downloads/bftools.zip ~/tools/
    cd ~/tools
    unzip bftools.zip

Finally add the ``bftools`` directory to your ``PATH``.

::

    export PATH=$PATH:~/tools/bftools

.. note:: You may want to add the line above to your ``.bashrc`` file.

Install the :mod:`jicimagelib` package
--------------------------------------

Finally install the :mod:`jicimagelib` package using ``pip``.

::

    pip install jicimagelib

Alternatively clone the package from `GitHub <https://github.com/>`_
and install it from source.

::

    git clone https://github.com/JIC-CSB/jicimagelib.git
    cd jicimagelib
    python setup.py install
