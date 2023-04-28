"""
Compute correlation length of velocity and velocity orientation.


.. rubric:: Syntax

.. code-block:: console

   python cav_imseq.py input_folder output_folder

* input_folder -- folder of PIV data
* output_folder -- folder to save output

.. rubric:: Test

.. code-block:: console

   python spatial_correlation.py test_images\batch_spatial_correlation\piv_folder\00 test_images\batch_spatial_correlation\spatial_correlation\00

.. rubric:: Edit

* Aug 06, 2020 -- (i) change corrI return value according to the change of corrI(), to speed up the code, (ii) write parameters in log down sampling: instead of computing correlations for all frames, now only take 100 frames if the video is shorter than 100 frames, do the whole video
* Dec 13, 2021 -- (i) Rewrite doc string. (ii) Minor structural modification.
* Dec 15, 2021 -- (i) Rename to `spatial_correlation.py`, (ii) modify test script, (iii) replace PIV data loading snippet with `read_piv` function.
* Jan 05, 2023 -- Adapt myimagelib import style.
* Feb 08, 2023 -- Rewrite in function wrapper form, to make autodoc work properly. (autodoc import the script and execute it, so anything outside ``if __name__=="__main__"`` will be executed, causing problems)
"""

if __name__=="__main__":

    from myimagelib.corrLib import corrS
    from myimagelib.myImageLib import readdata
    import numpy as np
    import pandas as pd
    import os
    import time
    import sys
    import pdb
    from myimagelib.pivLib import read_piv

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]

    # check output dir existence
    if os.path.exists(output_folder) == 0:
        os.makedirs(output_folder)
    with open(os.path.join(output_folder, 'log.txt'), 'w') as f:
        f.write('Input folder: ' + str(input_folder) + '\n')
        f.write('Ouput folder: ' + str(output_folder) + '\n')

    l = readdata(input_folder, "csv")
    num_frames = len(l)
    num_sample = 100 # can modify in the future
    if num_sample <= num_frames:
        for num, i in l.iterrows():
            if num % int(num_frames / num_sample) == 0:
                x, y, u, v = read_piv(i.Dir)
                X, Y, CA, CV = corrS(x, y, u, v)
                data = pd.DataFrame().assign(X=X.flatten(), Y=Y.flatten(), CA=CA.flatten(), CV=CV.flatten())
                # Save data
                data.to_csv(os.path.join(output_folder, i.Name+'.csv'), index=False)
                # Write log
                with open(os.path.join(output_folder, 'log.txt'), 'a') as f:
                    f.write(time.asctime() + ' // ' + i.Name + ' calculated\n')
    else:
        for num, i in l.iterrows():
            x, y, u, v = read_piv(i.Dir)
            X, Y, CA, CV = corrS(x, y, u, v)
            data = pd.DataFrame().assign(X=X.flatten(), Y=Y.flatten(), CA=CA.flatten(), CV=CV.flatten())
            # Save data
            data.to_csv(os.path.join(output_folder, i.Name+'.csv'), index=False)
            # Write log
            with open(os.path.join(output_folder, 'log.txt'), 'a') as f:
                f.write(time.asctime() + ' // ' + i.Name + ' calculated\n')
