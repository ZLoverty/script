import matplotlib.pyplot as plt
from skimage import io
from matplotlib.backend_bases import MouseButton
from matplotlib.patches import Rectangle
import numpy as np
import os
import pandas as pd
from scipy.ndimage import map_coordinates
from tifffile import imwrite
from myimagelib.myImageLib import to8bit

### Required settings below

imgDir = r"A:\SYMMETRIC\28 feb 2023\nd2\06.nd2"

save_folder = r"A:\SYMMETRIC\28 feb 2023"

suffix = 2

angles = [0, 120, 240]

w, h = 400, 500

### Settings above

if imgDir.endswith(".nd2"):
    from nd2reader import ND2Reader
    with ND2Reader(imgDir) as images:
        img = images[0]
elif imgDir.endswith(".tif"):
    img = io.imread(imgDir)
    if len(img.shape) == 3:
        img = img[0]

colors = plt.get_cmap("tab10")

fig, ax = plt.subplots()

ax.imshow(to8bit(img), cmap="gray")

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
        self.lines, self.rects = {}, {}
        self.xy, self.angles = {}, {} # rectangle base points
        self.numChannels = len(angles)
        for i in range(self.numChannels):
            self.lines[i], = self.ax.plot([0, 0], [0, 0], color=colors(i), animated=True)
            self.rects[i] = Rectangle((0, 0), 0, 0, fill=False, color=colors(i), ls="--")
            self.ax.add_patch(self.rects[i])

        canvas.mpl_connect('draw_event', self.on_draw)
        canvas.mpl_connect("button_press_event", self.on_button_press)
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
            event.button != MouseButton.LEFT):
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

            dfxy = pd.DataFrame(np.stack([self.xy[i] for i in self.xy]), columns=["BX", "BY"], index=range(self.numChannels))
            dfhu = pd.DataFrame(np.stack([self.h_unit[i] for i in self.h_unit]), columns=["hu0", "hu1"], index=range(self.numChannels))
            dfwu = pd.DataFrame(np.stack([self.w_unit[i] for i in self.w_unit]), columns=["wu0", "wu1"], index=range(self.numChannels))
            df = dfxy.join(dfhu).join(dfwu).assign(h=h, w=w)
            df.to_csv(os.path.join(save_folder, "crop_data{}.csv".format(suffix)))
            fig.savefig(os.path.join(save_folder, "crop{}.jpg".format(suffix)))
            for i in self.xy:
                YY, XX = np.mgrid[0:h, 0:w]
                YY = np.flip(YY, axis=0)
                X = self.xy[i][0] + XX * self.w_unit[i][0] + YY * self.h_unit[i][0]
                Y = self.xy[i][1] + XX * self.w_unit[i][1] + YY * self.h_unit[i][1]
                crop = map_coordinates(img, [Y, X], order=0, mode="constant")
                imwrite(os.path.join(save_folder, "{0}{1}.tif".format(chr(65+i), suffix)), to8bit(crop))

interactor = RectInteractor(ax)
plt.show()