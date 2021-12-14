# script
 Useful scripts for batch image processing

## To-do list
- All the batch script need to write a log file, recording the progress. For example, when batch_to_tif.py finds tifs for some files exists already, it should state explicitly in the log file that these files are skipped.
- Optimal PIV box size need to be determined.
- Reorganize test_images: smaller, more similar to real folder structure (with different folders intertwining together)
- `batch_gen_preview.py`
- orientational order calculation
- Solve the memory issue of reading large .raw file (np.fromfile)
- modify `gen_preview.py`: work on single .nd2 files

## Done list
