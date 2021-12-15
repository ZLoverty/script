import os
import sys
import time
from corrLib import corrS, readdata
from pivLib import read_piv

"""
GENERAL
=======
Batch spatial correlation computation.

USAGE
=====
python batch_spatial_correlation.py main_piv_foler

main_piv_folder is the folder containing many folders of PIV data. `piv_drop` for example.

TEST
====
python batch_spatial_correlation.py test_images\batch_spatial_correlation\piv_folder

LOG
===
Wed Dec 15 23:07:01 2021 \ Start batch_spatial_correlation in test_images\batch_spatial_correlation
Wed Dec 15 23:07:01 2021 \ Computing test_images\batch_spatial_correlation\piv_folder\00
Wed Dec 15 23:07:03 2021 \ Computing test_images\batch_spatial_correlation\piv_folder\01
Wed Dec 15 23:07:05 2021 \ Computing finished!

EDIT
====
Dec 15, 2021 -- Initial commit.
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
