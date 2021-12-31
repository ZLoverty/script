import os
import sys
import time
from corrLib import readdata

"""
GENERAL
=======
Batch mean velocity computation.

USAGE
=====
python batch_mean_velocity.py main_piv_foler

main_piv_folder is the folder containing many folders of PIV data. `piv_drop` for example.

TEST
====
python batch_mean_velocity.py test_images\batch_spatial_correlation\piv_folder

LOG
===
Fri Dec 31 23:48:12 2021 \ Start batch_mean_velocity in test_images\batch_spatial_correlation
Fri Dec 31 23:48:12 2021 \ Computing test_images\batch_spatial_correlation\piv_folder\00
Fri Dec 31 23:48:13 2021 \ Computing test_images\batch_spatial_correlation\piv_folder\01
Fri Dec 31 23:48:14 2021 \ Computing finished!

EDIT
====
Dec 31, 2021 -- Initial commit.
"""

if __name__=="__main__":
    main_piv_folder = sys.argv[1]
    parent_folder = os.path.split(main_piv_folder)[0]
    main_save_folder = os.path.join(parent_folder, "mean_velocity")
    if os.path.exists(main_save_folder) == False:
        os.makedirs(main_save_folder)
    log_file = os.path.join(parent_folder, "batch_mean_velocity_log.txt")
    with open(log_file, 'w') as f:
        f.write(time.asctime() + " \\ Start batch_mean_velocity in {}\n".format(parent_folder))

    sfL = next(os.walk(main_piv_folder))[1]
    for sf in sfL:
        piv_folder = os.path.join(main_piv_folder, sf)
        with open(log_file, 'a') as f:
            f.write(time.asctime() + " \\ Computing {}\n".format(piv_folder))
        os.system("python mean_velocity.py {0} {1}".format(piv_folder, main_save_folder))
    with open(log_file, 'a') as f:
        f.write(time.asctime() + " \\ Computing finished!")
