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
python velocity_autocorr.py test_images\velocity_autocorr test_images\velocity_autocorr\vac_result 0.1 20

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
    cutoff = 250
    if len(sys.argv) > 3:
        dt = float(sys.argv[3])
    if len(sys.argv) > 4:
        cutoff = int(sys.argv[4])

    if os.path.exists(out_folder) == False:
        os.makedirs(out_folder)
        
    l = readdata(piv_folder, "csv")
    piv = piv_data(l, fps=fps)
    ac = piv.vacf()

    out_filename = os.path.split(piv_folder)[1] + ".csv"
    ac.to_csv(os.path.join(out_folder, out_filename))





    # if os.path.exists(out_folder) == False:
    #     os.makedirs(out_folder)
    #
    # out_filename = os.path.split(piv_folder)[1] + ".csv"
    #
    # print(time.asctime() + " // Computing VACF of {}".format(piv_folder))
    #
    # ustack, vstack = read_piv_stack(piv_folder, cutoff=cutoff)
    #
    # # smooth the velocity fields with gaussian filter (4*sigma=3)
    #
    # ustack = scipy.ndimage.gaussian_filter(ustack, (3/4,0,0))
    # vstack = scipy.ndimage.gaussian_filter(vstack, (3/4,0,0))
    #
    # # The two step can potentially be combined by using 4-D arrays
    #
    # cu = vacf_piv(ustack, dt, mode="direct").rename(columns={"c": "ucorr"})
    # cv = vacf_piv(vstack, dt, mode="direct").rename(columns={"c": "vcorr"})
    #
    # vac_data = pd.concat((cu, cv), axis=1)
    # vac_data.to_csv(os.path.join(out_folder, out_filename))
