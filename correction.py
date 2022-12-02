import numpy as np
from skimage import io, filters, draw
import os
import matplotlib.pyplot as plt
import cv2
import matplotlib.patches as mpatch
from corrLib import readdata
import pandas as pd
from myImageLib import to8bit, show_progress, bestcolor, gauss1
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

"""
correction
==========

Subpixel correction of droplet trajectory data, based on cross-boundary fitting and circle fitting.

Edit:
Jul 05, 2022 -- If corrected_quality < 0.5, repeat the correction process once.
                This can effectively correct trackings that are very far off.
"""

analysis_folder = sys.argv[1]
img_folder = sys.argv[2]

save_step = 1000
snapshot_folder = os.path.join(analysis_folder, "correction-snapshots")
if os.path.exists(snapshot_folder) == False:
    os.makedirs(snapshot_folder)

correction_params = {}
with open(os.path.join(analysis_folder, "correction_paramst0c.json"), "r") as f:
    correction_params["t0"] = json.load(f)
with open(os.path.join(analysis_folder, "correction_paramst1c.json"), "r") as f:
    correction_params["t1"] = json.load(f)

for tname in correction_params:
    original_traj = pd.read_csv(os.path.join(analysis_folder,
                                             "fulltraj_{}l.csv".format(tname))).set_index("frame")
    circle_list = []
    n_frames = original_traj.index.max()
    count = 0
    t0 = time.monotonic()
    for num, i in original_traj.iterrows():
        original_circle = {"x": i.x, "y": i.y, "r": i.r}
        raw_img = io.imread(os.path.join(img_folder, "{:05d}.tif".format(num)))
        corrected_circle = subpixel_correction(original_circle, raw_img, **correction_params[tname])
        original_quality = circle_quality_std(raw_img, original_circle)
        corrected_quality = circle_quality_std(raw_img, corrected_circle)
        if corrected_quality < 0.5:
            corrected_circle = subpixel_correction(corrected_circle, raw_img, **correction_params[tname])
            corrected_quality = circle_quality_std(raw_img, corrected_circle)
        corrected_circle["frame"] = num
        corrected_circle["original_quality"] = original_quality
        corrected_circle["corrected_quality"] = corrected_quality
        circle_list.append(pd.DataFrame(corrected_circle, index=[num]))
        if num % save_step == 0:
            fig = plt.figure(figsize=(3,3), dpi=100)
            ax = fig.add_axes([0,0,1,1])
            ax.imshow(raw_img, cmap="gray")
            cobj = mpatch.Circle((original_circle["x"], original_circle["y"]), original_circle["r"], fill=False, ec="red", lw=1)
            ax.add_patch(cobj)
            ccor = mpatch.Circle((corrected_circle["x"], corrected_circle["y"]), corrected_circle["r"], fill=False, ec="green", lw=1)
            ax.add_patch(ccor)
            ax.set_xlim([int(original_circle["x"]-original_circle["r"]-10), int(original_circle["x"]+original_circle["r"]+10)])
            ax.set_ylim([int(original_circle["y"]-original_circle["r"]-10), int(original_circle["y"]+original_circle["r"]+10)])
            ax.annotate(num, (0.5, 0.5), xycoords="axes fraction")
            fig.savefig(os.path.join(snapshot_folder, "{:05d}.jpg".format(num)))
            plt.close(fig)
        t1 = time.monotonic() - t0
        show_progress(num / n_frames, label="{:.1f} frames/s".format(num / t1))
    corrected_traj = pd.concat(circle_list)
    corrected_traj.to_csv(os.path.join(analysis_folder, "fulltraj_{}lc.csv".format(tname)))
