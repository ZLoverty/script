import os
import numpy as np
from matplotlib import pyplot as plt
from skimage import io
import sys
import time
from myImageLib import to8bit
import shutil

"""
GENERAL
=======
This script is implemented to enable batch converting .raw to .tif image sequences.
It should only be used with the .raw image files generated by the tracking software (LabView) in the Clement Group at PMMH-ESPCI.
Detailed explanation of the .raw file structure can be found in extractImages.ipynb.

Written by Z. L.
Jul 16, 2021

The file structure:
folder
|- RawImage.raw
|- RawImageInfo.txt
|- ...

SYNTAX
======
python extractImages.py folder

folder -- the folder containing the .raw file

TEST
====
python extractImages.py test_images/extractImages

run in the folder of extractImages.py, produce two folders "raw" and "8-bit" under the target folder and save extracted images.

SAMPLE LOG
==========
Start to convert Documents\Github\script\test_images\extractImages\RawImage.raw to 8-bit tif images.
Sat Dec 11 22:07:17 2021 // frame 00000

EDIT
====
Aug 18, 2021 -- Generate log file, recording the total frames of .raw.
                This is to check if the image extraction is complete.
Nov 30, 2021 -- Follow the change of to_tif.py, we make two changes here:
                i) export both raw images and 8-bit saturated images
                ii) check disk capacity before extracting
                NOTE: in the future these two script should be combined
                iii) in addition, the image names start from 0
Dec 11, 2021 -- i) More detailed log file in both 8-bit and raw folders
                ii) Reorganize doc string.
"""

def check_necessary_files(folder):
    """ Check for necessary files
    Check for RawImage.raw, RawImageInfo.txt (height, width, fps ...)

    Test:
    info_file = os.path.join(folder, 'RawImageInfo.txt')
    read_raw_image_info(info_file)
    """
    return os.path.exists(os.path.join(folder, 'RawImage.raw')) and \
            os.path.exists(os.path.join(folder, 'RawImageInfo.txt'))

def read_raw_image_info(info_file):
    """
    Read image info, such as fps and image dimensions, from RawImageInfo.txt
    """
    with open(info_file, 'r') as f:
        a = f.read()
    fps, h, w = a.split('\n')[0:3]
    return int(fps), int(h), int(w)

def write_log(folder, num_images):
    """
    Generate a log file to the same folder as .raw file.
    Records the total number of frames in .raw.
    This log is used to check if the image extraction is complete.

    Args:
    folder -- folder of .raw
    num_images -- total number of frames in .raw
    """

    with open(os.path.join(folder, 'extract_log.txt'), 'w') as f:
        f.write("Raw image has {:d} frames".format(num_images))

def disk_capacity_check(file):
    """Check if the capacity of disk is larger than twice of the file size.
    Args:
    file -- directory of the (.nd2) file being converted
    Returns:
    flag -- bool, True if capacity is enough.
    """
    fs = os.path.getsize(file) / 2**30
    ds = shutil.disk_usage(file)[2] / 2**30
    print("File size {0:.1f} GB, Disk size {1:.1f} GB".format(fs, ds))
    return ds > 2 * fs

def raw_to_tif(raw_file, img_dim, save_folder):
    """ Read RawImage.raw and save .tif images
    Args:
    raw_file -- the directory of .raw file
    img_dim -- the (h, w) tuple of each frame
    save_folder -- folder to save .tif image sequence

    Returns:
    None

    Test:
    raw_file = os.path.join(folder, 'RawImage.raw')
    img_dim = (1024, 1024)
    save_folder = os.path.join(folder, 'images')
    raw_to_tif(raw_file, img_dim, save_folder)
    """
    if disk_capacity_check(raw_file) == False:
        print("No enough disk capacity!")
        exit()
    print("DISK CAPACITY OK")
    # read the binary file as a sequence of uint16
    a = np.fromfile(raw_file, dtype='uint16')

    # we check if the number of numbers in array a can be divided exactly by h*w+2
    h, w = img_dim
    assert(a.shape[0] % (h*w+2) == 0)

    # slice the sequential data into labels and images
    num_images = a.shape[0] // (h*w+2)
    img_in_row = a.reshape(num_images, h*w+2)
    labels = img_in_row[:, :2] # not in use currently
    images = img_in_row[:, 2:]

    # reshape the images from 1D to 2D
    images_reshape = images.reshape(num_images, h, w)

    # write log
    folder = os.path.split(raw_file)[0]
    # write_log(folder, num_images)

    # save the images as .tif sequence in save_folder
    if os.path.exists(save_folder) == False:
        os.makedirs(save_folder)

    # create folders
    out_raw_folder = os.path.join(save_folder, 'raw')
    out_8_folder = os.path.join(save_folder, '8-bit')
    if os.path.exists(out_raw_folder) == False:
        os.makedirs(out_raw_folder)
    if os.path.exists(out_8_folder) == False:
        os.makedirs(out_8_folder)
    
    # create log files
    with open(os.path.join(out_raw_folder, 'log.txt'), 'w') as f:
        f.write('Start to convert {} to raw tif images.\n'.format(raw_file))
    with open(os.path.join(out_8_folder, 'log.txt'), 'w') as f:
        f.write('Start to convert {} to 8-bit tif images.\n'.format(raw_file))   
    
    # save the image sequence
    num = 0
    for label, img in zip(labels, images_reshape):
        # num = label[0] + label[1] * 2 ** 16 + 1 # convert image label to uint32 to match the info in StagePosition.txt
        io.imsave(os.path.join(save_folder, 'raw', '{:05d}.tif'.format(num)), img, check_contrast=False)
        io.imsave(os.path.join(save_folder, '8-bit', '{:05d}.tif'.format(num)), to8bit(img), check_contrast=False)
        with open(os.path.join(out_raw_folder, 'log.txt'), 'a') as f:
            f.write(time.asctime() + ' // frame {:05d}'.format(num))
        with open(os.path.join(out_8_folder, 'log.txt'), 'a') as f:
            f.write(time.asctime() + ' // frame {:05d}'.format(num))   
        num += 1

if __name__=="__main__":    
    folder = sys.argv[1]
    if check_necessary_files(folder):
        info_file = os.path.join(folder, 'RawImageInfo.txt')
        raw_file = os.path.join(folder, 'RawImage.raw')
        save_folder = os.path.join(folder)
        fps, h, w = read_raw_image_info(info_file)
        raw_to_tif(raw_file, (h, w), save_folder)
    else:
        print('Incomplete files')


