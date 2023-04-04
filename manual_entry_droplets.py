"""
A simple graphical interface to manually input droplet coords which are not found by the automatic algorithm. The script reads the "tracking.csv" file as the raw trajectory, reindex it with index.min() and index.max(), and display all the missing frames (x, y are NaN) in order. Click on the droplet center and the coords will be recorded. The data will only be saved at the end of the script. 

.. rubric:: Syntax

.. code-block:: console

   python manual_entry_droplets.py analysis_folder nd2Dir radius

* analysis_folder: the folder containing all the tracking analysis related files. Current method involves many steps and files, e.g. ``hough_params.json`` and ``finding.csv``, so I collect all of them in a folder for easy management.
* nd2Dir: directory of the .nd2 raw image file.
* radius: radius of the inner droplet (pixels). This is used to set the circle cursor, which aids the eye during manual tracking. 

.. rubric:: Edit

* Mar 14, 2023 -- Initial commit.
* Apr 03, 2023 -- (i) Implement circle cursor to better position the manual tracking, (ii) save data on the last image and exit, (iii) index should be saved.
"""

import matplotlib.pyplot as plt
import sys
import os
import numpy as np
import pandas as pd
from matplotlib.image import AxesImage
from nd2reader import ND2Reader
from matplotlib.patches import Ellipse
from matplotlib.backend_bases import MouseButton


            


if __name__ == "__main__":

    analysis_folder = sys.argv[1]
    nd2Dir = sys.argv[2]
    radius = float(sys.argv[3])

    t = pd.read_csv(os.path.join(analysis_folder, "tracking.csv"))
    # r = t["r"].mean()
    pos = t.set_index("frame")
    pos = pos.reindex(np.arange(pos.index[0], 1 + pos.index[-1]))
    
    fig, ax = plt.subplots(dpi=200)
    

    missing_frame_index = pos.loc[np.isnan(pos.x)].index
    num_missing = len(missing_frame_index)
    num_total = len(pos)
    
    img_list = []
    with ND2Reader(nd2Dir) as images:
        for index in missing_frame_index:
            img = images[index]
            img_list.append(img)

    h = ax.imshow(img_list[0], cmap="gray")

    class CirclePicker:
        """
        A rectangle editor.

        Click button once to set a center of rotation.
        Click a second time to set the distance from the center and draw the rectangle.
        """

        def __init__(self, ax):
            self.ax = ax
            self.current_frame = 0
            self.coords = []
            canvas = self.ax.figure.canvas

            # self.ax.add_patch(rectpatch)
            self.cursor = Ellipse((100, 100), 2*radius, 2*radius, fill=False, ec="yellow", alpha=0)
            self.ax.add_patch(self.cursor)

            canvas.mpl_connect('draw_event', self.on_draw)
            canvas.mpl_connect("button_press_event", self.on_button_press)
            canvas.mpl_connect("motion_notify_event", self.on_mouse_move)
            canvas.mpl_connect("key_press_event", self.on_key_press)

            self.canvas = canvas
        
        def on_draw(self, event):
            """Callback for draws."""
            self.background = self.canvas.copy_from_bbox(self.ax.bbox)
            
            self.cursor.set_alpha(0.5)
            # self.ax.draw_artist(self.cursor)
            self.canvas.blit(self.ax.bbox)

        def on_button_press(self, event):
            """Callback for mouse button presses."""
            if (event.inaxes is None or 
                event.button != MouseButton.LEFT):
                return
            self.coords.append((event.xdata, event.ydata))
            self.current_frame += 1

            h.set(data=img_list[self.current_frame])
            print("{0:d}/{1:d}".format(self.current_frame, num_missing))
            self.ax.draw_artist(h)
            self.background = self.canvas.copy_from_bbox(self.ax.bbox)
            
            self.canvas.blit(self.ax.bbox)

            if self.current_frame >= num_missing - 1:
                coords = np.stack(self.coords)
                pos.loc[missing_frame_index[:self.current_frame], "x"] = coords[:, 0]
                pos.loc[missing_frame_index[:self.current_frame], "y"] = coords[:, 1]
                pos.to_csv(os.path.join(analysis_folder, "tracking_manual.csv"))
                exit()
            
        def on_mouse_move(self, event):
            """Callback for mouse movements."""
            if (event.inaxes is None):
                return

            self.cursor.set_center((event.xdata, event.ydata))
            
            # reset canvas
            self.canvas.restore_region(self.background)
            # draw
            self.ax.draw_artist(self.cursor)
            self.canvas.blit(self.ax.bbox)

        def on_key_press(self, event):
            """Callback for key presses. Press Enter to save crop data to file."""
            if not event.inaxes:
                return
            if event.key == 'enter':
                coords = np.stack(self.coords)
                pos.loc[missing_frame_index[:self.current_frame], "x"] = coords[:, 0]
                pos.loc[missing_frame_index[:self.current_frame], "y"] = coords[:, 1]
                pos.to_csv(os.path.join(analysis_folder, "tracking_manual.csv"))

    interactor = CirclePicker(ax)
    plt.show()

    # count = 1
    # for index, img in zip(missing_frame_index, img_list):
    #     h.set(data=img)
    #     ax.set_title("{0:d}/{1:d}, {2:d}/{3:d}".format(count, num_missing, index, num_total))
    #     pts = plt.ginput(1, timeout=-1)
    #     pos.loc[index, ["x", "y", "r", "particle"]] = pts[0][0], pts[0][1], r, 0
    #     print(pos.loc[index, ["x", "y", "r", "particle"]])
    #     count += 1
    
    # pos.to_csv(os.path.join(analysis_folder, "tracking.csv"))
