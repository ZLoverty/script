import os
import sys
import time
from myimagelib.corrLib import corrS
from myimagelib.myImageLib import readdata
from myimagelib.pivLib import read_piv

"""
batch_spatial_correlation
=========================

Batch spatial correlation computation.

.. rubric:: Syntax

.. code-block:: console

   python batch_spatial_correlation.py main_piv_foler

* main_piv_folder -- the folder containing many folders of PIV data. `piv_drop` for example.

.. rubric:: Test

.. code-block:: console

   python batch_spatial_correlation.py test_images\batch_spatial_correlation\piv_folder

.. rubric:: Edit

* Dec 15, 2021 -- Initial commit.
* Jan 05, 2023 -- Adapt myimagelib import style.
"""

if __name__=="__main__":
    main_piv_folder = sys.argv[1]
    parent_folder = os.path.split(main_piv_folder)[0]
    main_save_folder = os.path.join(parent_folder, "spatial_correlation")
    if os.path.exists(main_save_folder) == False:
        os.makedirs(main_save_folder)
    log_file = os.path.join(parent_folder, "batch_spatial_correlation_log.txt")
    with open(log_file, 'w') as f:
        f.write(time.asctime() + " \\ Start batch_spatial_correlation in {}\n".format(parent_folder))

    sfL = next(os.walk(main_piv_folder))[1]
    for sf in sfL:
        piv_folder = os.path.join(main_piv_folder, sf)
        with open(log_file, 'a') as f:
            f.write(time.asctime() + " \\ Computing {}\n".format(piv_folder))
        save_folder = os.path.join(main_save_folder, sf)
        os.system("python spatial_correlation.py {0} {1}".format(piv_folder, save_folder))
    with open(log_file, 'a') as f:
        f.write(time.asctime() + " \\ Computing finished!")
