
PIV
===

This is the most basic version of PIV.

.. rubric:: Syntax

.. code-block:: console

   python PIV.py img winsize dt piv_folder

* img: can be i) tif sequence folder, ii) nd2 file dir to be analyzed.
* winsize: interrogation window size.
* dt: time interval between adjacent frames (1/FPS).
* piv_folder: folder to save PIV results.

.. note::

   In this implementation, we set overlap as half of winsize.

.. rubric:: Edit

* Nov 03, 2022 -- Initial commit.
* Dec 06, 2022 -- Enable this script to process \*.nd2 files.
