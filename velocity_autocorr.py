import pandas as pd
import sys
import os
import time
from pivLib import piv_data
from myImageLib import readdata

"""
GENERAL
=======
Apply autocorrelation analysis on sequential PIV data.

USAGE
=====
python velocity_autocorr.py piv_folder out_folder [fps=50] [cutoff=250]

fps is the imaging frame rate and the dt between two adjacent frames is assumed to be 2 / fps
cutoff is set to analysis only the initial part of the velocity data.

TEST
====
python velocity_autocorr.py test_images\velocity_autocorr test_images\velocity_autocorr\vac_result 50 20

LOG
===
Mon Feb 21 17:44:33 2022 // Computing VACF of test_images\velocity_autocorr

EDIT
====
Dec 13, 2021 -- Initial commit.
Feb 21, 2022 -- Rewrite with new functions.
Mar 16, 2022 -- 1. Rewrite with piv_data class
                2. Use fps instead of dt as input argument
                3. Modify doc string
"""

if __name__=="__main__":
    piv_folder = sys.argv[1]
    out_folder = sys.argv[2]
    fps = 50
    cutoff = 2000
    if len(sys.argv) > 3:
        fps = float(sys.argv[3])
    if len(sys.argv) > 4:
        cutoff = int(sys.argv[4])

    if os.path.exists(out_folder) == False:
        os.makedirs(out_folder)

    l = readdata(piv_folder, "csv")
    piv = piv_data(l, fps=fps, cutoff=cutoff)
    ac = piv.vacf(smooth_method="smoothn")

    out_filename = os.path.split(piv_folder)[1] + ".csv"
    ac.to_csv(os.path.join(out_folder, out_filename))
