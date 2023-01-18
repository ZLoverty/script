
bpass
=====

Convert *\*.nd2* file to image sequence and apply bandpass filter to each image. Save this image sequence in a subfolder under the same folder as the *\*.nd2* file with corresponding name as the *\*.nd2* file name.


.. rubric:: Syntax

.. code-block:: console

   python bpass.py nd2Dir bpassLow bpassHigh

* nd2Dir -- full directory of *\*.nd2* file
* bpassLow -- lower bound of wavelength
* bpassHigh -- upper bound of wavelength

.. rubric:: Edit

* Nov 15, 2022 -- Modify docstring.
* Jan 05, 2023 -- Adapt myimagelib import style.
