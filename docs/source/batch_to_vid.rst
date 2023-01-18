
batch_to_vid
============

Batch convert .tif images to .avi by calling ``to_vid.py`` (more details can be found in to_vid.py doc string).
The code assumes the following folder structure:

.. code-block:: console

   main_folder
   |-- day1
       |-- 00.nd2
       |-- 00
           |-- 8-bit
           |-- raw
   |-- day2
       |-- 01.nd2
       |-- 01
          |-- 8-bit
          |-- raw

.. rubric:: Syntax

.. code-block:: console

   python batch_to_vid.py main_folder

.. rubric:: Test

.. code-block:: console

   python batch_to_vid.py test_images\batch_to_vid

.. rubric:: Edit

* Dec 11, 2021 -- add main_folder argument: it's better not to edit the script too often! (issue) to_vid.py alone now performs the function of batch_to_vid.py. Although the work can be done, it's not a consistent design with the to_tif. Need to work on this later.
* Jan 05, 2023 -- Adapt myimagelib import style.

.. deprecated:: 1.0

   Use ``to_vid.py`` instead.
