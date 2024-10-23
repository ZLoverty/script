
"""
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
* Jan 05, 2023 -- Adapt myimagelib import style.
* Feb 08, 2023 -- Rewrite in function wrapper form, to make autodoc work properly. (autodoc import the script and execute it, so anything outside ``if __name__=="__main__"`` will be executed, causing problems)
* Oct 04, 2024 -- Add argument parser to make it more user-friendly. Only convert one video now, instead of all videos in the folder.
* Oct 17, 2024 -- Add a filter to ensure the dimensions are divisible by 2.
"""

def main(folder, fmt, fps):
    input_imseq = os.path.join(folder, fmt)
    name = os.path.basename(folder)
    output_file = os.path.join(os.path.dirname(folder), name+".mp4")

    cmd = (
        "ffmpeg -y -framerate {0:f} -i \"{1}\" "
        "-vf \"pad=ceil(iw/2)*2:ceil(ih/2)*2\" "
        "-b:v 4M -minrate 4M -maxrate 4M -bufsize 4M -pix_fmt yuv420p \"{2}\""
    ).format(fps, input_imseq, output_file)
    print("==============Start converting {} to video~~==============\n".format(name))
    os.system(cmd)
    print("\nConversion of {0} is successful!\nA video is saved at {1}\n\n".format(name, output_file))

if __name__=="__main__":

    import os
    import sys
    import argparse

    # Parse arguments
    parser = argparse.ArgumentParser(description='Convert 8-bit tif image sequences to videos.')
    parser.add_argument('folder', type=str, help='The folder that contains the 8-bit tif image sequence.')
    parser.add_argument('--fmt', type=str, default="%05d.tif", help='Specify the format of image file name.')
    parser.add_argument('--fps', type=float, default=30, help='Specify the frame rate of the output video.')

    args = parser.parse_args()
    folder = args.folder
    fmt = args.fmt
    fps = args.fps

    main(folder, fmt, fps)
