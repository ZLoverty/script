"""
This code is intended for tracking droplets using ``cv2.HoughCircle()`` algorithm. The code is apparently written in a rush, so no formal test has been done. Therefore, do not use it until it's tested.

.. rubric:: Edit

* Jan 05, 2023 -- Adapt myimagelib import style.
* Feb 08, 2023 -- Rewrite in function wrapper form, to make autodoc work properly. (autodoc import the script and execute it, so anything outside ``if __name__=="__main__"`` will be executed, causing problems)
"""

import numpy as np
from skimage import io, filters, draw
import os
import matplotlib.pyplot as plt
import cv2
import matplotlib.patches as mpatch
import pandas as pd
from myimagelib.myImageLib import to8bit, show_progress, bestcolor, gauss1, readdata
import time
import trackpy as tp
import json
from scipy.optimize import curve_fit
from scipy.signal import savgol_filter
import cv2
from scipy.signal import argrelextrema, argrelmin
from scipy.ndimage import gaussian_filter1d
from de_utils import *
import sys



if __name__ == "__main__":
    # system args

    analysis_folder = sys.argv[1]
    img_folder = sys.argv[2]

    # load hough circle params from analysis folder

    with open(os.path.join(analysis_folder, "hough_paramst0.json"), "r") as f:
        hough_paramst0 = json.load(f)
    with open(os.path.join(analysis_folder, "hough_paramst1.json"), "r") as f:
        hough_paramst1 = json.load(f)

    # Initial params
    save_step = 1000 # save detection overlay image every save_step steps, int
    number_of_circles = 3 # number of circles to be detected, the idea is to detect multiple circles and use linking criteria to filter out false detection
    start_frame = 0
    end_frame = None

    l = readdata(img_folder, "tif")
    img_list = l.reset_index()
    num_images = len(img_list)
    data_list = {"t0": [], "t1": []}

    # HoughCircles params
    params = {}
    params["t0"] = hough_paramst0
    params["t1"] = hough_paramst1

    # initialize output folder
    cropped_folder = os.path.join(analysis_folder, 'snapshots')
    if os.path.exists(cropped_folder) == False:
        os.makedirs(cropped_folder)

    t0 = time.monotonic()
    count = 1
    for num, i in img_list.iterrows():
        if num < start_frame:
            continue
        # read image and convert to 8-bit (HoughCircles requires 8-bit images)
        img = to8bit(io.imread(i.Dir))
        # initialize empty dict circles
        circles = {}
        for tname in params:
            circles[tname] = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, **params[tname])
            if circles[tname] is not None: # check if any circle is detected
                for circle in circles[tname][0][:number_of_circles]:
                    data_item = pd.DataFrame({"x": circle[0],
                                            "y": circle[1],
                                            "r": circle[2],
                                            "frame": i.Name}, index=[0])
                    data_list[tname].append(data_item)

            else:
                # if no circle is detected, set x, y to NaN
                # x, y = np.nan, np.nan
                data_item = pd.DataFrame({"x": np.nan,
                                        "y": np.nan,
                                        "r": np.nan,
                                        "frame": int(i.Name)}, index=[0])
                data_list[tname].append(data_item)

        if num % save_step == 0: # save image and detecting result for validating purpose
            fig = plt.figure(figsize=(3, 3))
            ax = fig.add_axes([0,0,1,1])
            ax.imshow(img, cmap='gray')
            for tname in circles:
                if circles[tname] is not None: # check if any circle is detected
                    for circle in circles[tname][0][:number_of_circles]:
                        circle_object = mpatch.Circle((circle[0], circle[1]), circle[2],
                                                fill=False, ec='red', lw=1)
                        ax.add_patch(circle_object)
            fig.savefig(os.path.join(cropped_folder, '{}.jpg'.format(i.Name)))
            plt.close() # prevent figure from showing up inline
        t1 = time.monotonic()-t0
        show_progress((num+1)/num_images, label="{:.1f} frame/s".format(count/t1))
        count += 1

    # save traj data in a *.csv file
    for tname in params:
        data = pd.concat(data_list[tname], axis=0)
        data.to_csv(os.path.join(analysis_folder, 'fulltraj_{}.csv'.format(tname)), index=False)
        linked = tp.link(data, 20, memory=5)
        linked1 = tp.filter_stubs(linked, 500)
        linked1.to_csv(os.path.join(analysis_folder, 'fulltraj_{}l.csv'.format(tname)), index=False)
    # save HoughCircles params in a *.json file for future ref
