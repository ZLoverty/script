
de_piv_script
=============
A script to run PIV on all the nd2 files in a given folder. In addition, it applys masks to the raw PIV data and convert separated text files into more compact .mat files. The folder structure is assumed to be:

.. code-block:: console

   |-- folder
       |-- 000.nd2
       |-- 001.nd2
       |-- ...
       |-- PIV (results)
           |-- 000.mat
           |-- 001.mat
           |-- ...

.. rubric:: Syntax

.. code-block:: console
   
   python de_piv_script.py folder

* folder: a folder that contains nd2 files.

.. rubric:: Edit

* Jan 05, 2023 -- Initial commit.
