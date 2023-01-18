
piv_overlay
===========

Generate PIV arrow overlayed images for PIV visual inspection and illustration.

.. rubric:: Syntax

.. code-block:: console

   python piv_overlay.py piv_folder img_folder output_folder sparcity

* piv_folder -- folder containing PIV data in the form of .csv files
* img_folder -- folder containing .tif images
* output_folder -- folder to save the PIV overlay images in .jpg files (rescaled to 360 pixels in width)
* sparcity -- density of PIV arrows, higher value corresponds to sparcer arrows

.. rubric:: Test

.. code-block:: console

   python piv_overlay.py test_images\piv_drop test_images\piv_drop test_images\piv_overlay 1

.. rubric:: Edit

* Jan 03, 2022 --
    1. move from PIV to script,
    2. set scale,
    3. update docstring
    4. minor structural changes

    .. note::
       See `PIV technical report Sec II.A.1 <https://github.com/ZLoverty/DE/blob/main/Notes/PIV_technical_report.pdf>`_ for the reasoning of scale settings.

* Jan 22, 2022 -- reduce scale by 1.5 to increase the arrow size
* Mar 03, 2022 --
    1. Use `droplet_image` class to rewrite the script,
    2. remove logging
* Jan 05, 2023 -- Adapt myimagelib import style.
