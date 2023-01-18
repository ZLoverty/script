
bpass_mh
========

Convert *\*.nd2* file to image sequence and apply bandpass filter to each image. Save this image sequence in a subfolder under the same folder as the *\*.nd2* file with corresponding name as the *\*.nd2* file name. An additional histogram matching is performed so that the processed image looks similar to the original image.

.. rubric:: Syntax

.. code-block:: console

   python bpass_mh.py folder saveDir bpassLow bpassHigh

* folder = E:\Github\Python\Correlation\test_images\ixdiv_autocorr\raw
* saveDir = E:\Github\Python\Correlation\test_images\ixdiv_autocorr\bp_mh
* bpassLow = 3
* bpassHigh = 500

.. rubric:: Edit

* Jan 05, 2023 -- Adapt myimagelib import style.
