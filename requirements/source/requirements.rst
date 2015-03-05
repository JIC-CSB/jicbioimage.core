Requirements
============

We would like to have a Python library that allows us to rapidly explore
microscopy data in an interactive and iterative fashion.

Specifically we will need:

  - Data structures that can understand high dimensional microscopy data, e.g.
    z-stacks and time series, and that make it easy to visualise and work with
    the image data

  - A system that makes it easy to read in microscopy data

  - Good documentation of all built-in transforms and calculations, i.e. it
    should be clear what a tranform/calculation does and things should not
    happen "auto-magically"

  - Integration with IPython qtconsole/notebook to enable interactive
    visualisation

  - Means to easily augment and annotate images

  - Basic type checking to help prevent silly mistakes

  - A system tracks history and settings of how images were manipulated

The library should enable the work-flow outlined below:

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


