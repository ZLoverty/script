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
Tue Dec 14 11:59:29 2021 \ Start batch_to_tif in test_images\batch_to_tif
Tue Dec 14 14:10:47 2021 \ Start batch_gen_preview in test_images\batch_to_tif
The following files will be converted:
  Name                                   Dir
0   00  test_images\batch_to_tif\day1\00.nd2
1   01  test_images\batch_to_tif\day2\01.nd2

Tue Dec 14 14:10:47 2021 \ Generating preview for test_images\batch_to_tif\day1\00.nd2
Tue Dec 14 14:10:49 2021 \ Generating preview for test_images\batch_to_tif\day2\01.nd2

EDIT
====
Dec 14, 2021 -- i) Use system argument as input main folder. ii) Implement main log file. iii) Better doc string.
"""
main_folder = sys.argv[1]
out_folder = os.path.join(main_folder, "preview")
if os.path.exists(out_folder) == False:
    os.makedirs(out_folder)

l = readdata(main_folder, 'nd2')

log_file = os.path.join(main_folder, 'batch_gen_preview_log.txt')
with open(log_file, 'w') as f:
    f.write(time.asctime() + " \\ Start batch_gen_preview in {}\n".format(main_folder))
    f.write("The following files will be converted:\n")
    f.write(repr(l))
    f.write("\n\n")

if len(l) > 0:
    for num, i in l.iterrows():
        out_file = i.Dir.replace(main_folder, out_folder).replace(".nd2", ".tif")
        if os.path.exists(out_file) == False:
            print("Generating preview for {}".format(i.Dir))
            with open(log_file, 'a') as f:
                f.write(time.asctime() + " \\ Generating preview for {}\n".format(i.Dir))
            cmd = "python gen_preview.py {0} {1}".format(i.Dir, out_file)
            os.system(cmd)
        else:
            print("{} exists already, skipping".format(out_file))
            with open(log_file, 'a') as f:
                f.write(time.asctime() + " \\ {} exists already, skipping\n".format(out_file))
else:
    with open(log_file, 'a') as f:
        f.write(time.asctime() + " \\ No nd2 file exists in the given folder.")
