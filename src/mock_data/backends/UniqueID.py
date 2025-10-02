import random
import string
from typing import List,Iterable

from mock_data.backends import AbstractBackendInterface
from mock_data.backends.Correlation import Correlation

class UniqueID(AbstractBackendInterface):
    def __init__(
        self,
        min_generate: int,
        max_generate: int,
        lei: str = '',
        lou: int = 4, 
        entity: int = 12,
        verification: int = 2,
        correlation: str = Correlation.INDEPENDENT.name,
        **distribution_kwargs,
    ) -> None:
        """This will create an LEI with a random number of of digits following it as per FIG guidelines.
        the names of the attributes above as well as numbers are structured based on LEI. Max_generate is 
        simply the number of random characters following an LEI for the loan specific identifier. In our case, the 
        most it can generate is 25 values. 
          """
        super().__init__(correlation)
        self.lou = lou 
        self.entity = entity
        self.verification = verification
        self.min_generate = min_generate
        self.max_generate = max_generate
        self.lei = lei

    def generate_samples(self, size: int, directive: List = None) -> Iterable:
        uids = []
        for i in range(size):
            n = random.randint(self.min_generate, self.max_generate)
            if self.lei != '':
                uid = self.lei + ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))
                uids.append(uid)
            else:
                uids.append(''.join(random.choices(string.ascii_uppercase + string.digits, k=n)))
        return uids
    

        


    


        
        


