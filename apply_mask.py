"""
Apply mask on PIV data. It calls :py:func:`pivLib.apply_mask` to treat the input PIV data, and save the results (masked PIV data) in the same files. See `here <https://zloverty.github.io/mylib/pivLib/pivLib.apply_mask.html>`_ for more details.

.. rubric:: Syntax

.. code-block:: console

   python apply_mask.py piv_folder mask_dir

* piv_folder: folder containing PIV data (csv sequence)
* mask_dir: directory of a tif binary mask, of the same shape as raw images.
* erode: number of pixels to erode from the True region (this makes the mask smaller, reducing boundary effect). Default to 32, a good value is the winsize of PIV.

.. rubric:: Test

.. code-block:: console

   python apply_mask.py test_images\apply_mask test_images\apply_mask\A.tif

.. rubric:: Edit

* Nov 03, 2022 -- Initial commit.
* Dec 01, 2022 -- Remove erosion step. Mask should be used as it is.
* Dec 13, 2022 -- Fix a bug.
* Dec 19, 2022 -- More accurate docstring.
* Jan 05, 2023 -- (i) Adapt myimagelib import style. (ii) Add screen info.
* Feb 08, 2023 -- Rewrite in function wrapper form, to make autodoc work properly. (autodoc import the script and execute it, so anything outside ``if __name__=="__main__"`` will be executed, causing problems)
"""

if __name__=="__main__":

   import pandas as pd
   import numpy as np
   import os
   import sys
   from skimage import io
   from myimagelib.myImageLib import readdata, show_progress
   from myimagelib.pivLib import apply_mask



   def main(piv_folder, mask_dir):
      
      mask = io.imread(mask_dir)

      l = readdata(piv_folder, "csv")
      numFiles = len(l)

      print("applying mask to {}".format(piv_folder))

      for num, i in l.iterrows():
         show_progress((num+1)/numFiles, num+1)
         pivData = pd.read_csv(i.Dir)
         pivData = apply_mask(pivData, mask)
         pivData.to_csv(i.Dir, index=False)


   piv_folder = sys.argv[1]
   mask_dir = sys.argv[2]
   main(piv_folder, mask_dir)