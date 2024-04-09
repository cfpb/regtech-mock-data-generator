
import random
from typing import List

from .BoundedDatetime import BoundedDatetime
from mock_data.backends import Correlation

class MinDirectedDatetime(BoundedDatetime):
        def __init__(
            self,
            min_datetime: str,
            max_datetime: str,
            correlation: str,
            dep_field: str,
            format: str = "%Y%m%d",
        ) -> None:
            super().__init__(min_datetime, max_datetime, format=format, 
                             correlation=correlation, dep_field=dep_field)


        def generate_samples(self, size: int, directive: List = None) -> List[str]:
            epoch_timestamps = [
                random.randrange(max(self._calculate_epoch_equivalent(directive[c], self.format),
                                     self._lower_bound), self._upper_bound) for c in range(size)]
            return self.nums_to_dates(epoch_timestamps)
