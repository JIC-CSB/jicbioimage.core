Installation notes
==================

Create a virtual Python environment
-----------------------------------

Although you can install the :mod:`jicimagelib` package into your system Python
we recommend that you install it into a Python virtual environment.  To do this
you need to install ``virtualenv``.

You can install ``virtualenv`` using ``easy_install``.

::

    easy_install virtualenv

Or using ``pip``.

::

    pip install virtualenv

If your computer does not have ``easy_install`` or ``pip`` installed you can
try installing them using your package manager.

.. note:: More information on how to install ``virtualenv`` can be found in the
          `virtualenv documentation
          <https://virtualenv.pypa.io/en/latest/installation.html#installation>`_

When you have ``virtualenv`` installed you can create a virtual environment.

::

    virtualenv env

The command above will create a directory called ``env`` in which your virtual
environment is stored. To activate it source the ``env/bin/activate`` file.

::

    . ./env/bin/activate

.. note:: Note that the command above starts with a single ``.`` followed by a
          space.

Install the :mod:`jicimagelib` dependencies
-------------------------------------------

When you create a virtual environment it comes bundled with ``pip``, which we
will use to install the packages that :mod:`jicimagelib` depend on.

::

    pip install numpy
    pip install scipy
    pip install scikit-image

Although the :mod:`jicimage` package does not depend on it you may also want to
install the IPython notebook as :mod:`jicimagelib` has been designed to work
well with it, for example by providing the ability to view
:class:`jicimagelib.image.Image` and :class:`jicimagelib.image.ImageProxy`
objects as images in the IPython notebook.

::

    pip install "ipython[notebook]"

Install the BioFormats command line tools
-----------------------------------------

The :mod:`jicimagelib` package does not explicitly depend on the BioFormats
command line tools. However, it is needed if you want to be able to work with
microscopy file.

Download the `bftools.zip
<http://downloads.openmicroscopy.org/latest/bio-formats5.0/artifacts/bftools.zip>`_
file from the `openmicroscopy website
<http://www.openmicroscopy.org/site/support/bio-formats5.0/users/comlinetools/>`_.

Unzip the ``bftools.zip`` file into a memorable location for example ``tools``.

::

    mkdir ~/tools
    mv ~/Downloads/bftools.zip ~/tools/
    cd ~/tools
    unzip bftools.zip

Finally add the ``bftools`` directory to your ``PATH``.

::

    export PATH=$PATH:~/tools/bftools

.. note:: You may want to add the line above to your ``.bashrc`` file.

Install :mod:`jicimagelib`
--------------------------

Download the zip file from `githq
<https://githq.nbi.ac.uk/rg-matthew-hartley/jic-image-lib>`_ and unzip it.

::

    unzip jic-image-lib.git.zip

Finally install the :mod:`jicimagelib` package.

::

    cd jic-image-lib.git
    python setup.py install
