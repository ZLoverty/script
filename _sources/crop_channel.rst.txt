
crop_channel
============

Crop channels from bifurcation AN images. In a typical bifurcation experiment, we have a 3-way micro-channel photoprinted on a resin. This micro-channel is cast on the active microtubule system at an oil-water interface. The chaotic turbulent-like motions of microtubules will be rectified by the micro-channels. Ratchet structures are used to set one of the channels as inlet. The flow then goes into either remaining channels, or into both at certain fractions. We study what is the "preferred" bifurcation of the flow. In the cropped images, predetermined positive (+) direction always points upward.

.. rubric:: Syntax

.. code-block:: console

   python crop_channel.py crop_data img_folder crop_folder

* crop_data: a table specifying how the raw images should be cropped. Typically, it consists 6 rows, where rows 1, 3, 5 contain rotation information, rows 2, 4, 6 contain cropping information.
* img_folder: raw images folder
* crop_folder: folder to save cropped images

.. note::

   * When creating crop_data in ImageJ, only select "bounding rectangle" in "Analyze -> Set measurements..."
   * When creating crop_data, DO remember to remove the scale !!!

.. rubric:: Edit

* Nov 03, 2022 -- Initial commit.
