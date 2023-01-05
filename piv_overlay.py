import os
import sys
import numpy as np
from myimagelib.myImageLib import to8bit, readdata
from skimage import io
import time
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from myimagelib.pivLib import read_piv
from myimagelib.deLib import droplet_image

"""
piv_overlay
===========

Generate PIV arrow overlayed images for PIV visual inspection and illustration.

.. rubric:: Syntax

.. code-block:: console

   python piv_overlay.py piv_folder img_folder output_folder sparcity

* piv_folder -- folder containing PIV data in the form of .csv files
* img_folder -- folder containing .tif images
* output_folder -- folder to save the PIV overlay images in .jpg files (rescaled to 360 pixels in width)
* sparcity -- density of PIV arrows, higher value corresponds to sparcer arrows

.. rubric:: Test

.. code-block:: console

   python piv_overlay.py test_images\piv_drop test_images\piv_drop test_images\piv_overlay 1

.. rubric:: Edit

* Jan 03, 2022 --
    1. move from PIV to script,
    2. set scale,
    3. update docstring
    4. minor structural changes

    .. note::
       See `PIV technical report Sec II.A.1 <https://github.com/ZLoverty/DE/blob/main/Notes/PIV_technical_report.pdf>`_ for the reasoning of scale settings.

* Jan 22, 2022 -- reduce scale by 1.5 to increase the arrow size
* Mar 03, 2022 --
    1. Use `droplet_image` class to rewrite the script,
    2. remove logging
* Jan 05, 2023 -- Adapt myimagelib import style.
"""

def determine_arrow_scale(u, v, sparcity):
    row, col = u.shape
    return max(np.nanmax(u), np.nanmax(v)) * col / sparcity / 1.5

if __name__=="__main__": # whether the following script will be executed when run this code
    piv_folder = sys.argv[1]
    image_folder = sys.argv[2]
    out_folder = sys.argv[3]
    sparcity = 1
    if len(sys.argv) > 4:
        sparcity = int(sys.argv[4])

    if os.path.exists(out_folder) == False:
        os.makedirs(out_folder)

    seq = readdata(image_folder, "tif")
    DI = droplet_image(seq)

    DI.piv_overlay_fixed(piv_folder, out_folder, sparcity=sparcity)

    """
    l = readdata(pivDataFolder, "csv")

    # compute scale factor of quiver
    x, y, u, v = read_piv(l.Dir[0])
    row, col = x.shape
    scale = determine_arrow_scale(u, v, sparcity)

    for num, i in l.iterrows():
        # PIV data
        folder, pivname = os.path.split(i.Dir)
        x, y, u, v = read_piv(i.Dir)
        row, col = x.shape
        xs = x[0:row:sparcity, 0:col:sparcity]
        ys = y[0:row:sparcity, 0:col:sparcity]
        us = u[0:row:sparcity, 0:col:sparcity]
        vs = v[0:row:sparcity, 0:col:sparcity]
        # overlay image
        imgname = i.Name.split("-")[0]
        imgDir = os.path.join(imgFolder, imgname + '.tif')
        img = to8bit(io.imread(imgDir))
        # bp = bpass(img, 2, 100)
        # fig = plt.figure(figsize=(3, 3*row/col))
        dpi = 300
        figscale = 1
        w, h = img.shape[1] / dpi, img.shape[0] / dpi
        fig = Figure(figsize=(w*figscale, h*figscale)) # on some server `plt` is not supported
        canvas = FigureCanvas(fig) # necessary?
        ax = fig.add_axes([0, 0, 1, 1])
        ax.imshow(img, cmap='gray')
        ax.quiver(xs, ys, us, vs, color='yellow', width=0.003, \
                    scale=scale, scale_units='width') # it's better to set a fixed scale, see *Analysis of Collective Motions in Droplets* Section IV.A.2 for more info.
        ax.axis('off')
        # outfolder = folder.replace(pivDataFolder, output_folder) #
        # if os.path.exists(outfolder) == False:
        #     os.makedirs(outfolder)
        fig.savefig(os.path.join(output_folder, imgname + '.jpg'), dpi=dpi)
        with open(os.path.join(output_folder, 'log.txt'), 'a') as f:
            f.write(time.asctime() + ' // ' + imgname + ' calculated\n')
    """
