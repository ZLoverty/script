"""
This code is intended for tracking droplets using ``cv2.HoughCircle()`` algorithm. 

.. rubric:: Algorithm

* Run ``cv2.HoughCircle()`` with parameters in ``hough_params.json`` in the analysis_folder
* if number_of_circle_found > 0, then process next image frame
* else if number_of_circle_found == 0, increase ``param1`` (not implemented)
    - if no particle is found after 5 iterations, save x, y as ``np.nan`` and skip

.. rubric:: Syntax

.. code-block::

   python track_droplets.py analysis_folder nd2Dir

* ``analysis_folder`` -- folder to retrieve hough circle parameters ``hough_params.json``, and to save trajectory results
* ``nd2Dir`` -- directory of .nd2 raw image

.. rubric:: Test

.. code-block:: console

   python track_droplets.py test_images\track_droplets test_images\test.nd2 

.. rubric:: Edit

* Jan 05, 2023 -- Adapt myimagelib import style.
* Feb 08, 2023 -- Rewrite in function wrapper form, to make autodoc work properly. (autodoc import the script and execute it, so anything outside ``if __name__=="__main__"`` will be executed, causing problems)
* Mar 09, 2023 -- (i) Use .nd2 as input image, (ii) do not save cropped images, instead generate a report, (iii) I'm trying to generate a real time report using matplotlib, but the performance was an issue. The plot window freezes, and the tracking efficiency decays over time. Therefore, I disable this report system and postpone the development to the future.
* Mar 14, 2023 -- Remove the link step: link trajectories by nature is highly interactive, because one needs to actively check if the cutoff distance is chosen properly so that we don't miss detected particles with the filtering. 
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
import sys
from nd2reader import ND2Reader




def report(traj, hough_params, nd2Dir, num_images, number_of_circles_detected, fig, img):
    # generate report (for a sketch, see https://drive.google.com/open?id=1CrAxG9Wzg-yLUcKtmo7gak8eFOZLUoAw&authuser=liux3141%40umn.edu&usp=drive_fs)
    
    plt.clf()
    subfigs = fig.subfigures(3, 1, height_ratios=[0.2, 0.4, 0.4])

    # - number / total frames where no circles are found
    ax = subfigs[0].subplots()
    ax.annotate("{0:d}/{1:d} droplets found".format(len(traj.dropna()), num_images), \
                (0.5, 0.5), xycoords="axes fraction", fontsize=50,
                verticalalignment="center", horizontalalignment="center")
    ax.axis("off")

    # - distribution of circle radius
    ax = subfigs[1].subplots(1, 2, width_ratios=(3, 7))

    hist, bin_edges = np.histogram(traj["r"], bins=np.linspace(hough_params["minRadius"], hough_params["maxRadius"], 5))
    ax[0].bar(bin_edges[:-1], hist)
    ax[0].set_title("radius distribution")
    
    # - number of circles over time
    ax[1].plot(range(num_images), number_of_circles_detected)
    ax[1].set_title("number of circles detected")

    # - scatter plot
    ax = subfigs[2].subplots(1, 4)

    # - snapshots
    # randomly sample 3 frames and draw
    count = 0
    # for num, i in traj.sample(3).iterrows():
    #     with ND2Reader(nd2Dir) as images:
    #         img = images[i.frame]
    #     ax[count].imshow(img, cmap="gray")
    #     circ = mpatch.Circle((i.x, i.y), i.r, fill=False, color="red")
    #     ax[count].add_patch(circ)
    #     ax[count].set_title("frame {:d}".format(i.frame.astype("int")))
    #     count += 1

    ax[count].imshow(img, cmap="gray")
    ax[count].scatter(traj.x, traj.y, s=1)

    fig.canvas.draw()
    plt.pause(.001)

    return fig
    # fig.savefig(os.path.join(analysis_folder, "tracking_report.pdf"))
    


if __name__ == "__main__":
    # system args

    analysis_folder = sys.argv[1]
    nd2Dir = sys.argv[2]

    test = False

    # load hough circle params from analysis folder

    with open(os.path.join(analysis_folder, "hough_params.json"), "r") as f:
        hough_params = json.load(f)

    # Initial params
    # report_step = 100 # show report window every report_step steps, int
    max_number_of_circles = 3 # maximal number of circles to be detected, if in one frame we detect more circles, only the first number of circles will be recorded.
    number_of_circles_detected = [] # number of circles detected at each frame, used for evaluating the parameter set

    data_list = []

    t0 = time.monotonic()

    # fig = plt.figure(figsize=(16, 9), dpi=72)
    # plt.show(block=False)

    with ND2Reader(nd2Dir) as images:

        num_images = len(images)

        for num, img in enumerate(images):

            # a filter may apply here to suppress noise

            # apply hough circle algorithm to img, with the supplied parameters
            circles = cv2.HoughCircles(to8bit(img), cv2.HOUGH_GRADIENT, **hough_params)

            # save data in a DataFrame
            if circles is not None: # check if any circle is detected
                for circle in circles[0][:max_number_of_circles]:
                    data_item = pd.DataFrame({"x": circle[0],
                                            "y": circle[1],
                                            "r": circle[2],
                                            "frame": num}, index=[0])
                    data_list.append(data_item)

                number_of_circles_detected.append(len(circles[0]))
            else:
                # if no circle is detected, set x, y to NaN
                data_item = pd.DataFrame({"x": np.nan,
                                        "y": np.nan,
                                        "r": np.nan,
                                        "frame": num}, index=[0])
                data_list.append(data_item)
                number_of_circles_detected.append(0)

            t1 = time.monotonic()-t0
            show_progress((num+1)/num_images, label="{:.1f} frame/s".format(num/t1))

            if test == True:
                num_images = 200
                if num >= 199:
                    break
            
            

            # if num % report_step == 0 and num > 0:
            #     report(traj, hough_params, nd2Dir, num+1, number_of_circles_detected, fig, img)

    # link and save traj data in a *.csv file
    traj = pd.concat(data_list, axis=0)
    # linked = tp.link(traj, 20, memory=5)
    # linked1 = tp.filter_stubs(linked, 30)
    traj.to_csv(os.path.join(analysis_folder, 'finding.csv'), index=False)

    