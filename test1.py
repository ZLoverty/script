import os
import pandas as pd
from pivLib import PIV
from skimage import io
import pdb
def func(a, b):
    return a*a + b

def PIV_test(I0dir, I1dir, i):
    I0 = io.imread(I0dir)
    I1 = io.imread(I1dir)
    winsize = 40
    overlap = 20
    dt = 0.02
    x, y, u, v = PIV(I0, I1, winsize, overlap, dt)
    data = pd.DataFrame({"x": x.flatten(), "y": y.flatten(), "u": u.flatten(), "v": v.flatten()})
    data.to_csv(r"C:\Users\liuzy\Data\DE\12092021\piv_test\{:05d}.csv".format(i))
