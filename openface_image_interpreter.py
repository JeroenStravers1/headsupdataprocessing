#!/usr/bin/python

import subprocess
import sys
import os

# TODO -- docstrings?
"""runs openface head pose extraction on all image subdirs in 'paying_attention' or 'not_paying_attention' dirs. Output is stored in the respective image dirs."""
_TARGET_DIR = 1

_OPENFACE_FEATURE_EXTRACTOR = './../OpenFace/bin/FeatureExtraction '
_OPENFACE_OUTPUT_ARGS = '-rigid -verbose -no2Dfp -no3Dfp -noMparams -noAUs -noGaze -fdir "'
_OPENFACE_PATH_TO_IMAGES = './' #./../ the root directory for relative pathing remains Desktop, apparently
_OPENFACE_OUTPUT = '" -of "'
_OPENFACE_OUTPUT_FILE_LOCATION = ''
_OPENFACE_ADDITIONAL_OUTPUT_ARGS = '.txt" -world_coord 0 -q'


def construct_openface_command(target_dir, image_dir):
    """constructs the commandline argument required to run the openface build"""
    call_openface_on_dir = _OPENFACE_FEATURE_EXTRACTOR + _OPENFACE_OUTPUT_ARGS + _OPENFACE_PATH_TO_IMAGES \
                           + target_dir + _OPENFACE_OUTPUT + _OPENFACE_OUTPUT_FILE_LOCATION + target_dir + "/" + image_dir \
                           + _OPENFACE_ADDITIONAL_OUTPUT_ARGS
    return call_openface_on_dir

if __name__ == "__main__":
    target_dir = sys.argv[_TARGET_DIR]
    for yes_no_dir in os.listdir(target_dir):
        if yes_no_dir != ".gitkeep":
            current_dir = target_dir + "/" + yes_no_dir
            for image_dir in os.listdir(current_dir):
                current_subdir = current_dir + "/" + image_dir
                command_run_openface = construct_openface_command(current_subdir, image_dir)
                print(command_run_openface)
                os.system(command_run_openface)           
                #subprocess.call(command_run_openface)

