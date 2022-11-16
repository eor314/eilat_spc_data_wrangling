# eilat_spc_data_wrangling
## 13/11/22

A collection of python notebooks to examine annotated data produced by researchers at the Interuniversity Institute for Marine Sciences in Eilat (IUI). Most of thse are one-off scripts to visualize various aspeccts of the dataset. 

- `find_raw_paths.ipynb`: Many of the annotations were saved as masked images. This script recovers the absolute path the original processed output of the Dual-Mag-SPC. 
- `filter_size.ipynb`: Filters the annotated data by size and symlinks the images to a directory for model training.
- `filter_eval_images.pynb`: Selects a subset of frames and filters by size from all ROIs collected in a single run of the SPC. The desired subset is symlinked to a directory for model inference and evaluation. 
- `slice_dice_061122`: First through annotated data.
- `slice_dice_101122`: Second pass through annotated data. This set of plots reflects the training data after the unmasked ROIs were recovered and duplicate images were removed. 
