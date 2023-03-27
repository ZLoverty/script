import matplotlib.pyplot as plt
from skimage import io
from matplotlib.backend_bases import MouseButton
from matplotlib.patches import Rectangle
import numpy as np
import os
import pandas as pd

### Required settings below

imgDir = r"test_images\faster_cropping\crop-test.tif"

save_folder = r"test_images\faster_cropping"

angles = [0, 120, 240]

w, h = 400, 500

### Settings above

img = io.imread(imgDir)

colors = plt.get_cmap("tab10")

fig, ax = plt.subplots()

ax.imshow(img, cmap="gray")

# patch = Rectangle((0, 0), 500, 300, fill=False, lw=5)

# ax.add_patch(patch)

class RectInteractor:
    """
    A rectangle editor.

    Click button once to set a center of rotation.
    Click a second time to set the distance from the center and draw the rectangle.
    """
    epsilon = 5

    def __init__(self, ax):
        self.ax = ax
        canvas = self.ax.figure.canvas

        # self.ax.add_patch(rectpatch)
        self.status = 0
        self.lines, self.rects = {}, {}
        self.xy, self.angles = {}, {} # rectangle base points
        self.numChannels = len(angles)
        for i in range(self.numChannels):
            self.lines[i], = self.ax.plot([0, 0], [0, 0], color=colors(i), animated=True)
            self.rects[i] = Rectangle((0, 0), 0, 0, fill=False, color=colors(i), ls="--")
            self.ax.add_patch(self.rects[i])

        canvas.mpl_connect('draw_event', self.on_draw)
        canvas.mpl_connect("button_press_event", self.on_button_press)
        canvas.mpl_connect("button_release_event", self.on_button_release)
        canvas.mpl_connect("motion_notify_event", self.on_mouse_move)
        canvas.mpl_connect("key_press_event", self.on_key_press)

        self.canvas = canvas
    
    def on_draw(self, event):
        """Callback for draws."""
        self.background = self.canvas.copy_from_bbox(self.ax.bbox)
        for i in range(self.numChannels):
            self.ax.draw_artist(self.rects[i])
            self.ax.draw_artist(self.lines[i])
        self.canvas.blit(self.ax.bbox)

    def on_button_press(self, event):
        """Callback for mouse button presses."""
        if (event.inaxes is None or 
            event.button != MouseButton.LEFT or 
            self.status != 0):
            return
        self.xc = np.array((event.xdata, event.ydata))

    def rotation_matrix(self, angle):
        theta = angle / 180 * np.pi
        return np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])

    def on_mouse_move(self, event):
        """Callback for mouse movements."""
        if (event.inaxes is None or
            event.button != MouseButton.LEFT):
            return
        
        # compute channel A direction

        x = np.array((event.xdata, event.ydata))
        length = ((self.xc - x) ** 2).sum() ** 0.5
        angle = np.arctan2((self.xc[1] - x[1]), (self.xc[0] - x[0])) / np.pi * 180 + 90

        self.h_unit, self.w_unit = {}, {}

        for i in range(self.numChannels):
            # unit vectors of each rectangle in height and width direction
            self.angles[i] = angle + angles[i]
            self.h_unit[i] = np.array((-np.sin(self.angles[i]/180*np.pi), np.cos(self.angles[i]/180*np.pi)))
            self.w_unit[i] = np.array((np.cos(self.angles[i]/180*np.pi), np.sin(self.angles[i]/180*np.pi)))
            # set lines
            self.lines[i].set_data([self.xc[0], self.xc[0]+length*self.h_unit[i][0]], [self.xc[1], self.xc[1]+length*self.h_unit[i][1]])
            # compute rectangle base points
            self.xy[i] = self.xc - w/2*self.w_unit[i] + w/4*self.h_unit[i]
            # set rectangles
            self.rects[i].set(xy=self.xy[i], angle=self.angles[i], width=w, height=h)

        # reset canvas
        self.canvas.restore_region(self.background)
        # draw
        for i in range(self.numChannels):
            self.ax.draw_artist(self.rects[i])
            self.ax.draw_artist(self.lines[i])
        self.canvas.blit(self.ax.bbox)

    def on_key_press(self, event):
        """Callback for key presses. Press Enter to save crop data to file."""
        if not event.inaxes:
            return
        if event.key == 'enter':
            if not os.path.exists(save_folder):
                os.makedirs(save_folder)
            
            # image center, for rotating base points
            # this is to mimic the manual cropping in ImageJ
            xc = np.array((img.shape[1]//2, img.shape[0]//2))
            # the saved base points should be the diagonally opposite vertices
            xy = {}
            for i in range(self.numChannels):
                xy[i] = self.xy[i] + self.h_unit[i] * h + self.w_unit[i] * w
                xy[i] = np.matmul(self.rotation_matrix(180-self.angles[i]), xy[i] - xc) + xc 

            print(self.xy[0])
            print(self.h_unit[0])
            print(self.w_unit[0])
            
            df1 = pd.DataFrame(np.stack([xy[i] for i in xy]), columns=["BX", "BY"], index=[1,3,5]).assign(Width=w, Height=h).astype("int")
            df2 = pd.DataFrame(270-np.array([self.angles[i] for i in self.angles]), columns=["Angle"], index=[0,2,4])
            pd.concat([df1, df2]).sort_index().to_csv(os.path.join(save_folder, "crop_data_test.csv"))

    def on_button_release(self, event):
        """Callback for mouse button releases."""
        if (event.button != MouseButton.LEFT):
            return
        if self.status == 2:
            self.status = 0

interactor = RectInteractor(ax)
# ax.set_xlim([-10, 10])
# ax.set_ylim([-10, 10])
plt.show()