
circulation_order_parameter
===========================

Compute circulation order parameter according to Wioland 2013. Technical details can be found in `my note <https://github.com/ZLoverty/DE/blob/main/Notes/Analysis_of_collective_motions_in_droplets.pdf>`_.

.. rubric:: Syntax

.. code-block:: console

   python circulation_order_parameter.py piv_folder out_folder x y

* piv_folder -- folder containing PIV data (.csv), file names indicate frame number
* out_folder -- order parameter data file (.csv), contain frame and OP
* x, y -- the center position

A folder of PIV files are used to generate a single order parameter data file.

.. rubric:: Test

.. code-block:: console

   python circulation_order_parameter.py test_images\circulation_order_parameter\piv test_images\circulation_order_parameter\order_parameter 259 227

.. rubric:: Edit

* Jan 02, 2021 -- Initial commit.
* Jan 05, 2023 -- Adapt myimagelib import style.
