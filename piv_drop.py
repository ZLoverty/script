from openpiv import tools, pyprocess, validation, filters, scaling
import numpy as np
from skimage import io
import os
from scipy.signal import medfilt2d
import pandas as pd
import sys
from corrLib import readdata
import time

"""
Perform PIV analysis on an image sequence of **bacteria in a droplet**.
Written by Z. L.
Notebook for this script: DE/code/PIV/PIV analysis in droplets

USAGE
=====
python piv_drop.py image_folder save_folder params_file 

image_folder -- folder containing .tif image sequence
save_folder -- folder to save PIV data
params_file -- a text file containing all the required parameters.
               Parameter list:
                   PIV -- winsize, overlap, dt
                   ROI -- x0, y0, w, h
                   circle (mask) -- xc, yc, r
               The file should contain these 10 numbers in order.

TEST PARAMS
===========
image_folder = test_images\piv_drop
save_folder = test_images\piv_drop
params_file = test_images\piv_drop\params.txt

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
"""

def PIV_droplet(I0, I1, ROI, circle, winsize=40, overlap=20, dt=0.02):
    """Perform PIV analysis on the image sequence in given folder. Specific for images of droplets.
    Args:
    I0, I1 -- adjacent images in a sequence
    ROI -- 4-tuple, (x0, y0, w, h)
    circle -- indicate droplet position (wrt raw image upper left corner) and size
    Returns:
    frame_data -- x, y, u, v DataFrame, here x, y is wrt original image, (u, v) are in px/s"""
    # apply ROI
    I0_crop = apply_ROI(I0, *ROI).astype(np.int32)
    I1_crop = apply_ROI(I1, *ROI).astype(np.int32)
    # PIV
    u0, v0, sig2noise = pyprocess.extended_search_area_piv(
        I0_crop.astype(np.int32),
        I1_crop.astype(np.int32),
        window_size=winsize,
        overlap=overlap,
        dt=dt,
        search_area_size=winsize,
        sig2noise_method='peak2peak',
    )
    # get x, y
    x, y = pyprocess.get_coordinates(
        image_size=I0_crop.shape,
        search_area_size=winsize,
        overlap=overlap,
        window_size=winsize
    )
    x0, y0, w, h = ROI
    x, y = x + x0, y + y0
    # generate circle mask
    xc, yc, r = circle
    xcr, ycr = xc-x0, yc-y0
    mask = (x-xc) ** 2 + (y-yc) ** 2 <= (r-winsize) ** 2
    # apply mask to velocities and coordinates

#     xm = x * mask
#     ym = y * mask
    # signal to noise validation
    u1, v1, mask_s2n = validation.sig2noise_val(
        u0, v0,
        sig2noise,
        threshold = 1.05,
    )
    # replace_outliers
    u2, v2 = filters.replace_outliers(
        u1, v1,
        method='localmean',
        max_iter=3,
        kernel_size=3,
    )
    # median filter smoothing
    u3 = medfilt2d(u2, 3)
    v3 = medfilt2d(v2, 3)
    u3[~mask] = np.nan
    v3[~mask] = np.nan
    # generate DataFrame data
    frame_data = pd.DataFrame(
        data=np.array([x.flatten(), y.flatten(), u3.flatten(), v3.flatten()]).T, 
        columns=['x', 'y', 'u', 'v'])
    return frame_data

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
    params_file = sys.argv[3]
    
    winsize, overlap, dt, ROI, circle = read_params(params_file)
    
    if os.path.exists(save_folder) == 0:
        os.makedirs(save_folder)
    with open(os.path.join(save_folder, 'log.txt'), 'w') as f:
        f.write('Params\n')
        f.write('winsize: ' + str(winsize) + '\n')
        f.write('overlap: ' + str(overlap) + '\n')
        f.write('dt: ' + str(dt) + '\n')
        f.write('ROI: ' + str(ROI) + '\n')
        f.write('circle: ' + str(circle) + '\n')
    
    l = readdata(image_folder, 'tif')
    
    k = 0 # serve as a flag for I0 and I1

    for num, i in l.iterrows():
        if k % 2 == 0:
            I0 = io.imread(i.Dir)
            n0 = i.Name
            k += 1
        else:
            I1 = io.imread(i.Dir)
            k += 1
            frame_data = PIV_droplet(I0, I1, ROI, circle, winsize, overlap, (int(i.Name)-int(n0))*dt)
            frame_data.to_csv(os.path.join(save_folder, n0 + '-' + i.Name+'.csv'), index=False)
            with open(os.path.join(save_folder, 'log.txt'), 'a') as f:
                f.write(time.asctime() + ' // ' + n0 + '-' + i.Name + ' calculated\n')