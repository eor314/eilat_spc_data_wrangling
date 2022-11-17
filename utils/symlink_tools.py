# -*- coding: utf-8 -*-

import os
import glob
import argparse
from datetime import datetime
from tqdm import tqdm
from shutil import copyfile

__author__ = "Eric Orenstein"
__email__ = "eorenstein@mbari.org"
__doc__ = """

Utilities for symlinking images to new directories. Note: these scripts need to be run at admin on Windows. 

@author: __author__
@status: __status__
@license: __license__
"""


def symlink_from_file(inpath, outpath, fmt):
    """
    symlink all images from a directory to the output path

    :param inpath: absolute path to image directory
    :param outpath: absolute path to output directory
    :param fmt: what file format to search for
    :return :
    """
    imgs = glob.glob(os.path.join(inpath, f'*.{fmt}'))

    for img in tqdm(imgs, desc='symlinking...'):
        os.symlink(img, os.path.join(outpath, os.path.basename(img)))


def symlink_from_list(imgs, outpath):
    """
    symlink all images from a list to the output path

    :param imgs: image list
    :param outpath: absolute path to output directory
    :return :
    """

    imgs = [line.strip() for line in imgs]

    for img in tqdm(imgs, desc='symlinking...'):
        os.symlink(img, os.path.join(outpath, os.path.basename(img)))

    
def copy_from_list(imgs, outpath):
    """
    copy all images from a list to the output path

    :param imgs: image list
    :param outpath: absolute path to output directory
    :return :
    """

    imgs = [line.strip() for line in imgs]

    for img in tqdm(imgs, desc='symlinking...'):
        copyfile(img, os.path.join(outpath, os.path.basename(img)))

if __name__=="__main__":

    parser = argparse.ArgumentParser(description='Command line tool to symlink a list of images to a directory')
    parser.add_argument('ptf', metavar='ptf', help='path to images to symlink')
    parser.add_argument('outptf', metavar='outptf', help='where to make symlink')
    parser.add_argument('--format', default='jpeg', metavar='format', choices=['jpg', 'jpeg', 'png', 'tiff'],
                        help='format of file to symlink')

    args = parser.parse_args()

    if os.path.isdir(args.ptf):
        # if ptf is a directory
        if os.path.exists(args.ptf) and os.path.exists(args.outptf):
            symlink_from_file(args.ptf, args.outptf, args.format)
        else:
            print('Check file paths')
    
    elif os.path.isfile(args.ptf):
        # if ptf is a file
        with open(args.ptf, 'r') as ff:
            imglists = list(ff)
            ff.close()
        symlink_from_list(args.ptf, args.outptf)
