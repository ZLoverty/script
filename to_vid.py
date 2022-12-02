import os
from myImageLib import dirrec
import sys

"""
to_vid
======

Convert all the image sequence in a given folder to videos (avi). It is a wrapper of `ffmpeg <https://ffmpeg.org/>`_, which is a prerequisite of this script. Videos will be saved in the parent folder of the image sequence folder.

.. rubric:: Syntax

.. code-block:: console

   python to_vid.py folder [fmt=%05d.tif] [fps=50]

* folder -- the folder that contains the 8-bit tif image sequence, this script convert all 8-bit image sequences in given folder by default
* fmt -- specify the format of image file name, default to ``%05d.tif``
* fps -- specify the frame rate of the output video, default to ``50``


.. rubric:: Edit

* Nov 24, 2021 -- initial commit.
* Nov 26, 2021 -- Major change: now convert all the 8-bit folder in given folder to videos Change name to ``to_vid.py``
* Dec 08, 2021 -- Check if the target .avi file exists already. If so, skip the conversion.
"""

def main(folder, **kwargs):
    fps = 50
    fmt = "%05d.tif"
    for kw in kwargs:
        if kw == "fmt":
            fmt = kwargs[kw]
        if kw == "fps":
            fps = float(kwargs[kw])
    l = dirrec(folder, fmt % 0)
    for i in l:
        if "8-bit" in i:
            image_folder = os.path.split(i)[0]
            parent_folder, name = os.path.split(os.path.split(image_folder)[0]) # assume name/8-bit/*.tif
            output_file = os.path.join(parent_folder, "{}.avi".format(name))
            if os.path.exists(output_file) == False:
                input_imseq = os.path.join(image_folder, fmt)
                cmd = 'ffmpeg -y -framerate {0:f} -i {1} -vcodec h264 {2}'.format(fps, input_imseq, output_file)
                print("==============Start converting {} to video~~==============\n".format(name))
                os.system(cmd)
                print("\nConversion of {0} is successful!\nA video is saved at {1}\n\n".format(name, output_file))
            else:
                print("{} already exists, skipping ============".format(output_file))
        else:
            print("Cannot find 8-bit folder in {}".format(i))

if __name__=="__main__":
    folder = sys.argv[1]
    main(folder, **dict(arg.split('=') for arg in sys.argv[2:]))