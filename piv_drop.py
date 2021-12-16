# from openpiv import tools, pyprocess, validation, filters, scaling
from pivLib import PIV_masked
import numpy as np
from skimage import io
import os
# from scipy.signal import medfilt2d
import pandas as pd
import sys
from corrLib import readdata
import time
from multiprocessing import Pool
from itertools import repeat

"""
Perform PIV analysis on an image sequence of **bacteria in a droplet**.
Written by Z. L.
Notebook for this script: DE/code/PIV/PIV analysis in droplets

USAGE
=====
python piv_drop.py image_folder save_folder winsize overlap dt mask_dir

image_folder -- folder containing .tif image sequence
save_folder -- folder to save PIV data
winsize, overlap, dt -- regular params
mask_dir -- mask image dir

TEST PARAMS
===========
python piv_drop.py test_images\piv_drop test_images\piv_drop 40 20 0.02 test_images\piv_drop\mask.tif

LOG
===
Params
winsize: 40
overlap: 20
dt: 0.02
ROI: [132   8 691 805]
circle: [416. 417. 395.]
Thu Dec  9 23:18:14 2021 // 06972-06973 calculated
Thu Dec  9 23:18:16 2021 // 06974-06975 calculated

EDIT
====
12092021 -- Initial commit.
Dec 16, 2021 -- i) use `PIV_masked()` as the core algorithm, ii) implement multiprocessing with `Pool`
"""

def PIV_droplet(I0dir, I1dir, I0name, I1name, winsize, overlap, dt, mask, save_folder):
    """Perform PIV analysis on the image sequence in given folder. Specific for images of droplets.
    Args:
    I0, I1 -- adjacent images in a sequence
    winsize, overlap, dt -- regular PIV params
    mask -- a binary image of the same size as I0 and I1
    Returns:
    None"""
    # apply ROI
    I0 = io.imread(I0dir)
    I1 = io.imread(I1dir)
    x, y, u, v = PIV_masked(I0, I1, winsize, overlap, dt, mask)
    frame_data = pd.DataFrame({"x": x.flatten(), "y": y.flatten(), "u": u.flatten(), "v": v.flatten()})
    frame_data.to_csv(os.path.join(save_folder, "{0}-{1}.csv".format(I0name, I1name)), index=False)

# deprecated
def read_params(params_file):
    """Read piv_drop parameters from params_file.
    params_file template:
        winsize, overlap, dt,
        x0, y0, w, h,
        xc, yc, r
    """
    with open(params_file, 'r') as f:
        a = f.read()
    params = np.char.strip(np.array(a.split(','))).astype('float')
    assert(len(params)==10)
    return params[0].astype('int'), params[1].astype('int'), params[2], \
        params[3:7].astype('int'), params[7:]

def apply_ROI(img, x0, y0, w, h):
    """Apply ROI to the input image
    Args:
    img -- input image, an numpy.array
    x0, y0, w, h -- upper left corner coords, width and height of ROI
    Returns:
    cropped -- image within the ROI, cropped image
    Test:
    x0, y0 = 132, 8
    w, h = 691, 805
    test_img = io.imread(os.path.join('test_images', 'bf_images', '06972.tif'))
    test_img_cropped = apply_ROI(test_img, x0, y0, w, h)
    fig, ax = plt.subplots(nrows=1, ncols=2)
    ax[0].imshow(test_img)
    ax[1].imshow(test_img_cropped)"""
    return img[y0:y0+h, x0:x0+w]

if __name__=="__main__":
    image_folder = sys.argv[1]
    save_folder = sys.argv[2]
    winsize = int(sys.argv[3])
    overlap = int(sys.argv[4])
    dt = float(sys.argv[5])
    mask = io.imread(sys.argv[6])

    if os.path.exists(save_folder) == 0:
        os.makedirs(save_folder)
    with open(os.path.join(save_folder, 'log.txt'), 'w') as f:
        f.write('Params\n')
        f.write('winsize: ' + str(winsize) + '\n')
        f.write('overlap: ' + str(overlap) + '\n')
        f.write('dt: ' + str(dt) + '\n')

    l = readdata(image_folder, 'tif')

    l = l.loc[l.Name!="mask"]
    if len(l) % 2 != 0:
        l = l[:-1]

    with Pool(10) as p:
        p.starmap(PIV_droplet,
                zip(l[::2].Dir, l[1::2].Dir, l[::2].Name, l[1::2].Name, repeat(winsize), repeat(overlap),
                repeat(dt), repeat(mask), repeat(save_folder)))

    # k = 0 # serve as a flag for I0 and I1
    #
    # for num, i in l.iterrows():
    #     if k % 2 == 0:
    #         I0 = io.imread(i.Dir)
    #         n0 = i.Name
    #         k += 1
    #     else:
    #         I1 = io.imread(i.Dir)
    #         k += 1
    #         frame_data = PIV_droplet(I0, I1, ROI, circle, winsize, overlap, (int(i.Name)-int(n0))*dt)
    #         frame_data.to_csv(os.path.join(save_folder, n0 + '-' + i.Name+'.csv'), index=False)
    #         with open(os.path.join(save_folder, 'log.txt'), 'a') as f:
    #             f.write(time.asctime() + ' // ' + n0 + '-' + i.Name + ' calculated\n')
