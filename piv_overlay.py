import os
import sys
import numpy as np
from myImageLib import to8bit
from skimage import io
import time
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from pivLib import read_piv
from corrLib import readdata

"""
GENERAL
=======
Generate PIV arrow overlayed images for PIV visual inspection and illustration.

USAGE
=====
python piv_overlay.py piv_folder img_folder output_folder sparcity

piv_folder -- folder containing PIV data in the form of .csv files
img_folder -- folder containing .tif images
output_folder -- folder to save the PIV overlay images in .jpg files (rescaled to 360 pixels in width)
sparcity -- density of PIV arrows, higher value corresponds to sparcer arrows

TEST
====
python piv_overlay.py test_images\piv_drop test_images\piv_drop test_images\piv_overlay 1

> generate files 06972.jpg 069740jpg log.txt

LOG
===
piv_folder: test_images\piv_drop
img_folder: test_images\piv_drop
output_folder: test_images\piv_overlay
sparcity: 1
Mon Jan  3 12:31:44 2022 // 06972 calculated
Mon Jan  3 12:31:44 2022 // 06974 calculated

EDIT
====
Jan 03, 2022 -- i) move from PIV to script, ii) set scale, iii) update docstring
                iv) minor structural changes
"""

def determine_arrow_scale(u, v):
    pass # implement in the future

if __name__=="__main__": # whether the following script will be executed when run this code
    pivDataFolder = sys.argv[1]
    imgFolder = sys.argv[2]
    output_folder = sys.argv[3]
    if len(sys.argv) == 5:
        sparcity = int(sys.argv[4])
    else:
        sparcity = 1
    if os.path.exists(output_folder) == False:
        os.makedirs(output_folder)
    with open(os.path.join(output_folder, 'log.txt'), 'w') as f:
        f.write('piv_folder: ' + pivDataFolder + '\n')
        f.write('img_folder: ' + imgFolder + '\n')
        f.write('output_folder: ' + output_folder + '\n')
        f.write('sparcity: ' + str(sparcity) + '\n')

    # pivDataDir = dirrec(pivDataFolder, '*.csv')

    l = readdata(pivDataFolder, "csv")
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
        scale = .5
        w, h = img.shape[1] / dpi, img.shape[0] / dpi
        fig = Figure(figsize=(w*scale, h*scale)) # on some server `plt` is not supported
        canvas = FigureCanvas(fig) # necessary?
        ax = fig.add_axes([0, 0, 1, 1])
        ax.imshow(img, cmap='gray')
        ax.quiver(xs, ys, us, vs, color='yellow', width=0.003, \
                    scale_units="dots", scale=2) # it's better to set a fixed scale
        ax.axis('off')
        # outfolder = folder.replace(pivDataFolder, output_folder) #
        # if os.path.exists(outfolder) == False:
        #     os.makedirs(outfolder)
        fig.savefig(os.path.join(output_folder, imgname + '.jpg'), dpi=dpi)
        with open(os.path.join(output_folder, 'log.txt'), 'a') as f:
            f.write(time.asctime() + ' // ' + imgname + ' calculated\n')
