#!/usr/bin/python

class HeadPoseOutputParser(object):
    """OpenFace outputs head poses and other data as a non-formatted csv. This class splits the file into individual
    elements, and extracts the indices of elements required for further analysis."""
    _SUCCESS = "success"
    _RX = "pose_Rx"
    _RY = "pose_Ry"
    _RZ = "pose_Rz1"
    _DELIMITER = ", "
    _INDEX_INCREMENT = 1
    _PAYING_ATTENTION = "paying_attention"
    _NOT_PAYING_ATTENTION = "not_paying_attention"

    def __init__(self):
        self._index_success = 0
        self._index_rx = 0
        self._index_ry = 0
        self._index_rz = 0
        self._line_length = 0
        self._split_output_file = list()
        self._arff_dataline = ""

    def extract_valid_head_poses_from_output_file(self, file_location, arff_file_line_number):
        """opens the entire file in a single line (openface returns an unformatted csv as output (no \n))
        returns the output file split item by item, and the indices required to read it."""
        with open(file_location, "r") as estimated_head_poses:
            head_poses_output_as_single_line = estimated_head_poses.read()
            self._parse_unformatted_head_poses(head_poses_output_as_single_line, arff_file_line_number, file_location)
        return self._arff_dataline

    def _parse_unformatted_head_poses(self, poses_output, arff_file_line_number, file_location):
        """"splits the output file by ', ' -> leaving only the values"""
        self._split_output_file = poses_output.split(self._DELIMITER)
        self._extract_index_of_success_rx_ry_rz_values()
        self._extract_arff_dataline_from_indices(arff_file_line_number, file_location)

    def _extract_index_of_success_rx_ry_rz_values(self):
        """extract indices of success, rx, ry, rz and the length of the header (where the values start)"""
        current_index = 0
        for item in self._split_output_file:
            if item == self._SUCCESS:
                self._index_success = current_index
            elif item == self._RX:
                self._index_rx = current_index
            elif item == self._RY:
                self._index_ry = current_index
            elif item == self._RZ:
                self._index_rz = current_index
            elif self._is_numeric(item):
                self._line_length = current_index
                if not self._all_indices_extracted():
                    # TODO - log & throw error parsing required indices!
                    pass
                break
            current_index += self._INDEX_INCREMENT

    def _is_numeric(self, item_to_check):
        """checks if the item can be converted to float (should be faster than regex or similar methods"""
        try:
            float(item_to_check)
            return True
        except ValueError:
            return False

    def _all_indices_extracted(self):
        """check if all required indices have been successfully extracted from the output file"""
        if all(index > 0 for index in (self._index_success, self._index_rx, \
                                       self._index_ry, self._index_rz, self._line_length)):
            return True
        return False

    def _extract_arff_dataline_from_indices(self, arff_file_line_number, file_location):
        """generates a comma-separated string containing the required variables"""
        self._arff_dataline = str(arff_file_line_number) + ","
        self._arff_dataline += self._split_output_file[self._on_first_data_line(self._index_rx)] + ","
        self._arff_dataline += self._split_output_file[self._on_first_data_line(self._index_ry)] + ","
        self._arff_dataline += self._split_output_file[self._on_first_data_line(self._index_rz)] + ","
        self._arff_dataline += self._get_attribute_class_for_file(file_location) + "\n"

    def _on_first_data_line(self, variable):
        """increments an index to skip to the first dataline"""
        return variable + self._line_length -1

    def _get_attribute_class_for_file(self, filename):
        if self._NOT_PAYING_ATTENTION in filename:
            return self._NOT_PAYING_ATTENTION
        return self._PAYING_ATTENTION

if __name__ == "__main__":
    bob = HeadPoseOutputParser()
    bob.extract_valid_head_poses_from_output_file("test")


