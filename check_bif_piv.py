"""
A slider bar application for checking bifurcation PIV data. The PIV results in 3 channels will be displayed in the same window with the same scale. A slider makes it easy to go through all the frames. 

.. rubric:: Edit

* Mar 16, 2023 -- Initial commit.
* Apr 28, 2023 -- Wrap in ``__name__=="__main__"``.
"""

# Import libraries using import keyword
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from skimage import io
from scipy.io import loadmat
import os

if __name__=="__main__":
    # date and number of experiment
    folder = "/mnt/SYMMETRIC/19 jan 2023/"
    number = 1
    img_folder = os.path.join(folder, "nd2", "crop_channel")
    piv_folder = os.path.join(folder,  "PIV")
    # Load image and PIV data

    img1 = io.imread(os.path.join(img_folder, "{:02d}_A.tif".format(number)))
    img2 = io.imread(os.path.join(img_folder, "{:02d}_B.tif".format(number)))
    img3 = io.imread(os.path.join(img_folder, "{:02d}_C.tif".format(number)))

    cpiv_dict = loadmat(os.path.join(piv_folder, "{:02d}_A.mat".format(number)))
    x1, y1, U1, V1, mask1 = cpiv_dict["x"], cpiv_dict["y"], cpiv_dict["u"], cpiv_dict["v"], cpiv_dict["mask"]
    U1[:, ~(mask1>mask1.mean())] = np.nan
    V1[:, ~(mask1>mask1.mean())] = np.nan 
    cpiv_dict = loadmat(os.path.join(piv_folder, "{:02d}_B.mat".format(number)))
    x2, y2, U2, V2, mask2 = cpiv_dict["x"], cpiv_dict["y"], cpiv_dict["u"], cpiv_dict["v"], cpiv_dict["mask"]
    U2[:, ~(mask2>mask2.mean())] = np.nan
    V2[:, ~(mask2>mask2.mean())] = np.nan 
    cpiv_dict = loadmat(os.path.join(piv_folder, "{:02d}_C.mat".format(number)))
    x3, y3, U3, V3, mask3 = cpiv_dict["x"], cpiv_dict["y"], cpiv_dict["u"], cpiv_dict["v"], cpiv_dict["mask"]
    U3[:, ~(mask3>mask3.mean())] = np.nan
    V3[:, ~(mask3>mask3.mean())] = np.nan 
    # Setting Plot and Axis variables as subplots()
    # function returns tuple(fig, ax)
    fig, ax = plt.subplots(1, 3)
    
    # Adjust the bottom size according to the
    # requirement of the user
    plt.subplots_adjust(bottom=0.25)


    # plot the quiver
    scale = max(np.nanmax(U1), np.nanmax(V1)) * U1.shape[2] / 5
    l1 = ax[0].imshow(img1[0], cmap="gray")
    q1 = ax[0].quiver(x1, y1, U1[0], -V1[0], color="yellow", scale=scale, scale_units="width")
    l2 = ax[1].imshow(img2[0], cmap="gray")
    q2 = ax[1].quiver(x2, y2, U2[0], -V2[0], color="yellow", scale=scale, scale_units="width")
    l3 = ax[2].imshow(img3[0], cmap="gray")
    q3 = ax[2].quiver(x3, y3, U3[0], -V3[0], color="yellow", scale=scale, scale_units="width")
    # Choose the Slider color
    slider_color = 'White'
    
    # Set the axis and slider position in the plot
    axis_position = plt.axes([0.2, 0.1, 0.65, 0.03],
                            facecolor = slider_color)
    simg = Slider(axis_position, 'frame', 0, len(img1)-1, valinit=0, valstep=1, color="green")
    
    # update() function to change the graph when the
    # slider is in use
    def update(val):
        pos = simg.val
        ax[0].set_title("{:.1f}".format(np.nanmean(-V1[pos])))
        l1.set(data=img1[pos])
        q1.set_UVC(U1[pos], -V1[pos])
        ax[1].set_title("{:.1f}".format(np.nanmean(-V2[pos])))
        l2.set(data=img2[pos])
        q2.set_UVC(U2[pos], -V2[pos])
        ax[2].set_title("{:.1f}".format(np.nanmean(-V3[pos])))
        l3.set(data=img3[pos])
        q3.set_UVC(U3[pos], -V3[pos])
        fig.canvas.draw_idle()
    
    # update function called using on_changed() function
    simg.on_changed(update)
    
    # Display the plot
    plt.show()
