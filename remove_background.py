"""
This script removes the stationary background of a tif sequence in a given folder. Specifically, it does:

- Median z-projection
- divide raw images by the projection

By default, it replaces the original images with background removed images. 

.. rubric:: Syntax

.. code-block:: console

   python remove_background.py img_folder

* img_folder -- A folder of tiffstacks.

.. note::

   Here the processed images are converted to 8-bit images. Autocontrast is applied.

.. warning::

   Since the bifurcation images always require background subtraction, this procedure is included in the "crop_channel.py" script. We can still apply this script, but it essentially has no effect.
   
.. rubric:: Edit

* Nov 03, 2022 -- Initial commit.
* Jan 04, 2023 -- (i) Target on a folder of tiffstacks. Remove the background of each tiffstack, based on their own median image. (ii) Change default saving behavior: now REPLACE the original images with background removed images.
* Jan 05, 2023 -- Adapt myimagelib import style.
* Feb 08, 2023 -- Rewrite in function wrapper form, to make autodoc work properly. (autodoc import the script and execute it, so anything outside ``if __name__=="__main__"`` will be executed, causing problems)
"""

if __name__ == "__main__":

   from skimage import io
   import numpy as np
   import os
   import sys
   from myimagelib.myImageLib import readdata, show_progress, to8bit
   from tifffile import imwrite



   img_folder = sys.argv[1]
   l = readdata(img_folder, "tif")
   print("Reading images ...")
   for num, i in l.iterrows():
      print(i.Dir)
      stack = io.imread(i.Dir)
      med = np.median(stack, axis=0)
      stackr = stack / med
      stackr8 = to8bit(stackr)
      imwrite(i.Dir, stackr8)
