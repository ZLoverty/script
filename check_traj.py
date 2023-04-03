"""
Check trajectory data by plotting on top of raw images. Use scroll wheel to go back and forward. Display particle number in the data. 

.. rubric:: Syntax

.. code-block:: console

   python check_traj.py nd2Dir trajDir radius

* nd2Dir: directory of the .nd2 raw image file.
* trajDir: directory of trajectory data file.
* radius: radius of the inner droplet (pixels). This is used to set the circle position indicator. 

.. rubric:: Edit

* Apr 03, 2023 -- Initial commit.
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

class TrajViewer:
    """
    A trajectory viewer.

    Use scroll wheel to go back and forth.
    """

    def __init__(self, img_list, traj_data, radius):

        self.fig, self.ax = plt.subplots()
        self.data = traj_data

        self.frame_indices = self.data.frame.drop_duplicates().to_list()
        self.current_frame = 0
        self.img_list = img_list
        self.max_frame = len(self.frame_indices) - 1

        self.hsca, = self.ax.plot(t.x, t.y, marker="o", ls="", animated=True)
        self.himg = self.ax.imshow(img_list[0], cmap="gray")
        # self.coords = []
        canvas = self.ax.figure.canvas

        # self.ax.add_patch(rectpatch)
        self.cursor = Ellipse((100, 100), 2*radius, 2*radius, fill=False, ec="yellow", alpha=0.5)
        self.ax.add_patch(self.cursor)

        canvas.mpl_connect('draw_event', self.on_draw)
        canvas.mpl_connect("scroll_event", self.on_scroll)
        canvas.mpl_connect("motion_notify_event", self.on_mouse_move)
        canvas.mpl_connect("button_press_event", self.on_button_press)
        # canvas.mpl_connect("key_press_event", self.on_key_press)

        self.canvas = canvas
        

    def on_scroll(self, event):
        """Go to previous or next image."""
        if event.button == "up" and self.current_frame > 0:
            self.current_frame -= 1
        elif event.button == "down" and self.current_frame < self.max_frame:
            self.current_frame += 1
        else:
            return
        print(self.current_frame)
        self.display()

    def display(self):
        """Display image and data"""
        self.himg.set(data=img_list[self.current_frame])
        self.ax.draw_artist(self.himg)
        t = self.data.loc[self.data.frame == self.frame_indices[self.current_frame]]
        self.hsca.set_xdata(t.x)
        self.hsca.set_ydata(t.y)
        self.ax.draw_artist(self.hsca)
        for num, i in t.iterrows():
            a = self.ax.annotate(i.particle, (i.x, i.y))
            self.ax.draw_artist(a)
        self.canvas.blit(self.ax.bbox)
        self.background = self.canvas.copy_from_bbox(self.ax.bbox)

    def on_draw(self, event):
        """Callback for draws."""
        self.background = self.canvas.copy_from_bbox(self.ax.bbox)

    def on_button_press(self, event):
        """Callback for mouse button presses."""
        self.current_frame += 1
        self.display()

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
            pos.to_csv(os.path.join(analysis_folder, "tracking_manual.csv"), index=False)

if __name__ == "__main__":

    
    nd2Dir = sys.argv[1]
    trajDir = sys.argv[2]
    radius = float(sys.argv[3])

    t = pd.read_csv(trajDir)
    img_list = []
    with ND2Reader(nd2Dir) as images:
        for i in t.frame.drop_duplicates():
            img_list.append(images[i])
        
    

    interactor = TrajViewer(img_list, t, radius)
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
