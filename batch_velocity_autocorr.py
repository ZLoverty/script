import os
import sys
import time
from corrLib import readdata

"""
GENERAL
=======
Batch velocity autocorrelation computation.

USAGE
=====
python batch_mean_velocity.py main_piv_foler

main_piv_folder is the folder containing many folders of PIV data. `piv_drop` for example.

TEST
====
python batch_velocity_autocorr.py test_images\batch_spatial_correlation\piv_folder

LOG
===
Mon Feb 21 17:58:32 2022
------------------------
Run batch_velocity_autocorr on test_images\batch_spatial_correlation\piv_folder
Results will be saved in test_images\batch_spatial_correlation\velocity_autocorr
The following files will be processed:
        test_images\batch_spatial_correlation\piv_folder\00
        test_images\batch_spatial_correlation\piv_folder\01
------------------------

Mon Feb 21 17:58:33 2022 // Computing VACF of test_images\batch_spatial_correlation\piv_folder\00

EDIT
====
Feb 21, 2022 -- Initial commit.
"""


main_piv_folder = sys.argv[1].rstrip(os.sep)
parent_folder = os.path.split(main_piv_folder)[0]
main_save_folder = os.path.join(parent_folder, "velocity_autocorr")
sfL = next(os.walk(main_piv_folder))[1]
if os.path.exists(main_save_folder) == False:
    os.makedirs(main_save_folder)

print(time.asctime())
print("------------------------")
print("Run batch_velocity_autocorr on {}".format(main_piv_folder))
print("Results will be saved in {}".format(main_save_folder))
print("The following files will be processed:")
for sf in sfL:
    print("\t{}".format(os.path.join(main_piv_folder, sf)))
print("------------------------")

for sf in sfL:
    piv_folder = os.path.join(main_piv_folder, sf)
    print(time.asctime() + " Computing velocity autocorrelation of {}".format(os.path.join(main_piv_folder, sf)))
    os.system("python velocity_autocorr.py {0} {1}".format(piv_folder, main_save_folder))
