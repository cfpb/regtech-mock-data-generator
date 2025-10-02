# This will generate a complete HMDA test file given proper config files

import logging
import os
import argparse
import random
# import old_utils
import yaml
import pandas as pd

from mock_data import MockDataset
from mock_data import utils

parser = argparse.ArgumentParser('datagen')
parser.add_argument('-f', '--yaml_file')
parser.add_argument('-ts', '--transmittal_sheet')
parser.add_argument('-op', '--output_filepath')
parser.add_argument('-of', '--output_filename')
parser.add_argument('-n', '--nrows', type=int, default=100)
parser.add_argument('-v', '--verbose', action='store_true')
args = parser.parse_args()

loglevel = logging.DEBUG if args.verbose else logging.INFO
logging.basicConfig(level=loglevel)

# set the working directory to the folder containing this script
os.chdir(os.path.dirname(__file__))

random.seed()

mock = MockDataset.read_yaml_spec(args.yaml_file)

mock_df = mock.generate_mock_data(args.nrows)

# Create and append check digit for the ULI field using the utils.check_digit_gen() tool
mock_df["uli"] = mock_df["uli"] + mock_df["uli"].apply(
    lambda x: utils.check_digit_gen(ULI=x)
)

# Read in the transmittal sheet
with open(args.transmittal_sheet, "r") as file:
    ts = yaml.safe_load(file)
ts_df = pd.DataFrame(ts)

# Write the file out as a .txt following HMDA file format - TS as first row, LAR as subsequent rows
utils.write_file(
    outpath=args.output_filepath, ts_input=ts_df, lar_input=mock_df
)
