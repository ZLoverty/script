
velocity_autocorr
=================

Apply autocorrelation analysis on sequential PIV data.

.. rubric:: Syntax

.. code-block:: console

   python velocity_autocorr.py piv_folder out_folder [fps=50] [cutoff=2000]

* fps: the imaging frame rate
* cutoff: frame number above which the velocity data are not included in the analysis

.. rubric:: Test

.. code-block:: console

   python velocity_autocorr.py test_images\velocity_autocorr test_images\velocity_autocorr\vac_result 50 20

.. rubric:: Edit

* Dec 13, 2021 -- Initial commit.
* Feb 21, 2022 -- Rewrite with new functions.
* Mar 16, 2022 --

    1. Rewrite with piv_data class
    2. Use fps instead of dt as input argument
    3. Modify doc string

* Mar 23, 2022 -- add smoothn as an optional smoothing method
* Nov 15, 2022 -- Make ``fps`` and ``cutoff`` real *keyword* args.
