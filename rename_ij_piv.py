"""
Rename the PIV data file generated by the ImageJ macro ``_0.txt`` to my format ``{:05d}.csv``. Keep only x, y, u, v columns and add mask column if applicable.

.. rubric:: Syntax

.. code-block:: console

   python rename_ij_piv.py piv_folder

* piv_folder: piv data folder containing .txt files

.. rubric:: Edit

* Nov 30, 2022 -- Initial commit.
* Dec 01, 2022 -- Remove apply mask step, because it is not indicated in the script name and could be confusing.
* Dec 13, 2022 -- Remove residual mask related code.
* Jan 05, 2023 -- (i) Remove unused import. (ii) Adapt myimagelib import style.
* Feb 08, 2023 -- Rewrite in function wrapper form, to make autodoc work properly. (autodoc import the script and execute it, so anything outside ``if __name__=="__main__"`` will be executed, causing problems)
"""
import os
import sys
import pandas as pd
from skimage import io
from myimagelib.myImageLib import readdata, show_progress

if __name__ == "__main__":

   piv_folder = sys.argv[1]

   l = readdata(piv_folder, "txt")
   nFiles = len(l)
   for num, i in l.iterrows():
      show_progress((num+1)/nFiles, os.path.split(piv_folder)[1])
      pivData = pd.read_csv(i.Dir, usecols=[0,1,2,3], names=["x", "y", "u", "v"], sep=" ")
      pivData.to_csv(os.path.join(piv_folder, "{:05d}.csv".format(int(i.Name.strip("_")))), index=False)
      os.remove(i.Dir)