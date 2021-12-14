# script
 Useful scripts for batch image processing

## To-do list
- Optimal PIV box size need to be determined.
- orientational order calculation
- Solve the memory issue of reading large .raw file (np.fromfile)

## Done list
- All the batch script need to write a log file, recording the progress. For example, when batch_to_tif.py finds tifs for some files exists already, it should state explicitly in the log file that these files are skipped.
- modify `gen_preview.py`: work on single .nd2 files
- `batch_gen_preview.py`
