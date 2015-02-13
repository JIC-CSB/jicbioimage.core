Transformations
===============

In the general case there will be two different types of transformations which
correspond to the behaviour of Python's built-in ``map`` and ``reduce``
functions.

An example of a ``map`` transformation would be a Gaussian blur.

.. code-block:: python

    >>> from jicimagelib import transformation as tr
    >>> gaussian_im = tr.gaussian(org_im, sigma=2)

Note that the history of the transformations is saved in the image.

.. code-block:: python

    >>> gaussian_im.history
    [ ..., '<function jicimagelib.transformation.gaussian sigma=2>']

Another example of a ``map`` transformation would be a text annotation.

.. code-block:: python

    >>> annotated_im = tr.add_text(org_im, 5, 5, 'Hello')

A ``reduce`` transformation would be something like a z-stack projection.


.. code-block:: python

    >>> z_max_proj_im = tr.project(z_stack, max)

.. note:: Matthew how did you implement the above? Could it be generalised to
          any ``reduce`` situation?
