from pivLib import read_piv
import numpy as np
import pandas as pd
from myImageLib import readdata, show_progress
import sys
import os

"""
DESCRIPTION
===========
This script compute "volumetric flow rate" in a channel from 2D PIV data. The unit of the flow rate will be px^2/s (it comes from a mean velocity, px/s, multiplied by a width, px).

SYNTAX
======
python flowrate.py main_piv_folder flowrate_dir dt

main_piv_folder -- the folder contains PIV of all crops (channels).
flowrate_dir -- full directory of flow rate data file (.csv). The data will be ["crop-0", "crop-1", "crop-2", "t"].
dt -- time interval between two PIV data (2/FPS)

EDIT
====
11032022 -- Initial commit.
"""

main_piv_folder = sys.argv[1]
flowrate_dir = sys.argv[2]
dt = float(sys.argv[3])

if os.path.exists(os.path.split(flowrate_dir)[0]) == False:
    os.makedirs(os.path.split(flowrate_dir)[0])
    
def compute_flowrate(x, y, u, v):
    """
    Compute volumetric flow rate from masked PIV results. 
    x, y, u, v -- PIV data.
    """
    mask = ~np.isnan(v)
    x[~mask] = np.nan
    W = np.nanmax(x, axis=1) - np.nanmin(x, axis=1) # channel width along y, px
    v_meanx = np.nanmean(v, axis=1)
    Q = np.nanmean(W*v_meanx)
    return Q

sfL = next(os.walk(main_piv_folder))[1]
df = pd.DataFrame()
for sf in sfL:
    piv_folder = os.path.join(main_piv_folder, sf)
    l = readdata(piv_folder, "csv")
    Q_list = []
    for num, i in l.iterrows():
        x, y, u, v = read_piv(i.Dir)
        Q = compute_flowrate(x, y, u, v)
        Q_list.append(Q)
    df[sf] = Q_list
df = df.assign(t=df.index*dt)
df.to_csv(flowrate_dir, index=False)