
small_imseq
===========

Concentration has always been derived from the bright field images. While images are typically 1280*1080, the data we use are always coarse-grained down to 50*42. Although the down sizing step takes only several milliseconds, repeating the process over and over for hundreds of thousands of times (all images) takes a lot of time. Thus, I decide to convert the image sequences to the coarse-grained version and save them as numpy binary data. In this way, the 3000 frame video will be down sized to 3000*50*42 float16 numbers, which in total is 6M instead of the 4.64G. By saving this down sized data, the data also gets more portable because of the small size, while all the useful information is retained.


.. rubric:: Syntax

.. code-block:: console

   python small_imseq.py img_folder out_folder wsize step

* img_folder -- folder of image sequence
* out_folder -- folder to save the numpy array
* wsize, step --  window size (int, assuming square) and step, parameter of :py:func:`corrLib.divide_windows()`

.. note::

   The array will be saved as file 'stack.npy'

.. rubric:: Edit

* Sep 20, 2020 -- Initial commit.
