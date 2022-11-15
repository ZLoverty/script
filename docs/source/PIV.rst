
PIV
===

This is the most basic version of PIV.

.. rubric:: Syntax

.. code-block:: console

   python PIV.py img_folder winsize dt piv_folder

* img_folder: tif sequence folder to be analyzed.
* winsize: interrogation window size.
* dt: time interval between adjacent frames (1/FPS).
* piv_folder: folder to save PIV results.

.. note::

   In this implementation, we set overlap as half of winsize.

.. rubric:: Edit

* Nov 03, 2022 -- Initial commit.
