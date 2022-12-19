
collect_preview
===============

Collect all the tif files under preview folder into the main folder. Assume file structure is shown below. All the tif files are put in folder "collect preview".

.. code-block:: console

   main_folder
   |-- parent1
       |-- preview
           |-- 0.tif
           |-- 1.tif
           |-- ...
   |-- parent2
       |-- preview
           |-- 0.tif
           |-- 1.tif
           |-- ..
   |-- collect_preview
       |-- parent1-0.tif
       |-- parent1-1.tif
       |-- parent2-0.tif
       |-- parent2-1.tif

.. rubric:: Syntax

.. code-block:: console

   python collect_preview main_folder

* crop_data: the folder that contains subfolders named "preview".

.. note::

   * preview folder need not be immediate subfolder of main_folder.

.. rubric:: Test

.. code-block:: console
   
   python collect_preview.py test_images\gen_preview
   
.. rubric:: Edit

:Dec 06, 2022: Initial commit.
