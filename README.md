# script
 Useful scripts for batch image processing

## To-do list
- batch_gen_preview has directory bugs
```
generating preview for /media/zhengyang/XinQ/DE/12062021/19.nd2
/media/zhengyang/XinQ/DE/12062021/19.nd2 -> /media/zhengyang/XinQ/DE/preview12062021/19.tif
Generating preview for /media/zhengyang/XinQ/DE/12092021/20.nd2
/media/zhengyang/XinQ/DE/12092021/20.nd2 -> /media/zhengyang/XinQ/DE/preview12092021/20.tif
```
- orientational order calculation
- Solve the memory issue of reading large .raw file (np.fromfile)
- Optimal PIV box size need to be determined.
## Done list
- All the batch script need to write a log file, recording the progress. For example, when batch_to_tif.py finds tifs for some files exists already, it should state explicitly in the log file that these files are skipped.
- modify `gen_preview.py`: work on single .nd2 files
- `batch_gen_preview.py`
