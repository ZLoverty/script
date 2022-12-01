
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
