"""
Batch velocity autocorrelation computation.

.. rubric:: Syntax

.. code-block:: console

   python batch_mean_velocity.py main_piv_foler

* main_piv_folder -- the folder containing many folders of PIV data. `piv_drop` for example.

.. rubric:: Test

.. code-block:: console

   python batch_velocity_autocorr.py test_images\batch_spatial_correlation\piv_folder

.. rubric:: Edit

* Feb 21, 2022 -- Initial commit.
* Jan 05, 2023 -- Adapt myimagelib import style.
* Feb 08, 2023 -- Rewrite in function wrapper form, to make autodoc work properly. (autodoc import the script and execute it, so anything outside ``if __name__=="__main__"`` will be executed, causing problems)
"""

if __name__ == "__main__":

    import os
    import sys
    import time
    from myimagelib.myImageLib import readdata

    main_piv_folder = sys.argv[1].rstrip(os.sep)
    parent_folder = os.path.split(main_piv_folder)[0]
    main_save_folder = os.path.join(parent_folder, "velocity_autocorr")
    sfL = next(os.walk(main_piv_folder))[1]
    if os.path.exists(main_save_folder) == False:
        os.makedirs(main_save_folder)

    print(time.asctime())
    print("------------------------")
    print("Run batch_velocity_autocorr on {}".format(main_piv_folder))
    print("Results will be saved in {}".format(main_save_folder))
    print("The following files will be processed:")
    for sf in sfL:
        print("\t{}".format(os.path.join(main_piv_folder, sf)))
    print("------------------------")

    for sf in sfL:
        piv_folder = os.path.join(main_piv_folder, sf)
        print(time.asctime() + " Computing velocity autocorrelation of {}".format(os.path.join(main_piv_folder, sf)))
        os.system("python velocity_autocorr.py {0} {1}".format(piv_folder, main_save_folder))
