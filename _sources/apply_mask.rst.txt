
apply_mask
==========

Apply mask on PIV data. It sets all the irrelevant (x, y in the False region of the mask) PIV velocity to np.nan.

.. rubric:: Syntax

.. code-block:: console

   python apply_mask.py piv_folder mask_dir

* piv_folder: folder containing PIV data (csv sequence)
* mask_dir: directory of a tif binary mask, of the same shape as raw images.
* erode: number of pixels to erode from the True region (this makes the mask smaller, reducing boundary effect). Default to 32, a good value is the winsize of PIV.

.. note::

   The original PIV data will be overwritten, since they are no longer useful.

.. rubric:: Test

.. code-block:: console

   python apply_mask.py test_images\apply_mask test_images\apply_mask\A.tif

.. rubric:: Edit

* Nov 03, 2022 -- Initial commit.
* Dec 01, 2022 -- Remove erosion step. Mask should be used as it is.
