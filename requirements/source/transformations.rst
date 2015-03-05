Transformations
===============

Transformations should only ever be from a single
:class:`jicimagelib.image.Image` instance to a single instance of a
:class:`jicimagelib.image.Image` with optional arguments. The optional
arguments could be a sigma value in the case of a Gaussian transform and
another image in the case of the watershed algorithm.

Converting all :class:`jicimagelib.image.Image` instances in a
:class:`jicimagelib.image.Stack` then simply becomes a map of a transform.

.. note:: The implication of transformation being only single image to single
          image in the context of mapping a tranform to a stack. This means
          that any optional arguments (such as a second input image) would be
          the same for all slices in the stack.

Converting a :class:`jicimagelib.image.Stack` to a
:class:`jicimage.image.Image` is analogous to Python's built-in :func:`reduce`
function.

.. code-block:: python

    >>> from jicimagelib.transform import Gaussian
    >>> gaussian = Gaussian(sigma=2)
    >>> gaussian_im = gaussian(org_im)

.. note:: The style of above where the settings are applied to an instance of a
          of a callable class makes it easy to pass the callable to a mapper.

Note that the history of the transformations is saved in the image.

.. code-block:: python

    >>> gaussian_im.history
    [ ..., '<Gaussian(sigma=2)>']


Now let us apply the gaussian tranform to all the images in a stack.

.. code-block:: python

    >>> from jicimagelib.tranform import StackMap
    >>> stack_map = StackMap()
    >>> guassian_stack = stack_map(stack, gaussian)

Alternatively, the map function could be built into the
:class:`jicimage.image.Stack` class.

.. code-block:: python

    >>> guassian_stack = stack.map(gaussian)


Below is an illustration of how a stack can be reduced to an image.

.. code-block:: python

    >>> from jicimagelib.transform import ReduceStack
    >>> maxium_projection = ReduceStack(max)
    >>> z_max_proj_im = maxium_projection(z_stack)
