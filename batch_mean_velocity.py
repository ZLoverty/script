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
Run batch_mean_velocity on test_images\batch_spatial_correlation\piv_folder
Results will be saved in test_images\batch_spatial_correlation\mean_velocity
The following files will be processed:
        test_images\batch_spatial_correlation\piv_folder\00
        test_images\batch_spatial_correlation\piv_folder\01

------------------------
Sat Jan 22 15:32:40 2022 // Computing mean velocity of test_images\batch_spatial_correlation\piv_folder\00
Sat Jan 22 15:32:41 2022 // Computing mean velocity of test_images\batch_spatial_correlation\piv_folder\01

EDIT
====
Dec 31, 2021 -- Initial commit.
"""

if __name__=="__main__":
    main_piv_folder = sys.argv[1]
    parent_folder = os.path.split(main_piv_folder)[0]
    main_save_folder = os.path.join(parent_folder, "mean_velocity")
    sfL = next(os.walk(main_piv_folder))[1]
    if os.path.exists(main_save_folder) == False:
        os.makedirs(main_save_folder)

    print(time.asctime())
    print("------------------------")
    print("Run batch_mean_velocity on {}".format(main_piv_folder))
    print("Results will be saved in {}".format(main_save_folder))
    print("The following files will be processed:")
    for sf in sfL:
        print("\t{}".format(os.path.join(main_piv_folder, sf)))
    print("------------------------")

    for sf in sfL:
        piv_folder = os.path.join(main_piv_folder, sf)
        print(time.asctime() + " // Computing mean velocity of {}".format(piv_folder))
        os.system("python mean_velocity.py {0} {1}".format(piv_folder, main_save_folder))
