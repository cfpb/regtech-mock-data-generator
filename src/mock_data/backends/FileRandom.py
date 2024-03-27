
from importlib.resources import files
import os
import pandas as pd
import random
from typing import Iterable, List

from mock_data.backends import AbstractBackendInterface
from mock_data.backends.Correlation import Correlation

file_readers = { '.csv': pd.read_csv }
file_resource_dir = files('mock_data.backends.resources')

class FileRandom(AbstractBackendInterface):
    """Provides random values read from a csv or other formatted file."""
    
    def __init__(self, file: str, field: str,
                 correlation: str = Correlation.INDEPENDENT.name) -> None:
        super().__init__(correlation)
        self.file = file
        self.field = field


    def generate_samples(self, size: int, directive: List = None) -> Iterable:
        file_path = file_resource_dir.joinpath(self.file)
        _, ext = os.path.splitext(file_path)
        fr = file_readers.get(ext)
        df = fr(file_path, comment='#')
        values = df[self.field].values
        return [values[random.randrange(len(values))] for c in range(size)]
