
batch_mean_velocity
===================

Batch mean velocity computation from PIV data.

.. rubric:: Syntax

.. code-block:: console

   python batch_mean_velocity.py main_piv_foler

* main_piv_folder -- the folder containing many folders of PIV data. ``piv_drop`` for example.

.. rubric:: Test

.. code-block:: console

   python batch_mean_velocity.py test_images\batch_spatial_correlation\piv_folder

.. rubric:: Edit

* Dec 31, 2021 -- Initial commit.
* Jan 22, 2022 -- Strip the os.sep at the end of the given PIV directory, if exists.
* Jan 05, 2023 -- Adapt myimagelib import style.
