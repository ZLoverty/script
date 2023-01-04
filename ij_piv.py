from myImageLib import readdata, show_progress
from pivLib import compact_PIV
import os
import sys

"""
ij_piv
==========

Invoke ImageJ2 to run PIV macro "PIV_STACK_directory.ijm" based on "PIV_.jar" plugin, in headless mode. For more information about ImageJ headless mode, see `here <https://imagej.net/learn/headless>`_.

The macro itself is capable of iterating over all the \*.tif files in a given directory, so there is no need to repeat in the python script.

.. rubric:: Syntax

.. code-block:: console

   python ij_piv.py img_folder

* img_folder: folder containing \*.tif images

.. note::

   To be able to run the command `ImageJ` or `ImageJ-win64` (or other variants of ImageJ in different OS), we need to include the directory of the executable (.exe on windows) in the system path.

.. note::

   I put the actual macro file "PIV_STACK_directory.ijm" in the main macro folder of FIJI (in my case "C:\Fiji.app\macro"), so that ImageJ can find it without specifying the full path. On a different computer, I need to repeat this step.

.. note::

   I did a slight modification on the PIV_.jar, just to suppress the tedious logging info every step. The core algorithm should be the same as the original plugin.  

.. rubric:: Edit

* Dec 02, 2022 -- Initial commit.
* Jan 04, 2023 -- Add quotation marks \" around directories, to make it capable of processing directories with spaces.
"""

img_folder = sys.argv[1]

os.system("ImageJ-win64 --headless --console -macro PIV_STACK_directory.ijm \"{}\"".format(img_folder))
