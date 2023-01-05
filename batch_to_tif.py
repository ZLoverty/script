import os
from myimagelib.myImageLib import readdata
import sys
import time
import pandas as pd
"""
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
* Jan 05, 2023 -- Adapt myimagelib import style.
"""
main_folder = sys.argv[1]
l0 = readdata(main_folder, 'nd2')
print(time.asctime())
print("------------------------")
print("Start batch_to_tif on {}".format(main_folder))
print("The following nd2 files will be converted to tif sequences:")
l1 = readdata(main_folder, "raw")
l = pd.concat([l0, l1], axis=0)
for num, i in l.iterrows():
    print("\t{}".format(i.Dir))
# log_file = os.path.join(main_folder, 'batch_to_tif_log.txt')
# with open(log_file, 'w') as f:
#     f.write(time.asctime() + " // Start batch_to_tif in {}\n".format(main_folder))
#     f.write("The following files will be converted:\n")
#     f.write(repr(l))
#     f.write("\n\n")

if len(l) > 0:
    for num, i in l.iterrows():
        out_folder = os.path.splitext(i.Dir)[0]
        if os.path.exists(out_folder) == False:
            print(time.asctime() + " // Converting {} to tif".format(i.Dir))
            cmd = "python to_tif.py {}".format(i.Dir)
            os.system(cmd)
        else:
            print(time.asctime() + " // {} tif folder exists already, skipping".format(i.Dir))
else:
    print(time.asctime() + " // No nd2 file exists in the given folder.")
