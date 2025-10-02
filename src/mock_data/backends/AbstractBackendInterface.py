from abc import ABC, abstractmethod
from typing import Iterable, List
from mock_data.backends.Correlation import Correlation
import random 

directiveColumns = {}

class AbstractBackendInterface(ABC):
    """This class serves as an interface from which all backends should inherit.

    Each subclass must implement self.generate_samples(size)"""

    def __init__(self, correlation: str = Correlation.INDEPENDENT.name,
                 dep_field = None, dep_values: dict = None) -> None:
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
            col_values = []
            if type(self.dep_field) == list: #Behave different if list is given.
                for i in range(0,len(directive[0])): #for any given row
                    options = [] #Let's make a bucket of options for us, informed by directing fields.
                    blank = 0
                    for j in range(0,len(self.dep_field)): #For every directing field
                        if (directive[j][i] not in self.dep_values[self.dep_field[j]]): #if it is not in the dictionary
                            blank = 1 # we want the field to be blank.
                            break
                        elif (directive[j][i] in self.dep_values[self.dep_field[j]]) & (self.dep_values[self.dep_field[j]][directive[j][i]] != None): #If its in the dic and has specific values
                            new_possible_options = set(self.dep_values[self.dep_field[j]][directive[j][i]]) #new set of directions
                            old_possible_options = set(options) #set of old directions. NOTE: if this is blank, we essentially have no given restrictions yet. If its not blank, we need intersection of old directions.
                            options = list(new_possible_options & old_possible_options if old_possible_options != set() else new_possible_options) #takes intersection of options if previous restrictions were given, otherwise 0.
                    if len(options) != 0 & blank==0: #if specific values are directed to us and at no point directed to be blank, take those.
                        col_values.append(random.choice(options)) #choose from those
                    elif blank == 1: #if blank
                        col_values.append("") #be blank
                    else:
                        col_values.append(vals[i]) #If you do have directive fields with no specific values, then just accept whatever you populated.  
            else: # Only need special dictionary setup if you've got multiple dependencies.
                for i in range(0,len(directive)):#for any given row
                    if (directive[i] in list(self.dep_values.keys())): #If directive value is a key in dictionary,
                        if (self.dep_values[directive[i]] != None): #and non empty direction is given,
                            col_values.append(random.choice(self.dep_values[directive[i]])) #produce direction.
                        if (self.dep_values[directive[i]] == None): #if no direction is given
                            col_values.append(vals[i]) #produce what we would have anyway. 
                    else: 
                        col_values.append("")  #If not in dictionary, then we dont produce anything. 
        return col_values


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
