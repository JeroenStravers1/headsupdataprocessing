#!/usr/bin/python

import sys
import os
from head_pose_output_parser import HeadPoseOutputParser


class ArffGenerator(object):

    # manually determine the paths, easier than commandline args
    #_REL_PATH_TO_OPENFACE_OUTPUT_MAIN_DIR = "../attentionscorecalculator/head_pose_extraction/training_data"
    _REL_PATH_TO_OPENFACE_OUTPUT_MAIN_DIR = "C:/Users/Administrator/Desktop/hudc_processing/attentionscorecalculator/head_pose_extraction/training_data"#"../attentionscorecalculator/head_pose_extraction/training_data"
    _REL_PATH_TO_ARFF_DIR = "C:/Users/Administrator/Desktop/hudc_processing/attentionscorecalculator/head_pose_extraction/extracted_poses"#"../attentionscorecalculator/head_pose_extraction/extracted_poses"
    #_REL_PATH_TO_ARFF_DIR = "../attentionscorecalculator/head_pose_extraction/extracted_poses"

    _CLASS_PAYING_ATTENTION = "paying_attention"
    _CLASS_NOT_PAYING_ATTENTION = "not_paying_attention"

    _ARFF_FILE_RELATION = "@RELATION attention"
    _ARFF_FILE_RX = "@ATTRIBUTE 'rx'	REAL"
    _ARFF_FILE_RY = "@ATTRIBUTE 'ry'	REAL"
    _ARFF_FILE_RZ = "@ATTRIBUTE 'rz'	REAL"
    _ARFF_FILE_CLASS = "@ATTRIBUTE 'class' 	{'paying_attention','not_paying_attention'}"
    _ARFF_FILE_DATA = "@DATA"
    _ARFF_FILE_NAME = "/original.arff"
    _OUTPUT_FILE_EXTENSION = ".txt"

    def __init__(self):
        #self._path_to_main_dir = path_to_main_image_folder
        self._class_paying_attention = 0
        self._class_not_paying_attention = 0
        self._instances_paying_attention = list()
        self._instances_not_paying_attention = list()

    def generate_arff_from_openface_output(self):
        """main caller function"""
        self._arff_file_with_path = self._REL_PATH_TO_ARFF_DIR + self._ARFF_FILE_NAME
        self._construct_arff_file(self._REL_PATH_TO_ARFF_DIR)
        self._combine_all_output()

    def _construct_arff_file(self, output_path):
        """initialises the .arff file with metadata"""
        arff_file_location = output_path + self._ARFF_FILE_NAME
        with open(self._arff_file_with_path, 'w+') as arff_file:
            arff_metadata = self._generate_arff_metadata()
            arff_file.write(arff_metadata)

    def _generate_arff_metadata(self):
        """generates the metadata for the original.arff file"""
        arff_metadata = "%s\n\n%s\n%s\n%s\n%s\n\n%s\n" \
                    % (self._ARFF_FILE_RELATION, self._ARFF_FILE_RX, self._ARFF_FILE_RY, self._ARFF_FILE_RZ, self._ARFF_FILE_CLASS, self._ARFF_FILE_DATA)
        return arff_metadata

    def _combine_all_output(self):
        """writes all output in correct format to arff file"""
        output_parser = HeadPoseOutputParser()
        image_counter = 0
        for attention_yes_no_dir in os.listdir(self._REL_PATH_TO_OPENFACE_OUTPUT_MAIN_DIR):
            if attention_yes_no_dir != ".gitkeep":
                current_dir = self._REL_PATH_TO_OPENFACE_OUTPUT_MAIN_DIR + "/" + attention_yes_no_dir
                for image_dir in os.listdir(current_dir):
                    image_counter += 1
                    outputfile_path = current_dir + "/" + image_dir + "/" + image_dir + self._OUTPUT_FILE_EXTENSION
                    arff_data_line = output_parser.extract_valid_head_poses_from_output_file(outputfile_path, \
                                                                                             image_counter)
                    self._store_dataline_in_class_list(arff_data_line)
                    print (outputfile_path)
                    print (arff_data_line + "!!!")

        self._write_arff_datalines()

    def _store_dataline_in_class_list(self, dataline):
        """store all arff lines in a list per class"""
        if self._CLASS_NOT_PAYING_ATTENTION in dataline:
            self._instances_not_paying_attention.append(dataline)
        else:
            self._instances_paying_attention.append(dataline)

    def _write_arff_datalines(self):


        balanced_attention, balanced_no_attention = self._balance_datalines()
        with open(self._arff_file_with_path, 'a') as arff_file:
            for data_attention in balanced_attention:
                arff_file.write(data_attention)
            for data_no_attention in balanced_no_attention:
                arff_file.write(data_no_attention)

    def _balance_datalines(self):
        balanced_attention = self._instances_paying_attention
        balanced_no_attention = self._instances_not_paying_attention
        instances_no_attention = len(balanced_no_attention)
        instances_attention = len(balanced_attention)
        if instances_attention > instances_no_attention:
            balanced_attention = balanced_attention[:instances_no_attention]
        elif instances_no_attention > instances_attention:
            balanced_no_attention = balanced_no_attention[:instances_attention]
        return balanced_attention, balanced_no_attention

# with open(self._arff_file_with_path, 'a') as arff_file:
#

if __name__ == "__main__":
    
    arff_generator = ArffGenerator()
    arff_generator.generate_arff_from_openface_output()
