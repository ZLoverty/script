
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
* Dec 06, 2022 -- i) Enable this script to process \*.nd2 files. ii) Check if reults already exist. iii) Pick up job from middle. (Only work for nd2 PIV for the moment) iv) query num frames using metadata, rather than ``images.shape``
* Dec 07, 2022 -- Fix undefined "start" issue.
* Jan 05, 2023 -- (i) Check if img exists. (ii) Adapt myimagelib import style.
