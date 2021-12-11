import os
import time
from corrLib import readdata
import sys

"""
GENERAL
=======
Run `extractImages.py` on multiple .raw files.

Folder structure:
folder
|- sf1
  |- 1.raw
  |- ...
|- sf2
  |- 2.raw
  |- ...
|- ...

The script will search for all the .raw files under the given folder, then use `extractImages.py` on them. 

Steps:
i) search for .raw
ii) check if output folders exists
iii) if not, call `extractImages.py`
iv) write a log in **batch_extractImages_log.txt**

USAGE
=====
python batch_extractImages.py folder

TEST
====
python batch_extractImages.py test_images\batch_extractImages

LOG
===
(successful)
Sat Dec 11 23:27:43 2021 \ start extracting .raw files in test_images\batch_extractImages
Sat Dec 11 23:27:44 2021 \ test_images\batch_extractImages: Extraction DONE!
Sat Dec 11 23:27:46 2021 \ test_images\batch_extractImages: Extraction DONE!
(already exists)
Sat Dec 11 23:29:15 2021 \ start extracting .raw files in test_images\batch_extractImages
Sat Dec 11 23:29:15 2021 \ test_images\batch_extractImages: Output folders exist, skipping ...
Sat Dec 11 23:29:15 2021 \ test_images\batch_extractImages: Output folders exist, skipping ...

"""

if __name__ == "__main__":
    folder = sys.argv[1]    
    # create export log
    export_log = os.path.join(folder, "batch_extractImages_log.txt")
    with open(export_log, 'w') as f:
        f.write(time.asctime() + ' \\ start extracting .raw files in {}\n'.format(folder))
        
    # search for .raw files
    l = readdata(folder, 'raw')
    for num, i in l.iterrows():
        print(time.asctime() + " \\ Extracting {}".format(i.Dir))
        parent_folder = os.path.split(i.Dir)[0]
        out_raw_folder = os.path.join(parent_folder, 'raw')
        out_8_folder = os.path.join(parent_folder, '8-bit')
        # check if output folders exist
        if os.path.exists(out_raw_folder) and os.path.exists(out_raw_folder):
            print("Output folders exist, skipping ...")
            with open(export_log, 'a') as f:
                f.write(time.asctime() + ' \\ {}: Output folders exist, skipping ...\n'.format(folder))
        else:
            os.system("python extractImages.py {}".format(parent_folder))
            with open(export_log, 'a') as f:
                f.write(time.asctime() + ' \\ {}: Extraction DONE!\n'.format(folder))
                
            