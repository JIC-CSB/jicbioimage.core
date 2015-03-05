Interactive visualisation
=========================

We would like to be able to visualise both simple 2D images as well as stacks
of 2D images or even lists of lists of 2D images. When visualising more than
one image it should be possible to scroll through them or view them all in a
table format. Furthermore we would like to be able to annotate images with
things like circles, lines and text.

In order to achieve this whilst minimising complexity we propose that
responsibility of the viewer is simply to display collections of 2D images. And
the responsibility of annotating images lies with transform helper functions.
The user is then requested to build up the image(s) that he/she want to
visualise.

However the visualiser will still have both the concepts of loading an
image/stack as well as the concept of adding annotations layers.
          
.. note:: We propose to provide some built in factories that can be used
          to build common views of data using the required transforms.

Let us load a data manager and get an image and a zstack.

.. code-block:: python

    >>> from jicimagelib.image import DataManager, Stack
    >>> data_manager = DataManager()
    >>> data_manager.load('test.lif')
    >>> im_collection = data_manager[0]
    >>> im = im_collection.get_image(s=0, c=0, z=0, t=0)
    >>> zstack_iterator = im_collection.get_zstack_iterator(s=0, c=0, t=0) 
    >>> zstack = Stack.from_iterator(zstack_iterator)

Below is an example how one could view an individual image.

.. code-block:: python

    >>> from jicimagelib.viewer import ImageViewer
    >>> image_viewer = ImageViewer()
    >>> image_viewer.load(im)

Below is an example how one could view an image stack.

.. code-block:: python

    >>> from jicimagelib.viewer import StackViwer
    >>> stack_viewer = StackViwer()
    >>> stack_viewer.load(zstack)

Suppose that we wanted to highlight local maxima in the projected z-stack using
circles this may be achieved along the lines of the below.

.. code-block:: python

    >>> from jicimagelib.transform import ReduceStack
    >>> from jicimagelib.calculation import peak_local_max
    >>> from jicimagelib.render import Renderer
    >>> maximum_projection = ReduceStack(max)
    >>> z_max_proj_im = maximum_projection(zstack)
    >>> local_max_im, local_max_coords = jil.peak_local_max(z_max_proj_im)
    >>> renderer = Renderer()
    >>> circles_im = renderer.draw_circles(local_max_coords)
    >>> stack_viewer.load(zstack)
    >>> stack_viewer.add_image_layer(circles_im)

.. note:: The :class:`jicimagelib.viewer.StackViewer` should also have a
          :func:`jicimagelib.viewer.StackViewer.add_stack_layer` to be used if
          the layer should display information that is slice dependent.

.. note:: We may want to support other viewers for example summary information
          or intensity histograms. Furthermore we may want to be able to create
          a viewer that simply calls an external visualiser.
