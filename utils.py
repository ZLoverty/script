import os
import numpy as np
from scipy import fft
from scipy.signal import medfilt2d, convolve2d, fftconvolve
from scipy.optimize import curve_fit
import pandas as pd
import psutil
from skimage import io
import time
import shutil
from nd2reader import ND2Reader
from myimagelib.myImageLib import to8bit, show_progress

class rawImage:
    """
    This class converts raw images to tif sequences. Throughout my research, I have mostly worked with two raw image formats: *\*.nd2* and *\*.raw*. Typically, they are tens of GB large, and are not feasible to load into the memory of a PC as a whole. Therefore, the starting point of my workflow is to convert raw images into sequences of *\*.tif* images. """

    def __init__(self, file_dir):
        """
        Construct rawImage object using the file directory.
        """
        self.file = file_dir
        self.type = os.path.splitext(self.file)[1]
        if self.type == ".nd2":
            with ND2Reader(self.file) as images:
                self.images = images
        elif self.type == ".raw":
            pass
        else:
            raise ValueError
    def __repr__(self):
        """Ideally, I can see some general informations about this image. For example, the number of frames and the frame size. Frame rate would also be helpful."""
        repr_str = "source file: {0}\nimage shape: {1}".format(self.file, self.images.shape)
        return repr_str
    def extract_tif(self):
        """Wrapper of all format-specific extractors."""
        file, ext = os.path.splitext(self.file)
        if ext == ".raw":
            self._extract_raw()
        elif ext == ".nd2":
            self._extract_nd2()
        else:
            raise ValueError("Unrecognized image format {}".format(ext))
    def _extract_raw(self, cutoff=None):
        """Extract tif sequence from *\*.raw* file.
        :param cutoff: number of images to extract

        .. rubric:: Edit

        * Dec 07, 2022: fix progress bar error.
        """
        # read info from info_file
        folder, file = os.path.split(self.file)
        info_file = os.path.join(folder, "RawImageInfo.txt")
        if os.path.exists(info_file):
            fps, h, w = self.read_raw_image_info(info_file)
        else:
            print("Info file missing!")

        # create output folders, skip if both folders exist
        save_folder = folder
        out_raw_folder = os.path.join(save_folder, 'raw')
        out_8_folder = os.path.join(save_folder, '8-bit')
        if os.path.exists(out_raw_folder) and os.path.exists(out_8_folder):
            print(time.asctime() + " // {} tif folders exists, skipping".format(self.file))
            return None
        if os.path.exists(out_raw_folder) == False:
            os.makedirs(out_raw_folder)
        if os.path.exists(out_8_folder) == False:
            os.makedirs(out_8_folder)

        # check disk
        if self._disk_capacity_check() == False:
            raise SystemError("No enough disk capacity!")

        # calculate buffer size based on available memory, use half of it
        file_size = os.path.getsize(self.file)
        avail_mem = psutil.virtual_memory().available
        unit_size = (h * w + 2) * 2 # the size of a single unit in bytes (frame# + image)
        buffer_size = ((avail_mem // 2) // unit_size) * unit_size # integer number of units
        remaining_size = file_size

        # print("Memory information:")
        # print("Available memory: {:.1f} G".format(avail_mem / 2 ** 30))
        # print("File size: {:.1f} G".format(file_size / 2 ** 30))
        # print("Buffer size: {:.1f} G".format(buffer_size / 2 ** 30))

        # read the binary files, in partitions if needed
        num = 0
        n_images = int(file_size // unit_size)
        t0 = time.monotonic()
        while remaining_size > 0:
            # load np.array from buffer
            if remaining_size > buffer_size:
                read_size = buffer_size
            else:
                read_size = remaining_size
            with open(self.file, "rb") as f:
                f.seek(-remaining_size, 2) # offset bin file reading, counting remaining size from EOF
                bytestring = f.read(read_size)
                a = np.frombuffer(bytestring, dtype=np.uint16)
            remaining_size -= read_size

            # manipulate the np.array
            assert(a.shape[0] % (h*w+2) == 0)
            num_images = a.shape[0] // (h*w+2)
            img_in_row = a.reshape(num_images, h*w+2)
            labels = img_in_row[:, :2] # not in use currently
            images = img_in_row[:, 2:]
            images_reshape = images.reshape(num_images, h, w)

            # save the image sequence
            for label, img in zip(labels, images_reshape):
                # num = label[0] + label[1] * 2 ** 16 + 1 # convert image label to uint32 to match the info in StagePosition.txt
                io.imsave(os.path.join(save_folder, 'raw', '{:05d}.tif'.format(num)), img, check_contrast=False)
                io.imsave(os.path.join(save_folder, '8-bit', '{:05d}.tif'.format(num)), to8bit(img), check_contrast=False)
                t1 = time.monotonic() - t0
                show_progress((num+1 / n_images), label="{:.1f} frame/s".format(num / t1))
                num += 1
                if cutoff is not None:
                    if num > cutoff:
                        return None

    def read_raw_image_info(self, info_file):
        """
        Read image info, such as fps and image dimensions, from *\*.RawImageInfo.txt*.
        Helper function of :py:func:`myImageLib.rawImage.extract_raw`.
        """
        with open(info_file, 'r') as f:
            a = f.read()
        fps, h, w = a.split('\n')[0:3]
        return int(fps), int(h), int(w)

    def _extract_nd2(self, raw=False):
        """
        Extract tif sequence from *\*.nd2* file.
        """
        # check disk
        if self._disk_capacity_check() == False:
            raise SystemError("No enough disk capacity!")

        folder, file = os.path.split(self.file)
        name, ext = os.path.splitext(file)
        saveDir8 = os.path.join(folder, name)
        if os.path.exists(saveDir8) == False:
            os.makedirs(saveDir8)
        t0 = time.monotonic()
        l = []
        with ND2Reader(self.file) as images:
            # Calculate global 1st and 99th percentile pixel values
            all_pixels = []
            for frame in images[::100]:
                all_pixels.extend(frame.flatten())
            global_min = np.percentile(all_pixels, 1)
            global_max = np.percentile(all_pixels, 99)

            n_images = len(images)
            for num, image in enumerate(images):
                image8 = (image - global_min) / (global_max - global_min) * 255
                image8 = np.clip(image8, 0, 255).astype(np.uint8)
                io.imsave(os.path.join(saveDir8, '%05d.tif' % num), image8, check_contrast=False)
                t1 = time.monotonic() - t0
                show_progress((num+1) / n_images, label="{:.1f} frame/s".format(num/t1))
         
    def _disk_capacity_check(self):
        """Check if the capacity of disk is larger than twice of the file size.
        Args:
        file -- directory of the (.nd2) file being converted
        Returns:
        flag -- bool, True if capacity is enough."""
        d = os.path.split(self.file)[0]
        fs = os.path.getsize(self.file) / 2**30
        ds = shutil.disk_usage(d)[2] / 2**30
        print("File size {0:.1f} GB, Disk size {1:.1f} GB".format(fs, ds))
        return ds > 2 * fs