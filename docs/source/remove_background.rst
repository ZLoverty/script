
remove_background
=================

This script removes the stationary background of a tif sequence in a given folder. Specifically, it does:

- Median z-projection
- divide raw images by the projection

By default, it replaces the original images with background removed images. 

.. rubric:: Syntax

.. code-block:: console

   python remove_background.py img_folder

* img_folder -- A folder of tiffstacks.

.. note::

   Here the processed images are converted to 8-bit images. Autocontrast is applied.

.. warning::

   Since the bifurcation images always require background subtraction, this procedure is included in the "crop_channel.py" script. We can still apply this script, but it essentially has no effect.
   
.. rubric:: Edit

* Nov 03, 2022 -- Initial commit.
* Jan 04, 2023 -- (i) Target on a folder of tiffstacks. Remove the background of each tiffstack, based on their own median image. (ii) Change default saving behavior: now REPLACE the original images with background removed images.
* Jan 05, 2023 -- Adapt myimagelib import style.
