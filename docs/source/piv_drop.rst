
piv_drop
========

Perform PIV analysis on an image sequence of **bacteria in a droplet**. 

.. rubric:: Syntax

.. code-block:: console

   python piv_drop.py image_folder save_folder winsize overlap dt mask_dir

* image_folder -- folder containing .tif image sequence
* save_folder -- folder to save PIV data
* winsize, overlap, dt -- regular params
* mask_dir -- mask image dir

.. rubric:: Test

.. code-block:: console

   python piv_drop.py test_images\piv_drop test_images\piv_drop 40 20 0.02 test_images\piv_drop\mask.tif

.. rubric:: Edit

* Dec 09, 2021 -- Initial commit.
* Dec 16, 2021 -- i) use `PIV_masked()` as the core algorithm, ii) implement multiprocessing with `Pool`
* Jan 16, 2022 -- add info print, can be used with ">>" to write log.
* Feb 15, 2022 -- remove printing steps to avoid log file spamming.
* Mar 03, 2022 -- i) Reverse the multi-thread code to linear, ii) use `droplet_image` class for the script, iii) no longer print PIV settings to screen, save a `piv_params` json instead
* Jan 05, 2023 -- Adapt myimagelib import style.
