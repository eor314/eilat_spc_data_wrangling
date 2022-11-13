# -*- coding: utf-8 -*-

import pandas as pd
import os
import glob
import argparse
from tqdm import tqdm
from datetime import datetime

__author__ = "Eric Orenstein"
__email__ = "eorenstein@mbari.org"
__doc__ = """

Convert the output database javascript file from Dual-Mag-Data to dataframe object for slicing and manipultation

@author: __author__
@status: __status__
@license: __license__
"""

def read_js(ptf):
    """
    Read a javascript database file from Dual-Mag-Data and return as a dataframe with image-id as index
    
    :param ptf: absolute path to javascript file
    :return out: pd.DataFrame
    """

    with open(ptf, 'r') as ff:
        tmp = list(ff)
        ff.close()

    # ignore the first two lines and strip newline control characters
    tmp = tmp[2::]
    tmp = [line.strip() for line in tmp]

    # split the long string into a dictionary of lists. Each entry represents a single image
    idx = [ix+1 for ix, val in enumerate(tmp) if val == '{']  # find index of open curly braket that indicates new entry
    js_dict = [tmp[ii:ii+10] for ii in idx]  # use that to make a list of lists

    out = []

    # use the dictionary to extract the absolute path to the file and the name of the data collection run
    for xx in js_dict:
        img_id = xx[7].split(': ')[1].split('/')[-1][:-2]
        
        # get the absolute path to the rawcolor file
        abs_path =  os.path.join(
            os.path.split(ptf)[0],
            'low_mag_cam_rois',
            xx[7].split(': ')[1].split('/')[1], 
            f'{os.path.splitext(img_id)[0]}_rawcolor.jpeg'
        )

        # save file paths and desired info from js
        out.append({
            'img_id': img_id, 
            'abspath_rawcolor': abs_path, 
            'aspect_ratio': float(xx[5].split(': ')[1][:-1]), 
            'major_axis_length': float(xx[6].split(': ')[1][:-1]),
            'frame_number': int(img_id.split('-')[3])
        })

    out = pd.DataFrame(out)
    out.set_index('img_id', inplace=True)

    return out

if __name__ == '__main__':

    # parse from command line
    parser = argparse.ArgumentParser(description='Read js database, output dataframe')
    parser.add_argument('data_ptf', metavar='data_ptf', help='path to processed SPC directory')
    parser.add_argument('out_dir', metavar='out_dir', help='path to output files')
    parser.add_argument(
        '--camera', metavar='camera', 
        default='low_mag_cam', choices=['low_mag_cam', 'high_mag_cam']
    )

    args = parser.parse_args()

    # check if ptf is directory or the javascript
    if os.path.isdir(args.data_ptf):
        ptfs = glob.glob(os.path.join(args.data_ptf, 'processed*', 'webapp', f'{args.camera}_rois.js'))
    else:
        ptfs = [args.data_ptf]

    # create the output directory if needed
    out_dir = args.out_dir
    if not os.path.exists(out_dir):
        os.path.mkdir(out_dir)

    # convert to dataframe and save
    for ptf in tqdm(ptfs, desc='processing DBs'):

        # extract
        tmp = read_js(ptf)

        # get the parent directory
        outname = [line for line in ptf.split('\\') if 'processed-' in line][0]
        outname = os.path.join(out_dir, f'{outname}-{args.camera}.csv')

        tmp.to_csv(os.path.join(out_dir, outname))
