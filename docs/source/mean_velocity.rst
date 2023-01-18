
mean_velocity
=============

Compute mean velocity of PIV data.

1. Compute the magnitude of each PIV arrow
2. Take average of these arrows

.. rubric:: Syntax

.. code-block:: console

   python mean_velocity.py piv_folder out_folder

* piv_folder -- folder containing PIV data (.csv), file names indicate frame number
* out_folder -- mean velocity data file (.csv), contain frame and mean_v columns

A folder of PIV files are used to generate a single mean velocity data file.

.. rubric:: Test

.. code-block:: console

   python mean_velocity.py test_images\piv_drop test_images\mean_velocity

.. rubric:: Edit

* Dec 31, 2021 -- Initial commit.
* Jan 02, 2021 -- Minor changes in docstring.
* Jan 05, 2023 -- Adapt myimagelib import style.
