
remove_background
=================

This script removes the stationary background of a tif sequence in a given folder. Specifically, it does:

- Median z-projection
- divide raw images by the projection

By default, it saves the output images to a "..._rb" folder, where "..." is the original folder name. For example, images from crop_channel/crop-0 will be processed and saved in crop_channel/crop-0_rb.

.. rubric:: Syntax

.. code-block:: console

   python remove_background.py img_folder

* img_folder -- tif sequence folder to be processed.

.. note::

   Here the processed images are converted to 8-bit images. Autocontrast is applied.

.. rubric:: Edit

* Nov 03, 2022 -- Initial commit.
