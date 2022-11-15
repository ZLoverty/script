import pandas as pd
import sys
import os
import time
from pivLib import piv_data
from myImageLib import readdata

"""
velocity_autocorr
=================

Apply autocorrelation analysis on sequential PIV data.

.. rubric:: Syntax

.. code-block:: console

   python velocity_autocorr.py piv_folder out_folder [fps=50] [cutoff=2000]

* fps: the imaging frame rate
* cutoff: frame number above which the velocity data are not included in the analysis

.. rubric:: Test

.. code-block:: console

   python velocity_autocorr.py test_images\velocity_autocorr test_images\velocity_autocorr\vac_result 50 20

.. rubric:: Edit

* Dec 13, 2021 -- Initial commit.
* Feb 21, 2022 -- Rewrite with new functions.
* Mar 16, 2022 --

    1. Rewrite with piv_data class
    2. Use fps instead of dt as input argument
    3. Modify doc string

* Mar 23, 2022 -- add smoothn as an optional smoothing method
* Nov 15, 2022 -- Make ``fps`` and ``cutoff`` real *keyword* args.
"""

def main(piv_folder, out_folder, **kwargs):
    fps = 50
    cutoff = 2000
    # if len(sys.argv) > 3:
    #     fps = float(sys.argv[3])
    # if len(sys.argv) > 4:
    #     cutoff = int(sys.argv[4])

    for kw in kwargs:
        if kw == "fps":
            fps = float(kwargs[kw])
        if kw == "cutoff":
            cutoff = int(kwargs[kw])

    if os.path.exists(out_folder) == False:
        os.makedirs(out_folder)

    l = readdata(piv_folder, "csv")
    piv = piv_data(l, fps=fps, cutoff=cutoff)
    ac = piv.vacf(smooth_method="smoothn")

    out_filename = os.path.split(piv_folder)[1] + ".csv"
    ac.to_csv(os.path.join(out_folder, out_filename))

if __name__=="__main__":
    piv_folder = sys.argv[1]
    out_folder = sys.argv[2]
    main(piv_folder, out_folder, **dict(arg.split("=") for arg in sys.argv[3:]))
