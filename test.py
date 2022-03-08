import os
import pandas as pd

positions = pd.read_csv(r"test_images\moving_mask_piv\positions.csv")
name = "16"
i = positions.loc[positions.Label=="{}.tif".format(name)]
cmd = r"python moving_mask_piv.py test_images\moving_mask_piv\raw test_images\moving_mask_piv\piv_result 20 10 0.02 test_images\moving_mask_piv\mask.tif {0:d} {1:d} {2:d} {3:d}".format(int(i.X), int(i.Y), int(i.Major), int(i.Major))
os.system(cmd)
