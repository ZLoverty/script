from multiprocessing import Pool, TimeoutError
import time
import os
from test1 import func, PIV_test
from corrLib import readdata

with Pool(4) as pool:
    print(pool.starmap(func, zip(range(10), range(10))))

# %% codecell
%%time
folder = r"C:\Users\liuzy\Data\DE\12092021\24"
l = readdata(folder, 'tif')

with Pool(12) as pool:
    pool.starmap(PIV_test, zip(l[::2].Dir, l[1::2].Dir, l[::2].index))
# 10.1 s - 12 procs
# 10.2 s - 4 procs
# 12.9 s - 3 procs
# 18.1 s - 2 procs
# 28.1 s - 1 proc

# %% codecell
%%time
folder = r"C:\Users\liuzy\Data\DE\12092021\24"
l = readdata(folder, 'tif')
for I0dir, I1dir, i in zip(l[::2].Dir, l[1::2].Dir, l[::2].index):
    PIV_test(I0dir, I1dir, i)
# 24.9 s
