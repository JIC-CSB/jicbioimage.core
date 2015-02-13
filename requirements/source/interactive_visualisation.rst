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
visualise. Note that this modifies the work-flow slightly.
          
.. graphviz::

   digraph mental_model {
     node [fontname=Sans, shape=box, style=filled];
     edge [fontname=Sans, fontsize=10];

     files [label="File(s)"];
     images [label="Image(s)"];
     derived_data [label="Derived data"];
     visualiser [label="Visualiser"];
     transformer [label="Transfomer"];

     files -> images [label="Read"];
     images -> files [label="Write"];
     {images, derived_data} -> transformer [label="Input"]
     images -> visualiser [label="Input"]
     transformer -> images [label="Transform"];
     images -> derived_data [label="Calculate"];
     
   }


.. note:: We propose to provide some built in factories that can be used
          to build common views of data using the required transforms.

Suppose that we wanted to highlight local minima on an image using circles this
may be achieved along the lines of the below.

.. code-block:: python

    >>> import jicimagelib as jil
    >>> data_manager = jil.DataManager()
    >>> data_manager.load('test.lif')
    >>> image_collection = data_manager[0]
    >>> z_max_proj_im = jil.project_using_function(image_collection.z_stack, max)
    >>> local_maxima = jil.peak_local_max(z_max_proj_im)
    >>> annotated_im = jil.add_circles(z_max_proj_im, local_maxima.coordinates)
    >>> jil.view(annotated_im)

Alternative suggestion for the viewer API.

.. code-block:: python

    >>> viewer = jil.ImageViewer()
    >>> viewer.view(annotated_im)

To toggle between the maximum z-stack projection and the image annotated with
the image one could use the syntax below to create a viewer with the two images
of interest.

.. code-block:: python

    >>> viewer = jil.ImageViewer()
    >>> viewer.view([z_max_proj_im, annotated_im])

Alternative syntax suggestion, which would allow adding more data to the viewer
ad-hoc, for example the entire z-stack.

.. code-block:: python

    >>> viewer = jil.ImageViewer()
    >>> viewer.load([z_max_proj_im, annotated_im])
    >>> viewer.load(image_collection.z_stack)

Suppose that we wanted to annotate all slices in a z-stack. In this case we
should probably have a helper function along the lines of the below.

.. code-block:: python

    >>> annotated_z_stack = jil.transform_all(jil.add_circles,
    ...                                       image_collection.z_stack,
    ...                                       local_maxima.coordinates)
    ...
    >>> viewer.clear()
    >>> viewer.load(annotated_z_stack)

.. warning:: The above may get too inefficient and cumbersome. Suggest that we
             functionality to be able to add layers and set their visibility.

.. code-block:: python

    >>> viewer.load(org_im)
    >>> circles = jil.circles(coordinates)
    >>> viewer.add_layer(circles)

MVC
---

.. warning:: Using the MVC pattern does not seem like a good fit for what we
             want to do. Instead we are in favor of creating simple viewers and
             transforms and using factories to build up more complicated
             composite views.

Should we use a model/view/controller (MVC) architectural pattern?

`<http://en.wikipedia.org/wiki/Model_view_controller>`_

In the GoF "Design Patterns" book the MVC is described in terms of the
``observer``, ``composite`` and ``strategy`` patterns.

The ``observer`` pattern being the view, for example textual/tabular summary
information an image or an intensity histogram.

The ``composite`` is a pattern for handing nested views, one could imaging
wanting to create a view along the lines of the below:

- view

  - original image
  - meta data

    - summary information
    - intensity histogram

The controller uses the ``strategy`` pattern as a means to decide how input is
interpreted by the view. For example if the model was a z-stack then the mouse
scroll might allow the user to scroll through the images in the z-stack in an
"image view", but do nothing with a view of summary information about the z-stack.
