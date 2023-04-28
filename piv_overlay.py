"""
Generate PIV arrow overlayed images for PIV visual inspection and illustration.

.. rubric:: Syntax

.. code-block:: console

   python piv_overlay.py matDir imgDir output_folder [optional args]

* matDir -- compact PIV data file (.mat) directory
* imgDir -- tiffstack image file (.tif) directory
* output_folder -- folder to save the PIV overlay images in .jpg files
* output_width (optional) -- specify the width of output overlay images (pixels). Default is 300. To use, do ``--width 300``.

.. rubric:: Test

.. code-block:: console

   python piv_overlay.py test_images\piv_drop test_images\piv_drop test_images\piv_overlay 1

.. rubric:: Edit

* Jan 03, 2022 -- (i) move from PIV to script, (ii) set scale, (iii) update docstring, (iv) minor structural changes

.. note::
   See `PIV technical report Sec II.A.1 <https://github.com/ZLoverty/DE/blob/main/Notes/PIV_technical_report.pdf>`_ for the reasoning of scale settings.

* Jan 22, 2022 -- reduce scale by 1.5 to increase the arrow size
* Mar 03, 2022 -- (i) Use `droplet_image` class to rewrite the script, (ii) remove logging
* Jan 05, 2023 -- Adapt myimagelib import style.
* Feb 08, 2023 -- Rewrite in function wrapper form, to make autodoc work properly. (autodoc import the script and execute it, so anything outside ``if __name__=="__main__"`` will be executed, causing problems)
* Apr 27, 2023 -- (i) Stop using ``droplet_image`` class for making PIV overlay. Making PIV overlay is necessary in multiple projects and should be made more general. (ii) In this edit, we use tiffstack and compact PIV as the standard input for this script. In future versions, nd2 should also be legit input images. (iii) Sparcity argument is disabled temporarily. (iv) rewrite commandline argument parser with argparse module. 
"""

import os
import argparse
import numpy as np
from skimage import io
import matplotlib.pyplot as plt
from scipy.io import loadmat



def determine_arrow_scale(u, v, sparcity):
    row, col = u.shape
    return max(np.nanmax(u), np.nanmax(v)) * col / sparcity / 1.5

if __name__=="__main__": 
    parser = argparse.ArgumentParser(prog="pivOverlay", description="Generate PIV overlay images.", )
    parser.add_argument("matDir")
    parser.add_argument("imgDir")
    parser.add_argument("output_folder")
    parser.add_argument("--width", type=int, default=300)
    parser.add_argument("--sparcity", type=int, default=1)
    args = parser.parse_args()

    img = io.imread(args.imgDir)
    cpiv_dict = loadmat(args.matDir)
    if os.path.exists(args.output_folder) == False:
        os.makedirs(args.output_folder)
    x, y, U, V, mask = cpiv_dict["x"], cpiv_dict["y"], cpiv_dict["u"], cpiv_dict["v"], cpiv_dict["mask"]
    U[:, ~(mask>mask.mean())] = np.nan
    V[:, ~(mask>mask.mean())] = np.nan


    f, h, w = img.shape
    scale = max(np.nanmax(U), np.nanmax(V)) * U.shape[2] / 5

    fig = plt.figure(figsize=(1, h/w), dpi=args.width)
    ax = fig.add_axes([0,0,1,1])
    ax.axis("off")
    
    l = ax.imshow(img[0], cmap="gray")
    q = ax.quiver(x, y, U[0], V[0], color="yellow", scale=scale, scale_units="width")


    for i, u, v in zip(range(len(U)), U, V):
        print(i)
        l.set(data=img[i])
        ## note: this script does not match image and PIV data in an intelligent way.
        q.set_UVC(u, -v)
        fig.canvas.draw_idle()
        fig.savefig(os.path.join(args.output_folder, "{:05d}.jpg".format(i)))

    plt.close()