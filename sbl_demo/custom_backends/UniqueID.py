import random
import string
from typing import List,Iterable

from mock_data.backends import AbstractBackendInterface
 
class UniqueID(AbstractBackendInterface):
    def __init__(
            self,
    ) -> None:
        def generate_lei(self):
            n = random.randint(1, 25)
            first = ''.join(random.choices(string.digits, k=4))
            middle = ''.join(random.choices(string.ascii_uppercase + string.digits,k=14))
            last = ''.join(random.choices(string.digits, k=2))
            final = ''.join(random.choices(string.digits, k=n))
        return ''.join(first+middle+last+final)
    
    def generate_samples(self, size: int) -> Iterable:
        return super().generate_samples(size)
    


        
        


