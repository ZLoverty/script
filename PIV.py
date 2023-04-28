"""
Particle image velocimetry (PIV) analysis on an image sequence. This script utilize the ``extended_search_area_piv()`` function of the `openpiv-python <>`_ package. Every pair of frames will give a velocity field, which will be saved as a table of [x, y, u, v]. For example, a 3-frame sequence will lead to 2 velocity fields, namely 1-2 and 2-3. More generally, an n-frame image will result in an (n-1)-frame velocity field. 

.. rubric:: Syntax

.. code-block:: console

   python PIV.py img [winsize piv_folder]

* img: can be i) tif sequence folder, ii) nd2 file dir, iii) tiffstack dir.
* winsize (optional): interrogation window size. Default is 32. Specify a different value with ``--winsize 16``.
* piv_folder (optional): folder to save PIV results. Default is ".", i.e. the same directory as the script. Specify a different folder with ``--piv_folder /folder/you/like``.

.. note::

   In this implementation, we set overlap as half of winsize.

.. rubric:: Test

.. code-block:: console

   python PIV.py test_images/piv_drop/ --piv_folder test_images/piv_drop/

.. rubric:: Edit

* Nov 03, 2022 -- Initial commit.
* Dec 06, 2022 -- i) Enable this script to process \*.nd2 files. ii) Check if reults already exist. iii) Pick up job from middle. (Only work for nd2 PIV for the moment) iv) query num frames using metadata, rather than ``images.shape``
* Dec 07, 2022 -- Fix undefined "start" issue.
* Jan 05, 2023 -- (i) Check if img exists. (ii) Adapt myimagelib import style.
* Feb 08, 2023 -- Rewrite in function wrapper form, to make autodoc work properly. (autodoc import the script and execute it, so anything outside ``if __name__=="__main__"`` will be executed, causing problems)
* Mar 23, 2023 -- Also process tiff stacks.
* Apr 28, 2023 -- (i) improve docstring, (ii) remove argument ``dt``, (iii) rewrite argument parser with argparse, (iv) make pair sampling consistent (every frame instead of every 2 frames).
"""

if __name__ == "__main__":

    from myimagelib.pivLib import PIV
    import sys
    import os
    from skimage import io
    from myimagelib.myImageLib import readdata, show_progress
    import pandas as pd
    from nd2reader import ND2Reader
    import argparse

    parser = argparse.ArgumentParser(prog="PIV")
    parser.add_argument("img")
    parser.add_argument("--winsize", type=int, default=32)
    parser.add_argument("--piv_folder", default=".")
    args = parser.parse_args()

    img = args.img
    winsize = args.winsize
    piv_folder = args.piv_folder
    dt = 1

    if os.path.exists(img) == False:
        raise ValueError("The specified image dir does not exist!")

    if os.path.exists(piv_folder) == False:
        os.makedirs(piv_folder)
        start = 0
    else: 
        # this means we have created a folder to save the results already
        # possibly, there are some results in this folder, but not completed
        # try to analyze the folder and determine if it's needed to pick up the job
        print("piv_folder {} exists, analyzing contents".format(piv_folder))
        lr = readdata(piv_folder, "csv")
        if len(lr) > 0:
            print("The folder has {:d} csv files".format(len(lr)))
            last_name = lr.iloc[-1]["Name"]
            # analyze the name
            print("The last csv file has name: {}".format(last_name))
            start = int(last_name.split("-")[0])
            print("Start doing PIV from frame {:d}".format(start))
            if start > len(lr): # check if there are missing results before
                print("There are files missing, start from beginning.")
                start = 0
        else:
            start = 0 
    overlap = winsize // 2

    if os.path.isdir(img):
        l = readdata(img, "tif")
        nImages = len(l)
        for ind0, ind1 in zip(l.index[:-1:], l.index[1::]):
            show_progress((ind0+2)/nImages, ind0+1)
            I0 = io.imread(l.at[ind0, "Dir"])
            I1 = io.imread(l.at[ind1, "Dir"])
            x, y, u, v = PIV(I0, I1, winsize, overlap, dt)
            pivData = pd.DataFrame({"x": x.flatten(), "y": y.flatten(), "u": u.flatten(), "v": v.flatten()})
            pivData.to_csv(os.path.join(piv_folder, "{0}.csv".format(l.at[ind0, "Name"])), index=False)
    
    elif img.endswith(".nd2"):
        with ND2Reader(img) as images:
            nImages = images.metadata["num_frames"]
            for i in range(start, nImages):
                show_progress((i+1)/nImages, i+1)
                I0 = images[i]
                I1 = images[i+1]
                x, y, u, v = PIV(I0, I1, winsize, overlap, dt)
                pivData = pd.DataFrame({"x": x.flatten(), "y": y.flatten(), "u": u.flatten(), "v": v.flatten()})
                pivData.to_csv(os.path.join(piv_folder, "{0:05d}.csv".format(i)), index=False)

    elif img.endswith(".tif"):
        img = io.imread(img)
        assert(len(img.shape)==3)
        nImages = len(img)
        for i, I0, I1 in zip(range(nImages-1), img[:-1], img[1:]):
            show_progress((i+1)/nImages, i+1)
            x, y, u, v = PIV(I0, I1, winsize, overlap, dt)
            pivData = pd.DataFrame({"x": x.flatten(), "y": y.flatten(), "u": u.flatten(), "v": v.flatten()})
            pivData.to_csv(os.path.join(piv_folder, "{0:05d}.csv".format(i)), index=False)