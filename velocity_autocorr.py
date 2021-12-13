import pandas as pd
from corrLib import readdata, match_hist
from myImageLib import bpass
from skimage import io
import numpy as np
import sys
import os
import time
from pivLib import read_piv

"""
GENERAL
=======
Apply autocorrelation analysis on sequential PIV data.
Modified based on `autocorr_imseq.py`.

USAGE
=====
python velocity_autocorr.py piv_folder out_folder

TEST
====
python velocity_autocorr.py test_images\velocity_autocorr test_images\velocity_autocorr\vac_result

LOG
===
Mon Dec 13 22:56:05 2021 \ Compute velocity autocorrelation function of PIV data in test_images\velocity_autocorr
Mon Dec 13 22:56:05 2021 \ The results will be saved in test_images\velocity_autocorr\vac_result
Mon Dec 13 22:56:05 2021 \ Finish computing the VACF of 15 velocity data

EDIT
====
Dec 13, 2021 -- Initial commit.
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

if __name__=="__main__":
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
