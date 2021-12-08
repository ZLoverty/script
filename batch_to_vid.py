import os
from corrLib import readdata

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
Input the main_folder by editing the first line of the code and run the script by
```
python batch_to_vid.py
```
Test
====
set the first line:
```
main_folder = os.path.join('test_images', 'batch_to_vid')
"""
# main_folder = '/media/zhengyang/NothingToSay/DE/'
main_folder = os.path.join('test_images', 'batch_to_vid')
folders = next(os.walk(main_folder))[1]
print(folders)
for sf in folders:
    folder = os.path.join(main_folder, sf)
    cmd = "python to_vid.py {} fmt=8b%05d.tif fps=50".format(folder)
    os.system(cmd)

