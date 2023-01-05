from myimagelib.pivLib import PIV
import sys
import os
from skimage import io
from myimagelib.myImageLib import readdata, show_progress
import pandas as pd
from nd2reader import ND2Reader

"""
PIV
===

This is the most basic version of PIV.

.. rubric:: Syntax

.. code-block:: console

   python PIV.py img winsize dt piv_folder

* img: can be i) tif sequence folder, ii) nd2 file dir to be analyzed.
* winsize: interrogation window size.
* dt: time interval between adjacent frames (1/FPS).
* piv_folder: folder to save PIV results.

.. note::

   In this implementation, we set overlap as half of winsize.

.. rubric:: Edit

* Nov 03, 2022 -- Initial commit.
* Dec 06, 2022 -- i) Enable this script to process \*.nd2 files. ii) Check if reults already exist. iii) Pick up job from middle. (Only work for nd2 PIV for the moment) iv) query num frames using metadata, rather than ``images.shape``
* Dec 07, 2022 -- Fix undefined "start" issue.
* Jan 05, 2023 -- (i) Check if img exists. (ii) Adapt myimagelib import style.
"""

img = sys.argv[1]
winsize = int(sys.argv[2])
dt = float(sys.argv[3])
piv_folder = sys.argv[4]

if os.path.exists(img) == False:
    raise ValueError("The specified image dir does not exist!")

if os.path.exists(piv_folder) == False:
    os.makedirs(piv_folder)
    start = 0
else: 
    # this means we have created a folder to save the results already
    # possibly, there are some results in this folder, but not completed
    # try to analyze the folder and determine if it's needed to pick up the job
    print("piv_folder {} exists, analyzing contents".format(piv_folder))
    lr = readdata(piv_folder, "csv")
    if len(lr) > 0:
        print("The folder has {:d} csv files".format(len(lr)))
        last_name = lr.iloc[-1]["Name"]
        # analyze the name
        print("The last csv file has name: {}".format(last_name))
        start = int(last_name.split("-")[0])
        print("Start doing PIV from frame {:d}".format(start))
        if start > len(lr) * 2: # check if there are missing results before
            print("There are files missing, start from beginning.")
            start = 0
    else:
        start = 0 
overlap = winsize // 2

if os.path.isdir(img):
    l = readdata(img, "tif")
    nImages = len(l)
    for ind0, ind1 in zip(l.index[::2], l.index[1::2]):
        show_progress((ind0+2)/nImages, ind0+1)
        I0 = io.imread(l.at[ind0, "Dir"])
        I1 = io.imread(l.at[ind1, "Dir"])
        x, y, u, v = PIV(I0, I1, winsize, overlap, dt)
        pivData = pd.DataFrame({"x": x.flatten(), "y": y.flatten(), "u": u.flatten(), "v": v.flatten()})
        pivData.to_csv(os.path.join(piv_folder, "{0}-{1}.csv".format(l.at[ind0, "Name"], l.at[ind1, "Name"])), index=False)
   
elif img.endswith(".nd2"):
    with ND2Reader(img) as images:
        nImages = images.metadata["num_frames"]
        for i in range(start, nImages, 2):
            show_progress((i+1)/nImages, i+1)
            I0 = images[i]
            I1 = images[i+1]
            x, y, u, v = PIV(I0, I1, winsize, overlap, dt)
            pivData = pd.DataFrame({"x": x.flatten(), "y": y.flatten(), "u": u.flatten(), "v": v.flatten()})
            pivData.to_csv(os.path.join(piv_folder, "{0:05d}-{1:05d}.csv".format(i, i+1)), index=False)

