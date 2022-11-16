
batch_to_tif
============

Batch convert *\*.nd2* files to .tif images by calling ``to_tif.py``. The code assumes the following folder structure:

.. code-block:: console

   main_folder
   |-- day1
       |-- 00.nd2
   |-- day2
       |-- 01.nd2

.. rubric:: Syntax

.. code-block:: console

   python batch_to_tif.py main_folder

* main_folder -- the folder containing *\*.nd2* files.

.. rubric:: Test

.. code-block:: console

   python batch_to_tif.py test_images\batch_to_tif

.. rubric:: Edit

* Dec 14, 2021 --
    * Use system argument as input main folder.
    * Implement main log file.
    * Better doc string.
* Jan 22, 2022 -- Remove the log file and print all the information to stdout. When using the code, use ``>>`` to save the screen message to a file. It's easier to locate the log file... This change should be applied to all the batch code.
