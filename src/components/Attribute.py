import numpy as np
from enum import Enum, StrEnum
from src.const import *


class KindsOfAttributes(StrEnum):
    SIZE = "size"
    TYPE = "type"
    POSITION = "position"
    ROTATION = "rotation"
    FILLING = "filling"

class Attribute:
    """
    superclass of all attributes

    Should not be instantiated. The level of an attribute is the chosen level between the maximum level
    and the minimum level of the Attribute

    self.level: the current level of the attribute
    self.value: the current value of the attribute determined with the level
    self.values: list of possible values, if there are predefined values

    """

    def __init__(self):
        self.value = None
        pass


    
    def sample(self):
        """
        sample the value of the attribute
        """
        pass

    def get_value(self):
        return self.value
        

class Size(Attribute):

    def __init__(self, min_level=SIZE_MIN, max_level=SIZE_MAX):
        """
        Initialize new size attribute

        Args:
            min_level (int): the minimum level of the size.
            max_level (int): the maximum level of the size
        """
        super().__init__()
        self.min_level = min_level
        self.max_level = max_level
        
        # standard value
        self.value = max_level

    def sample(self):
        self.value = np.random.uniform(self.min_level, self.max_level)


class Rotation(Attribute):

    def __init__(self, value=0):
        """
        Initialize new size attribute
        """

        # standard value
        super().__init__()
        self.value = value

    def sample(self):
        """
        randomize the rotation
        """
        self.value = np.random.randint(ROTATION_MIN, ROTATION_MAX + 1)

class Type(Attribute):
   

    def __init__(self, value = TYPE_VALUES[TYPE_MIN]):
        """
        Initialize new size attribute

        Args:
            value (str): actual value of the type
        """
        super().__init__()
        self.min_level = TYPE_MIN
        self.max_level = TYPE_MAX
        self.values = TYPE_VALUES
        
        # standard value
        self.value = value

    
    def sample(self):
        """
        sample the value of the Type
        """

        self.value = self.values[ np.random.randint(self.min_level, self.max_level+1)]


class Position(Attribute):

    def __init__(self, min_level=-1, max_level=1):
        """
        Initialize new position attribute

        Args:
            min_level (int): the minimum level of the position.
            max_level (int): the maximum level of the position.
        """
        super().__init__()
        self.min_level = min_level
        self.max_level = max_level

        self.value = np.array([0.,0.])

    
    def sample(self, width=0):
        """
        sample the value of the position

        Args:
            width(float): width of the object, so its inside the borders
        """
        minimal_left_upper_corner = np.ones(2) * (width / 2 + self.min_level)
        self.value = np.array([np.random.uniform(0, self.max_level - width - self.min_level), np.random.uniform(0, self.max_level - width - self.min_level)]) + minimal_left_upper_corner



class Filling(Attribute):
    def __init__(self, min_level = FILLING_MIN, max_level=FILLING_MAX):
        """
        Initialize new Filling attribute

        Args:
            min_level (int): the minimum level of the filling.
            max_level (str): the maximum level of the filling.
        """
        super().__init__()
        self.min_level = min_level
        self.max_level = max_level

        #standard value
        self.value = min_level

   
    def sample(self):
        """
        sample the value of the filling
        """
        self.value = 1- np.random.uniform(self.min_level, self.max_level)



        

