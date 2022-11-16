import sys
import os
import numpy as np
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import glob
import cv2


def make_confmat(y_true, y_pred, acc, mat_size=None, labels=None, outpath=None):
    """
    takes classifier output and labels to generate a confusion matrix
    :param labels: list of true numeric labels
    :param dec: list of labels from classifiers
    :param acc: accuracy [float]
    :param mat_size: size for plot in inches (assumed square dims) [int]
    :param outpath: file path for saving [str]
    """
    # compute the confusion matrix from sklearn
    conf = confusion_matrix(y_true, y_pred)

    # Normalize by support
    conf = conf / conf.sum(axis=1)[:, np.newaxis]

    # create the figure output
    fig, ax = plt.subplots()
    ax.set_aspect(1)
    aximg = ax.imshow(conf, cmap="Blues", interpolation='nearest')
    plt.title('Object accuracy: %.3f' % acc)
    fig.colorbar(aximg)
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

    if labels is not None:
        plt.xticks(np.arange(len(labels)), labels, rotation=90)
        plt.yticks(np.arange(len(labels)), labels)

    if mat_size is not None:
        fig.set_size_inches(mat_size, mat_size)

    # turn off this block of comments to remove numeric ticks
    """
    plt.tick_params(
    axis = 'both',
    which = 'both',
    bottom = 'off',
    top = 'off',
    labelbottom = 'off',
    right = 'off',
    left = 'off',
    labelleft = 'off')
    """

    # if a file for saving is defined, save it
    if outpath is not None:
        plt.savefig(outpath, dpi=120)

    # otherwise, display it
    else:
        plt.show()