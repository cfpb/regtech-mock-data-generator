import random
import string
from typing import List,Iterable

from mock_data.backends import AbstractBackendInterface
from mock_data.backends.Correlation import Correlation

class UniqueID(AbstractBackendInterface):
    def __init__(
        self,
        max_generate: int,
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
        self.max_generate = max_generate
    
    def generate_samples(self, size: int, directive: List = None) -> Iterable:
        lei_ids = []
        for i in range(size):
            n = random.randint(1,self.max_generate)
            lou = ''.join(random.choices(string.digits, k=self.lou))
            entity_id = ''.join(random.choices(string.ascii_uppercase + string.digits,k=self.entity))
            verification_id = ''.join(random.choices(string.digits,k=self.verification))
            loan_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))
            lei_ids.append(''.join(lou+'00'+entity_id+verification_id+loan_id))
        return lei_ids
    

        


    


        
        


