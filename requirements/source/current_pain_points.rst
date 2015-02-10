Current pain points
===================

Currently we tend to visualise and do simple transformations of images in
ImageJ. We then tend to try to create a more automated and reproducible
work-flow using Python. This is painful in that the analysis needs to
be done twice using two different methods.

Furthermore both ImageJ and Python have pain points in themselves.

ImageJ is painful to use because:

  - The GUI is complex and non-intuitive
  - Analysis requires too many clicks
  - Analysis is non-reproducible (one forgets which buttons to click)
  - Things happen "auto-magically" and there is poor documentation of what the
    different buttons actually do to the image
  - It is prone to automatically update its tools during the life-time of a
    project
  - There is no undo or history

Python is painful to use because:

  - Pre-processing is needed to convert microscopy images into a file format
    that can be parsed
  - One needs to make Python understand the structure of the microscopy data
    (e.g. z-stacks, time series)
  - There is no out of the box way of visualising high dimensional image data
  - One often ends up using several imaging libraries (PIL, scipy.ndimage,
    scikit-image, opencv) and these have subtly different representations of
    images
  - It is easy to inadvertently loose data, for example PIL compresses data to
    fit into 8-bit images when writing them to file
  - The libraries that one make use of are complex and sometimes non-intuitive
    which means that one is constantly re-learning how to parse data using the
    different imaging libraries and how to display images using matplotlib
