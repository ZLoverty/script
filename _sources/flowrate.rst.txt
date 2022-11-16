
flowrate
========

This script compute "volumetric flow rate" in a channel from 2D PIV data. The unit of the flow rate will be px^2/s (it comes from a mean velocity, px/s, multiplied by a width, px).

.. rubric:: Syntax

.. code-block:: console

   python flowrate.py main_piv_folder flowrate_dir dt

* main_piv_folder -- the folder contains PIV of all crops (channels).
* flowrate_dir -- full directory of flow rate data file (.csv). The data will be ["crop-0", "crop-1", "crop-2", "t"].
* dt -- time interval between two PIV data (2/FPS)

.. rubric:: Edit

* Nov 03, 2022 -- Initial commit.
