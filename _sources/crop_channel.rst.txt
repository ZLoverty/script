
crop_channel
============

Crop channels from bifurcation AN images. In a typical bifurcation experiment, we have a 3-way micro-channel photoprinted on a resin. This micro-channel is cast on the active microtubule system at an oil-water interface. The chaotic turbulent-like motions of microtubules will be rectified by the micro-channels. Ratchet structures are used to set one of the channels as inlet. The flow then goes into either remaining channels, or into both at certain fractions. We study what is the "preferred" bifurcation of the flow. In the cropped images, predetermined positive (+) direction always points upward.

This code crops the original multi-microchannel images into single channels, to allow more efficient PIV analysis. Ono top of cropping, the code also remove the background static feature from the images, by dividing the images by the median of the image stack. The images are then converted from float64 to 8-bit to save the storage space.

.. rubric:: Syntax

.. code-block:: console

   python crop_channel.py crop_data nd2Dir

* crop_data: the directory to a \*.csv file specifying how the raw images should be cropped. Typically, it consists 6 rows, where rows 1, 3, 5 contain rotation information, rows 2, 4, 6 contain cropping information. The image will rotate according to row 1, and cropped according to row 2, and so on so forth. The file is typically generated using ImageJ measurement tool.
* nd2Dir: full directory of the \*.nd2 file to be cropped.

The folder structure is illustrated below:

.. code-block:: console

   |-- nd2_folder
       |-- 00.nd2
       |-- 01.nd2
       |-- ...
       |-- crop_channel
           |-- 00_A.tif
           |-- 00_B.tif
           |-- 00_C.tif

.. note::

   * When creating crop_data in ImageJ, only select "bounding rectangle" in "Analyze -> Set measurements..."
   * When creating crop_data, DO remember to remove the scale !!!

.. rubric:: Edit

* Nov 03, 2022 -- Initial commit.
* Nov 23, 2022 -- To make the workflow consistent with Claire's, it is more convenient to crop the channel region directly from the \*.nd2 file, and save as tifstack. Now crop directly from \*.nd2 files to  tifstack.
* Jan 05, 2023 -- Adapt myimagelib import style.
