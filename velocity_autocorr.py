import pandas as pd
from corrLib import readdata, autocorr_t, vacf_piv
from myImageLib import bpass
from skimage import io
import numpy as np
import sys
import os
import time
from pivLib import read_piv_stack, read_piv
import scipy
import pdb

"""
GENERAL
=======
Apply autocorrelation analysis on sequential PIV data.
Modified based on `autocorr_imseq.py`.

USAGE
=====
python velocity_autocorr.py piv_folder out_folder [dt] [cutoff]

cutoff is set to analysis only the initial part of the velocity data.

TEST
====
python velocity_autocorr.py test_images\velocity_autocorr test_images\velocity_autocorr\vac_result 0.1 20

LOG
===
Mon Feb 21 17:44:33 2022 // Computing VACF of test_images\velocity_autocorr

EDIT
====
Dec 13, 2021 -- Initial commit.
Feb 21, 2022 -- Rewrite with new functions.
"""

if __name__=="__main__":
    piv_folder = sys.argv[1]
    out_folder = sys.argv[2]
    dt = 0.04 # fps=50, dt = 2/fps
    cutoff = 250
    if len(sys.argv) > 3:
        dt = float(sys.argv[3])
    if len(sys.argv) > 4:
        cutoff = int(sys.argv[4])

    if os.path.exists(out_folder) == False:
        os.makedirs(out_folder)

    out_filename = os.path.split(piv_folder)[1] + ".csv"

    print(time.asctime() + " // Computing VACF of {}".format(piv_folder))

    ustack, vstack = read_piv_stack(piv_folder, cutoff=cutoff)

    # smooth the velocity fields with gaussian filter (4*sigma=3)

    ustack = scipy.ndimage.gaussian_filter(ustack, (3/4,0,0))
    vstack = scipy.ndimage.gaussian_filter(vstack, (3/4,0,0))

    # The two step can potentially be combined by using 4-D arrays

    cu = vacf_piv(ustack, dt, mode="direct").rename(columns={"c": "ucorr"})
    cv = vacf_piv(vstack, dt, mode="direct").rename(columns={"c": "vcorr"})

    vac_data = pd.concat((cu, cv), axis=1)
    vac_data.to_csv(os.path.join(out_folder, out_filename))
