"""
A simple graphical interface to manually input droplet coords which are not found by the automatic algorithm. The script reads the "tracking.csv" file as the raw trajectory, reindex it with index.min() and index.max(), and display all the missing frames (x, y are NaN) in order. Click on the droplet center and the coords will be recorded. The data will only be saved at the end of the script. 

.. rubric:: Syntax

.. code-block:: console

   python manual_entry_droplets.py analysis_folder nd2Dir

.. rubric:: Edit

* Mar 14, 2023 -- Initial commit.
"""

import matplotlib.pyplot as plt
import sys
import os
import numpy as np
import pandas as pd
from matplotlib.image import AxesImage
from nd2reader import ND2Reader

if __name__ == "__main__":

    analysis_folder = sys.argv[1]
    nd2Dir = sys.argv[2]

    t = pd.read_csv(os.path.join(analysis_folder, "tracking.csv"))
    r = t["r"].mean()
    pos = t.set_index("frame")
    pos = pos.reindex(np.arange(pos.index[0], 1 + pos.index[-1]))
    
    fig, ax = plt.subplots(dpi=300)
    

    missing_frame_index = pos.loc[np.isnan(pos.x)].index
    num_missing = len(missing_frame_index)
    num_total = len(pos)
    
    img_list = []
    with ND2Reader(nd2Dir) as images:
        for index in missing_frame_index:
            img = images[index]
            img_list.append(img)

    h = ax.imshow(img)

    count = 1
    for index, img in zip(missing_frame_index, img_list):
        h.set(data=img)
        ax.set_title("{0:d}/{1:d}, {2:d}/{3:d}".format(count, num_missing, index, num_total))
        pts = plt.ginput(1, timeout=-1)
        pos.loc[index, ["x", "y", "r", "particle"]] = pts[0][0], pts[0][1], r, 0
        print(pos.loc[index, ["x", "y", "r", "particle"]])
        count += 1
    
    pos.to_csv(os.path.join(analysis_folder, "tracking.csv"))
