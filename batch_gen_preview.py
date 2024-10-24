"""
Batch generate preview images from nd2 files. The code assumes the following folder structure:

.. code-block:: console

   main_folder
   |-- day1
       |-- 00.nd2
   |-- day2
       |-- 01.nd2

.. rubric:: Syntax

.. code-block:: console

   python batch_gen_preview.py main_folder

* main_folder -- any folder / parent folder that contains *\*.nd2* images.

.. rubric:: Test

.. code-block:: console

   python batch_gen_preview.py test_images\batch_to_tif

.. rubric:: Edit

* Dec 14, 2021 --
    1. Use system argument as input main folder.
    2. Implement main log file. iii) Better doc string.
* Dec 15, 2021 -- Remove the last os.sep of main_folder, so that it is ok to pass main_folder with "\" (win) or "/" (linux) at the end.
* Jan 05, 2023 -- Adapt myimagelib import style.
* Feb 02, 2023 -- Fix space in dir bug.
* Feb 08, 2023 -- Rewrite in function wrapper form, to make autodoc work properly. (autodoc import the script and execute it, so anything outside ``if __name__=="__main__"`` will be executed, causing problems)
"""

if __name__ == "__main__":
    
    import os
    from myimagelib.myImageLib import readdata
    import sys
    import time


    main_folder = sys.argv[1].rstrip(os.sep)
    out_folder = os.path.join(main_folder, "preview")
    if os.path.exists(out_folder) == False:
        os.makedirs(out_folder)

    l = readdata(main_folder, 'nd2', mode="r")

    print(time.asctime())
    print("------------------------")
    print("Run batch_gen_preview on {}".format(main_folder))
    print("Results will be saved in {}".format(out_folder))
    print("The following files will be processed:")
    for num, i in l.iterrows():
        print("\t{}".format(i.Dir))
    print("------------------------")

    if len(l) > 0:
        for num, i in l.iterrows():
            out_file = i.Dir.replace(main_folder, out_folder).replace(".nd2", ".tif")
            if os.path.exists(out_file) == False:
                print("Generating preview for {}".format(i.Dir))
                cmd = "python gen_preview.py \"{0}\"".format(i.Dir)
                os.system(cmd)
            else:
                print("{} exists already, skipping".format(out_file))
    else:
        print(time.asctime() + " \\ No nd2 file exists in the given folder.")
