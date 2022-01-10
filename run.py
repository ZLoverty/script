# This script is not purpose fixed.
# Review every time before running.
#
import os
from corrLib import readdata

if __name__=="__main__":
    folder = "/media/zhengyang/XinQ/DE/01052022"
    sfL = next(os.walk(folder))[1]
    cmd_list = []
    for sf in sfL:
        image_folder = os.path.join(folder, sf, "raw")
        if os.path.exists(image_folder):
            mask_dir = os.path.join(folder, "mask", sf + ".tif")
            if os.path.exists(mask_dir):
                save_folder = os.path.join(folder, "piv_drop", sf)
                if os.path.exists(save_folder) == False:
                    os.makedirs(save_folder)
                    cmd_list.append("python piv_drop.py {0} {1} 20 10 0.02 {2}".format(image_folder, save_folder, mask_dir))
            else:
                print("Mask not found at {}, skipping".format(mask_dir))
        else:
            print("Raw folder not found, skipping {}".format(sf))
    folder = "/media/zhengyang/XinQ/DE/01062022"
    sfL = next(os.walk(folder))[1]
    for sf in sfL:
        image_folder = os.path.join(folder, sf, "raw")
        if os.path.exists(image_folder):
            mask_dir = os.path.join(folder, "mask", sf + ".tif")
            if os.path.exists(mask_dir):
                save_folder = os.path.join(folder, "piv_drop", sf)
                if os.path.exists(save_folder) == False:
                    os.makedirs(save_folder)
                    cmd_list.append("python piv_drop.py {0} {1} 20 10 0.02 {2}".format(image_folder, save_folder, mask_dir))
            else:
                print("Mask not found at {}, skipping".format(mask_dir))
        else:
            print("Raw folder not found, skipping {}".format(sf))

    cmd = " && ".join(cmd_list)
    os.system(cmd)

