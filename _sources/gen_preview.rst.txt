
gen_preview
===========

Generete preview images of given folder.

Assumed folder structure:

.. code-block:: console

   folder
   |-- 00.nd2
   |-- 01.nd2
   |-- ...

The script will extract the images of each \*.nd2 file and save as a tif image with the same name as the corresponding \*.nd2 files. 

.. rubric:: Syntax

.. code-block:: console

   python gen_preview.py nd2Dir

* nd2Dir -- nd2 file directory
* out_folder -- folder to save a tif file with the same name as the nd2 file

.. rubric:: Test

.. code-block:: console

   python gen_preview.py test_images\batch_to_tif\day1\00.nd2 test_images\batch_to_tif\preview\day1


.. rubric:: Edit

* Dec 12, 2021 -- Initial commit
* Dec 13, 2021 -- `cp` command is not platform independent. Use python native tools `shutil.copy` instead.
* Dec 14, 2021 -- Now work on single .nd2 file, instead of a folder of tif sequences.
* Dec 06, 2022 -- Now save first and last frames for a single nd2. Change of default behavior!
