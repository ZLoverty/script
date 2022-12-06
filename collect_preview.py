import sys
import os
from shutil import copyfile

"""
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
"""

main_folder = sys.argv[1]
save_folder = os.path.join(main_folder, "collect_preview")
if os.path.exists(save_folder) == False:
    os.makedirs(save_folder)
for r, s, f in os.walk(main_folder):
    if os.path.split(r)[1] == "preview":
        for filename in f:
            if filename.endswith(".tif"):
                print("collect {}".format(os.path.join(r, filename)))
                new_name = os.path.split(os.path.split(r)[0])[1] + "-" + filename
                copyfile(os.path.join(r, filename), os.path.join(save_folder, new_name))