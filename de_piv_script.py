"""
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
* Feb 08, 2023 -- Rewrite in function wrapper form, to make autodoc work properly. (autodoc import the script and execute it, so anything outside ``if __name__=="__main__"`` will be executed, causing problems)
"""

if __name__ == "__main__":

    from myimagelib.myImageLib import readdata
    import sys
    import os
    import time
    import pandas as pd

    folder = sys.argv[1]

    log = pd.read_csv(os.path.join(folder, "log.csv"))

    with open(os.path.join(folder, "tmp"), "w") as f:
        pass

    for num, i in log.iterrows():
        nd2Dir = os.path.join(folder, "{:03d}.nd2".format(i["DE#"]))
        if os.path.exists(nd2Dir) == False:
            with open(os.path.join(folder, "tmp"), "a") as f:
                f.write("{:03d} is missing\n".format(i["DE#"]))
            continue
        winsize = int(5 / i.MPP)
        dt = 1 / i.FPS
        piv_folder = os.path.join(folder, "PIV", "{:03d}".format(i["DE#"]))
        os.system("python PIV.py \"{0}\" {1} {2} \"{3}\"".format(nd2Dir, winsize, dt, piv_folder))
        mask_dir = os.path.join(folder, "mask", "{:03d}.tif".format(i["DE#"]))
        os.system("python apply_mask.py \"{0}\" \"{1}\"".format(piv_folder, mask_dir))
        os.system("python wrap_piv.py \"{}\"".format(piv_folder))