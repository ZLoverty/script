"""
Delete all the .tif files generated by ``to_tif.py`` script, in a given directory. Note that instead of looking for .tif files, the script looks for folders "8-bit" and "raw".

.. rubric:: Syntax

   python cleanup_tif.py folder

* folder -- any folder that contains .tif files generated by ``to_tif.py``

.. rubric:: Test

   python cleanup_tif.py test_images

.. rubric:: Edit

* Mar 09, 2023 -- Initial commit.
"""

import os
import sys
import shutil

if __name__ == "__main__":

    folder = sys.argv[1]
    for r, s, f in os.walk(folder):
        for sf in s:
            if sf == "8-bit" or sf == "raw":
                d = os.path.join(r, sf)
                print("Deleting {}".format(d))
                shutil.rmtree(d)