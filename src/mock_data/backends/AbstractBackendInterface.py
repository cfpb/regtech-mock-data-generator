from abc import ABC, abstractmethod
from typing import Iterable, List
from mock_data.backends.Correlation import Correlation
import random 

directiveColumns = {}

class AbstractBackendInterface(ABC):
    """This class serves as an interface from which all backends should inherit.

    Each subclass must implement self.generate_samples(size)"""

    def __init__(self, correlation: str = Correlation.INDEPENDENT.name,
                 dep_field: str = None, dep_values: dict[str,List[str]] = None) -> None:
        self.correlation = Correlation[correlation.upper()]
        self.dep_field = dep_field
        self.dep_values = dep_values


    def directive_requires_value(self, dval: any):
        dval = dval.split(';') if type(dval) == str and ';' in dval else str(dval)
        return ((type(dval) == str and dval in self.dep_values) or
                (type(dval) == list and (set(dval) & set(self.dep_values))))


    def values_where_directed(self, vals, directive):
        if not directive:
            return vals
        else:
            initial_list = []
            for i in range(0,len(directive)):
                if (directive[i] in list(self.dep_values.keys())): #If directive value is a key in dictionary,
                   if (self.dep_values[directive[i]] != None): #and non empty direction is given
                       initial_list.append(random.choice(self.dep_values[directive[i]])) #produce direction
                   if (self.dep_values[directive[i]] == None): #if no direction is given
                        initial_list.append(vals[i]) #produce what we would have anyway. 
                else: initial_list.append("")  #If not in dictionary, then we dont produce anything. 
        return initial_list


    @abstractmethod
    def generate_samples(self, size: int, directive: List) -> Iterable:
        """This method must be implemented by each sampling engine. The method should
        accept the number of samples to generate and return a numpy array containing
        samples. These can be of any data type appropriate for the sampling engine.

        Args:
            size (int): A positive integer representing the desired number of samples.

        Returns:
            Iterable: An iterable (list, np.array, etc) of sampled values with `size`
                elements.
        """
        pass
