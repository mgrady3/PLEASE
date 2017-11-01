"""PLEASE - The Python Low-energy Electron Analysis SuitE.

Author: Maxwell Grady
Affiliation: University of New Hampshire Department of Physics Pohl group
Version 1.0.0
Date: October, 2017

config_test_data.py

This file provides a script that will automatically adjust the data path setting
in the four YAML configuration files for the test data sets provided with the
PLEASE project.

Note: if the directories containing the test data have been changed from the structure
initially set in the project directory, then this script will fail.
"""

import glob
import os
import sys
import yaml


if not os.path.abspath(".").split(os.sep)[-1] == "TestData":
    print("Error: config_test_data.py must be run from the TestData directory.")
    sys.exit()

"""
Dir Structure:

TestData
|
|
\___ActualDatasets
    |
    |
    \___LEED
        |
        |
        \___Data
    |
    |
    \___LEEM
        |
        |
        \___Data
|
|
\___TestDataSets
    |
    |
    \___LEEDTestData
        |
        |
        \___dat2
    |
    |
    \___LEEMTestData
        |
        |
        \___dat
"""


cd = os.path.abspath(".")  # full path to directory containig this script
actual_data_dir = os.path.join(cd, "ActualDatasets")
test_data_dir = os.path.join(cd, "TestDataSets")

actual_LEED = os.path.join(actual_data_dir, "LEED")
actual_LEEM = os.path.join(actual_data_dir, "LEEM")
test_LEED = os.path.join(test_data_dir, "LEEDTestData")
test_LEEM = os.path.join(test_data_dir, "LEEMTestData")

actual_LEED_data_dir = os.path.join(actual_data_dir, "LEED", "Data")
actual_LEEM_data_dir = os.path.join(actual_data_dir, "LEEM", "Data")
test_LEED_data_dir = os.path.join(test_data_dir, "LEEDTestData", "dat2")
test_LEEM_data_dir = os.path.join(test_data_dir, "LEEMTestData", "dat")

top_dirs = [actual_LEED, actual_LEEM, test_LEED, test_LEEM]
data_dirs = [actual_LEED_data_dir, actual_LEEM_data_dir, test_LEED_data_dir, test_LEEM_data_dir]

# for each Experiment.yaml file
#    replace the Data Path setting with the appropriate local data dir from the list data_dirs
#    overwrite Experiment.yaml with new settings

for idx, path in enumerate(top_dirs):
    try:
        settings_file = glob.glob(os.path.join(path, "Experiment.yaml"))[0]
    except IndexError:
        print("Error: No file named Experiment.yaml found in path {}".format(path))
        sys.exit()

    print("Reading settings from file {} ...".format(settings_file))
    with open(settings_file, 'r') as f:
        lines = f.readlines()

    # search for correct setting to adjust
    print("Searching for data path setting to adjust ...")
    for line_index, line in enumerate(lines):
        if "Data Path:" in line:
            # print("Found path to adjust at index {}: {}".format(line_index, line))
            # print("Found path to adjust in file {}".format(settings_file))
            line_num = line_index
            break
    lines[line_num] = "    Data Path:  {}".format(data_dirs[idx]) + os.linesep
    print("Overwriting settings file with new path settings ...")
    print(lines[line_num])
    with open(settings_file, 'w') as f:
        for line in lines:
            f.write(line)
    print("Successfully wrote settings to file."+os.linesep)
sys.exit()
