import os
from corrLib import readdata
import sys
import time

"""
GENERAL
=======
Batch generate preview images from nd2 files.
The code assumes the following folder structure:

main_folder
|- day1
  |- 00.nd2
|- day2
  |- 01.nd2

USAGE
=====
python batch_gen_preview.py main_folder

TEST
====
python batch_gen_preview.py test_images\batch_to_tif

LOG
===
Sat Jan 22 15:20:44 2022
------------------------
Run batch_gen_preview on test_images\batch_to_tif
Results will be saved in test_images\batch_to_tif\preview
The following files will be processed:
        test_images\batch_to_tif\day1\00.nd2
        test_images\batch_to_tif\day2\01.nd2
------------------------
Generating preview for test_images\batch_to_tif\day1\00.nd2
D:\miniconda\lib\site-packages\nd2reader\raw_metadata.py:187: UserWarning: Z-levels details missing in metadata. Using Z-coordinates instead.
  warnings.warn("Z-levels details missing in metadata. Using Z-coordinates instead.")
test_images\batch_to_tif\day1\00.nd2 -> test_images\batch_to_tif\preview\day1\00.tif
Generating preview for test_images\batch_to_tif\day2\01.nd2

D:\miniconda\lib\site-packages\nd2reader\raw_metadata.py:187: UserWarning: Z-levels details missing in metadata. Using Z-coordinates instead.
  warnings.warn("Z-levels details missing in metadata. Using Z-coordinates instead.")
test_images\batch_to_tif\day2\01.nd2 -> test_images\batch_to_tif\preview\day2\01.tif

EDIT
====
Dec 14, 2021 -- i) Use system argument as input main folder. ii) Implement main log file. iii) Better doc string.
Dec 15, 2021 -- Remove the last os.sep of main_folder, so that it is ok to pass main_folder with "\" (win) or "/" (linux) at the end.
"""
main_folder = sys.argv[1].rstrip(os.sep)
out_folder = os.path.join(main_folder, "preview")
if os.path.exists(out_folder) == False:
    os.makedirs(out_folder)

l = readdata(main_folder, 'nd2')

print(time.asctime())
print("------------------------")
print("Run batch_gen_preview on {}".format(main_folder))
print("Results will be saved in {}".format(out_folder))
print("The following files will be processed:")
for num, i in l.iterrows():
    print("\t{}".format(i.Dir))
print("------------------------")
if len(l) > 0:
    for num, i in l.iterrows():
        out_file = i.Dir.replace(main_folder, out_folder).replace(".nd2", ".tif")
        if os.path.exists(out_file) == False:
            print("Generating preview for {}".format(i.Dir))
            cmd = "python gen_preview.py {0} {1}".format(i.Dir, out_file)
            os.system(cmd)
        else:
            print("{} exists already, skipping".format(out_file))
else:
    print(time.asctime() + " \\ No nd2 file exists in the given folder.")
