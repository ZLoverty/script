import numpy as np
import pandas as pd
import os
import sys
import time
from corrLib import readdata

"""
circulation_order_parameter
===========================

Compute circulation order parameter according to Wioland 2013. Technical details can be found in `my note <https://github.com/ZLoverty/DE/blob/main/Notes/Analysis_of_collective_motions_in_droplets.pdf>`_.

.. rubric:: Syntax

.. code-block:: console

   python circulation_order_parameter.py piv_folder out_folder x y

* piv_folder -- folder containing PIV data (.csv), file names indicate frame number
* out_folder -- order parameter data file (.csv), contain frame and OP
* x, y -- the center position

A folder of PIV files are used to generate a single order parameter data file.

.. rubric:: Test

.. code-block:: console

   python circulation_order_parameter.py test_images\circulation_order_parameter\piv test_images\circulation_order_parameter\order_parameter 259 227

.. rubric:: Edit

* Jan 02, 2021 -- Initial commit.
"""

# %% codecell
def tangent_unit(point, center):
    """Compute tangent unit vector based on point coords and center coords.
    Args:
    point -- 2-tuple
    center -- 2-tuple
    Returns:
    tu -- tangent unit vector
    """
    point = np.array(point)
    # center = np.array(center)
    r = np.array((point[0] - center[0], point[1] - center[1]))
    # the following two lines set the initial value for the x of the tangent vector
    ind = np.logical_or(r[1] > 0, np.logical_and(r[1] == 0, r[0] > 0))
    x1 = np.ones(point.shape[1:])
    x1[ind] = -1
    # avoid divided by 0
    r[1][r[1]==0] = np.nan

    y1 = - x1 * r[0] / r[1]
    length = (x1**2 + y1**2) ** 0.5
    return np.array([x1, y1]) / length

def order_parameter_wioland2013(pivData, center):
    """Compute order parameter with PIV data and droplet center coords using the method from wioland2013.
    Args:
    pivData -- DataFrame of x, y, u, v
    center -- 2-tuple droplet center coords
    Return:
    OP -- float, max to 1
    """
    point = (pivData.x, pivData.y)
    tu = tangent_unit(point, center)
    # \Sigma vt
    sum_vt = abs((pivData.u * tu[0] + pivData.v * tu[1])).sum()
    sum_v = ((pivData.u**2 + pivData.v**2) ** 0.5).sum()
    OP = (sum_vt/sum_v - 2/np.pi) / (1 - 2/np.pi)
    return OP

# %% codecell
# test mean_v
def test():
    pivData = pd.read_csv(r"test_images\piv_drop\06972-06973.csv")
    v = mean_v(pivData)
    print("mean velocity is {:.2f}".format(v))

if __name__=="__main__":
    piv_folder = sys.argv[1]
    out_folder = sys.argv[2]
    x = float(sys.argv[3])
    y = float(sys.argv[4])
    out_filename = os.path.split(piv_folder)[1] + ".csv"
    l = readdata(piv_folder, 'csv')
    if os.path.exists(out_folder) == False:
        os.makedirs(out_folder)
    # with open(os.path.join(out_folder, "log.txt"), "w") as f:
    #     f.write(time.asctime() + " \\ Start computing mean velocity of {}\n".format(piv_folder))
    frame_list = []
    OP_list = []
    for num, i in l.iterrows():
        frame_number = int(i.Name.split("-")[0])
        pivData = pd.read_csv(i.Dir)
        OP = order_parameter_wioland2013(pivData, (x, y))
        frame_list.append(frame_number)
        OP_list.append(OP)
    result = pd.DataFrame({"frame": frame_list, "OP": OP_list})
    result.to_csv(os.path.join(out_folder, out_filename), index=False)
    # with open(os.path.join(out_folder, "log.txt"), "a") as f:
    #     f.write(time.asctime() + " \\ Finish!".format(piv_folder))
