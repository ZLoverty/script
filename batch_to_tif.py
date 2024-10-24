"""
Batch convert *\*.nd2* files to .tif images by calling ``to_tif.py``. The code assumes the following folder structure:

.. code-block:: console

   main_folder
   |-- day1
       |-- 00.nd2
   |-- day2
       |-- 01.nd2

.. rubric:: Syntax

.. code-block:: console

   python batch_to_tif.py main_folder

* main_folder -- the folder containing *\*.nd2* files.

.. rubric:: Test

.. code-block:: console

   python batch_to_tif.py test_images\batch_to_tif

.. rubric:: Edit

* Dec 14, 2021 -- (i) Use system argument as input main folder, (ii) Implement main log file, (iii) Better doc string.
* Jan 22, 2022 -- Remove the log file and print all the information to stdout. When using the code, use ``>>`` to save the screen message to a file. It's easier to locate the log file... This change should be applied to all the batch code.
* Jan 05, 2023 -- Adapt myimagelib import style.
* Mar 09, 2023 -- (i) add ``mode="r"`` for ``readdata``, which looks for target file recursively. (ii) use in other folders
"""

if __name__=="__main__":

    import os
    from myimagelib.myImageLib import readdata
    import sys
    import time
    import pandas as pd


    script_folder, script_name = os.path.split(sys.argv[0])
    main_folder = sys.argv[1]

    l0 = readdata(main_folder, "nd2", mode="r")
    l1 = readdata(main_folder, "raw", mode="r")
    l = pd.concat([l0, l1], axis=0)
    print(time.asctime())
    print("------------------------")
    print("Start batch_to_tif on {}".format(main_folder))
    print("The following raw images files will be converted to tif sequences:")
    
    for num, i in l.iterrows():
        print("\t{}".format(i.Dir))

    if len(l) > 0:
        for num, i in l.iterrows():
            out_folder = os.path.splitext(i.Dir)[0]
            if os.path.exists(out_folder) == False:
                print(time.asctime() + " // Converting {} to tif".format(i.Dir))
                cmd = "python {0} {1}".format(os.path.join(script_folder, "to_tif.py"), i.Dir)
                os.system(cmd)
            else:
                print(time.asctime() + " // {} tif folder exists already, skipping".format(i.Dir))
    else:
        print(time.asctime() + " // No nd2 file exists in the given folder.")
