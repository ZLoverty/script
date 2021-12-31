import numpy as np
import pandas as pd
import os
import sys
import time
from corrLib import readdata

"""
Compute mean velocity of PIV data.
1. Compute the magnitude of each PIV arrow
2. Take average of these arrows

USAGE
=====
python mean_velocity.py piv_folder out_file

piv_folder -- folder containing PIV data (.csv), file names indicate frame number
out_file -- mean velocity data file (.csv), contain frame and mean_v columns

A folder of PIV files are used to generate a single mean velocity data file.

TEST
====
python mean_velocity.py test_images\piv_drop test_images\mean_velocity

TEST OUTPUT
===========
```log.txt
Fri Dec 31 23:32:00 2021 \ Start computing mean velocity of test_images\piv_drop
Fri Dec 31 23:32:00 2021 \ Finish!
```

```piv_drop
frame,mean_v
6972,7.259217406587053
6974,7.9069235460355465
```

EDIT
====
Dec 31, 2021 -- Initial commit.
"""


# %% codecell
def mean_v(pivData):
    """
    pivData -- DataFrame of x, y, u, v
    Returns:
    velocity -- mean velocity
    """
    vs = (pivData.u ** 2 + pivData.v ** 2) ** 0.5
    velocity = np.nanmean(vs)
    return velocity

# %% codecell
# test mean_v
def test():
    pivData = pd.read_csv(r"test_images\piv_drop\06972-06973.csv")
    v = mean_v(pivData)
    print("mean velocity is {:.2f}".format(v))

if __name__=="__main__":
    piv_folder = sys.argv[1]
    out_folder = sys.argv[2]
    out_filename = os.path.split(piv_folder)[1]
    l = readdata(piv_folder, 'csv')
    if os.path.exists(out_folder) == False:
        os.makedirs(out_folder)
    with open(os.path.join(out_folder, "log.txt"), "w") as f:
        f.write(time.asctime() + " \\ Start computing mean velocity of {}\n".format(piv_folder))
    frame_list = []
    v_list = []
    for num, i in l.iterrows():
        frame_number = int(i.Name.split("-")[0])
        pivData = pd.read_csv(i.Dir)
        v = mean_v(pivData)
        frame_list.append(frame_number)
        v_list.append(v)
    result = pd.DataFrame({"frame": frame_list, "mean_v": v_list})
    result.to_csv(os.path.join(out_folder, out_filename), index=False)
    with open(os.path.join(out_folder, "log.txt"), "a") as f:
        f.write(time.asctime() + " \\ Finish!".format(piv_folder))
