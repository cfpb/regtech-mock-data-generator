import logging
import os
import argparse

from custom_backends import MultipleResponse

from mock_data import MockDataset

logging.basicConfig(level=logging.DEBUG)

parser = argparse.ArgumentParser('datagen')
parser.add_argument('-n', '--nrows', type=int, default=10)
args = parser.parse_args()

# set the working directory to the folder containing this script
os.chdir(os.path.dirname(__file__))

# register the MultipleResponse backend
MockDataset.register_backend(MultipleResponse)

mock = MockDataset.read_yaml_spec("sbl.yaml")

mock_df = mock.generate_mock_data(args.nrows)

mock_df.to_csv("fake_data.csv", index=False)
