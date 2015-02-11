Interactive visualisation
=========================

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
