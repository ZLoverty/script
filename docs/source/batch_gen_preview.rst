
batch_gen_preview
=================

Batch generate preview images from nd2 files. The code assumes the following folder structure:

.. code-block:: console

   main_folder
   |-- day1
       |-- 00.nd2
   |-- day2
       |-- 01.nd2

.. rubric:: Syntax

.. code-block:: console

   python batch_gen_preview.py main_folder

* main_folder -- any folder / parent folder that contains *\*.nd2* images.

.. rubric:: Test

.. code-block:: console

   python batch_gen_preview.py test_images\batch_to_tif

.. rubric:: Edit

* Dec 14, 2021 --
    1. Use system argument as input main folder.
    2. Implement main log file. iii) Better doc string.
* Dec 15, 2021 -- Remove the last os.sep of main_folder, so that it is ok to pass main_folder with "\" (win) or "/" (linux) at the end.
* Jan 05, 2023 -- Adapt myimagelib import style.
