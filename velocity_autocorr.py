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
def autocorr_imseq(stack):
    """Compute intensity autocorrelation of an image sequence.
    Args:
    stack -- A 3D array
    Returns:
    ac_mean -- the autocorrelation
    Test:
    stack = np.load(r'E:\moreData\08032020\small_imseq\06\stack.npy')[3000:3600]
    ac = autocorr_imseq(stack)
    plt.plot(np.arange(0, 600)/30, ac)
    Edit:
    Dec 13, 2021 -- Copy from corr_utils.py.
    """
    def autocorr(x):
        x = (x - np.nanmean(x)) / np.nanstd(x)
        result = np.correlate(x, x, mode='full')/len(x)
        return result[len(result)//2:]
    r = stack.reshape((stack.shape[0], stack.shape[1]*stack.shape[2])).transpose()
    ac_list = []
    for x in r:
        ac = autocorr(x)
        ac_list.append(ac)
    ac_stack = np.stack(ac_list)
    ac_mean = np.nanmean(ac_stack, axis=0)
    return ac_mean

def test():
    piv_folder = sys.argv[1]
    out_folder = sys.argv[2]
    if os.path.exists(out_folder) == False:
        os.makedirs(out_folder)
    with open(os.path.join(out_folder, 'log.txt'), 'w') as f:
        f.write(time.asctime() + " \\ Compute velocity autocorrelation function of PIV data in {}\n".format(piv_folder))
        f.write(time.asctime() + " \\ The results will be saved in {}\n".format(out_folder))

    l = readdata(piv_folder, "csv")
    u_list = []
    v_list = []
    t_list = []
    for num, i in l.iterrows():
        X, Y, U, V = read_piv(i.Dir)
        t = int(i.Name.split("-")[0])
        u_list.append(U)
        v_list.append(V)
        t_list.append(t)
    u = np.stack(u_list, axis=0)
    v = np.stack(v_list, axis=0)
    u_ac = autocorr_imseq(u)
    v_ac = autocorr_imseq(v)
    vac = (u_ac + v_ac) / 2
    t = np.arange(len(vac)) * 2 # times 2 because PIV is done every 2 frames, unit: frame
    vac_data = pd.DataFrame({"t": t, "vac":vac})
    vac_data.to_csv(os.path.join(out_folder, "vac_data.csv"), index=False)

    with open(os.path.join(out_folder, 'log.txt'), 'a') as f:
        f.write(time.asctime() + " \\ Finish computing the VACF of {:d} velocity data".format(len(vac)))

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
    print(time.asctime() + " // Computing VACF of {}".format(piv_folder))

    ustack, vstack = read_piv_stack(piv_folder, cutoff=cutoff)

    # smooth the velocity fields with gaussian filter (4*sigma=3)

    ustack = scipy.ndimage.gaussian_filter(ustack, (3/4,0,0))
    vstack = scipy.ndimage.gaussian_filter(vstack, (3/4,0,0))

    # The two step can potentially be combined by using 4-D arrays

    cu = vacf_piv(ustack, dt, mode="direct").rename(columns={"c": "ucorr"})
    cv = vacf_piv(vstack, dt, mode="direct").rename(columns={"c": "vcorr"})

    vac_data = pd.concat((cu, cv), axis=1)
    vac_data.to_csv(os.path.join(out_folder, "vac_data.csv"))
