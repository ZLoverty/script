"""
Subpixel correction of droplet trajectory data, based on cross-boundary fitting and circle fitting.

.. rubric:: Algorithm
* if original_circle_quality < 0.5 and corrected_circle_quality > original_circle_quality then
* use corrected circle
.. rubric:: Edit

* Jul 05, 2022 -- If corrected_quality < 0.5, repeat the correction process once. This can effectively correct trackings that are very far off.
* Jan 05, 2023 -- Adapt myimagelib import style.
* Feb 08, 2023 -- Rewrite in function wrapper form, to make autodoc work properly. (autodoc import the script and execute it, so anything outside ``if __name__=="__main__"`` will be executed, causing problems)
* Mar 13, 2023 -- (i) Adapt to nd2 images, (ii) apply only on inner trajectory, instead of on both inner and outer. It turns out that the outer trjectory can add more noise to the inner trajectory. 
"""

if __name__ == "__main__":
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
    from myimagelib.deLib import subpixel_correction, circle_quality_std
    import sys
    from nd2reader import ND2Reader


    analysis_folder = sys.argv[1]
    nd2Dir = sys.argv[2]

    with open(os.path.join(analysis_folder, "correction_params.json"), "r") as f:
        correction_params = json.load(f)

    save_step = 1000
    snapshot_folder = os.path.join(analysis_folder, "correction-snapshots")
    if os.path.exists(snapshot_folder) == False:
        os.makedirs(snapshot_folder)

    original_traj = pd.read_csv(os.path.join(analysis_folder,
                                            "tracking.csv")).set_index("frame")
    circle_list = []
    n_frames = original_traj.index.max()
    count = 0
    t0 = time.monotonic()

    with ND2Reader(nd2Dir) as images:
        for num, i in original_traj.iterrows():
            original_circle = {"x": i.x, "y": i.y, "r": i.r}
            raw_img = images[num]
            corrected_circle = subpixel_correction(original_circle, raw_img, **correction_params)
            original_quality = circle_quality_std(raw_img, original_circle)
            corrected_quality = circle_quality_std(raw_img, corrected_circle)

            # if corrected_quality < 0.5:
            #     corrected_circle = subpixel_correction(corrected_circle, raw_img, **correction_params[tname])
            #     corrected_quality = circle_quality_std(raw_img, corrected_circle)

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
        corrected_traj.to_csv(os.path.join(analysis_folder, "corrected_tracking.csv"))
