import os
from corrLib import readdata
import sys

"""
General
=======
Batch convert .tif images to .avi by calling `to_vid.py` (more details can be found in to_vid.py doc string).
The code assumes the following folder structure:

main_folder
|- day1
  |- 00.nd2
  |- 00
    |- 8-bit
    |- raw
|- day2
  |- 01.nd2
  |- 01
    |- 8-bit
    |- raw

Usage
=====
python batch_to_vid.py main_folder

Test
====
python batch_to_vid.py test_images\batch_to_vid

LOG
===


EDIT
====
Dec 11, 2021 -- add main_folder argument: it's better not to edit the script too often!
                (issue) to_vid.py alone now performs the function of batch_to_vid.py. 
                Although the work can be done, it's not a consistent design with the to_tif.
                Need to work on this later. 
"""

if __name__=="__main__":
    main_folder = sys.argv[1]
    folders = next(os.walk(main_folder))[1]
    print(folders)
    for sf in folders:
        folder = os.path.join(main_folder, sf)
        cmd = "python to_vid.py {} fmt=8b%05d.tif fps=50".format(folder)
        os.system(cmd)

