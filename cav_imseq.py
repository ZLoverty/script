from corrLib import corrS, readdata
import numpy as np
import pandas as pd
import os
import time
import sys

"""
GENERAL
=======
Compute correlation length of velocity and velocity orientation.

Edit
====
Aug 06, 2020 - i) change corrI return value according to the change of corrI(), to speed up the code, ii) write parameters in log down sampling: instead of computing correlations for all frames, now only take 100 frames if the video is shorter than 100 frames, do the whole video
Dec 13, 2021 - i) Rewrite doc string. ii) Minor structural modification. 

USAGE
====
python cav_imseq.py input_folder output_folder
input_folder -- folder of PIV data
output_folder -- folder to save output
        
TEST
====
python cav_imseq.py test_images\cav_imseq test_images\cav_imseq\cav_imseq_results

LOG
===
Thu Feb 13 11:39:47 2020 // 900-901 calculated
Thu Feb 13 11:40:35 2020 // 902-903 calculated
"""

if __name__=="__main__":
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
                pivData = pd.read_csv(i.Dir)
                col = len(pivData.x.drop_duplicates())
                row = len(pivData.y.drop_duplicates())
                X = np.array(pivData.x).reshape((row, col))
                Y = np.array(pivData.y).reshape((row, col))
                U = np.array(pivData.u).reshape((row, col))
                V = np.array(pivData.v).reshape((row, col))
                X, Y, CA, CV = corrS(X, Y, U, V)        
                data = pd.DataFrame().assign(X=X.flatten(), Y=Y.flatten(), CA=CA.flatten(), CV=CV.flatten())
                # Save data
                data.to_csv(os.path.join(output_folder, i.Name+'.csv'), index=False)
                # Write log
                with open(os.path.join(output_folder, 'log.txt'), 'a') as f:
                    f.write(time.asctime() + ' // ' + i.Name + ' calculated\n')
    else:
        for num, i in l.iterrows():
            pivData = pd.read_csv(i.Dir)
            col = len(pivData.x.drop_duplicates())
            row = len(pivData.y.drop_duplicates())
            X = np.array(pivData.x).reshape((row, col))
            Y = np.array(pivData.y).reshape((row, col))
            U = np.array(pivData.u).reshape((row, col))
            V = np.array(pivData.v).reshape((row, col))
            X, Y, CA, CV = corrS(X, Y, U, V)        
            data = pd.DataFrame().assign(X=X.flatten(), Y=Y.flatten(), CA=CA.flatten(), CV=CV.flatten())
            # Save data
            data.to_csv(os.path.join(output_folder, i.Name+'.csv'), index=False)
            # Write log
            with open(os.path.join(output_folder, 'log.txt'), 'a') as f:
                f.write(time.asctime() + ' // ' + i.Name + ' calculated\n')



    
    
    
    