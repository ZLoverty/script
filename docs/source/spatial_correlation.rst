
spatial_correlation
===================

Compute correlation length of velocity and velocity orientation.


.. rubric:: Syntax

.. code-block:: console

   python cav_imseq.py input_folder output_folder

* input_folder -- folder of PIV data
* output_folder -- folder to save output

.. rubric:: Test

.. code-block:: console

   python spatial_correlation.py test_images\batch_spatial_correlation\piv_folder\00 test_images\batch_spatial_correlation\spatial_correlation\00

.. rubric:: Edit

* Aug 06, 2020 --
    1. change corrI return value according to the change of corrI(), to speed up the code,
    2. write parameters in log down sampling: instead of computing correlations for all frames, now only take 100 frames if the video is shorter than 100 frames, do the whole video
* Dec 13, 2021 --
    1. Rewrite doc string.
    2. Minor structural modification.
* Dec 15, 2021 --
    1. Rename to `spatial_correlation.py`,
    2. modify test script,
    3. replace PIV data loading snippet with `read_piv` function.
