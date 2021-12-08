import os
from corrLib import readdata

"""
General
=======
Batch convert .nd2 files to .tif images by calling `to_tif.py`.
The code assumes the following folder structure:

main_folder
|- day1
  |- 00.nd2
|- day2
  |- 01.nd2

Usage
=====
Input the main_folder by editing the first line of the code and run the script by
```
python batch_to_tif.py
```
Test
====
set the first line:
```
main_folder = os.path.join('test_images', 'batch_to_tif')
"""
# main_folder = '/media/zhengyang/NothingToSay/DE/'
main_folder = os.path.join('test_images', 'batch_to_tif')
folders = next(os.walk(main_folder))[1]
print(folders)
for sf in folders:
    folder = os.path.join(main_folder, sf)
    l = readdata(folder, 'nd2')
    if len(l) > 0:
        for num, i in l.iterrows(): # check if folder exists
            out_folder = os.path.join(folder, i.Name)
            print("converting {} to tif".format(out_folder))
            if os.path.exists(out_folder) == False:
                cmd = "python to_tif.py {}".format(i.Dir)
                os.system(cmd)
            else:
                print("tif folder exists already, skipping")

