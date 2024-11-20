import numpy as np

from const import(SIZE_VALUES,SIZE_MAX,SIZE_MIN, TYPE_VALUES, TYPE_MAX, TYPE_MIN,SINGLE_IMAGE_HEIGHT, FILLING_MAX, FILLING_MIN, FILLING_VALUES)

class Attribute():
    """
    superclass of all attributes

    Should not be instantiated. The level of an attribute is the chosen level between the maximum level
    and the minimum level of the Attribute

    self.level: the current level of the attribute
    self.value: the current value of the attribute determined with the level
    self.values: list of possible values, if there are predefined values

    """

    def __init__(self):
        pass


    
    def sample():
        """
        sample the value of the attribute
        """
        pass

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value
        

class Size(Attribute):

    def __init__(self, min_level=SIZE_MIN, max_level=SIZE_MAX):
        """
        Initialize new size attribute

        Args:
            min_level (int): the minimum level of the size.
            max_level (str): the maximum level of the size
        """

        self.min_level = min_level
        self.max_level = max_level
        self.values = SIZE_VALUES
        
        # standard value
        self.level = min_level
        self.value = self.values[self.level]

    def sample(self):
        self.level = np.random.randint(self.min_level, self.max_level+1)
        self.value = self.values[self.level]

class Type(Attribute):
   

    def __init__(self, min_level=TYPE_MIN, max_level=TYPE_MAX):
        """
        Initialize new size attribute

        Args:
            min_level (int): the minimum level of the size.
            max_level (str): the maximum level of the size
        """
        self.min_level = min_level
        self.max_level = max_level
        self.values = TYPE_VALUES
        
        # standard value
        self.level = min_level
        self.value = self.values[self.level]

    
    def sample(self):
        """
        sample the value of the Type
        """

        self.level = np.random.randint(self.min_level, self.max_level+1)
        self.value = self.values[self.level]


class Position(Attribute):


   
    def __init__(self, min_level=0, max_level=SINGLE_IMAGE_HEIGHT):
        """
        Initialize new position attribute

        Args:
            min_level (int): the minimum level of the position.
            max_level (str): the maximum level of the position.
        """
         
        self.min_level = min_level
        self.max_level = max_level
        
        # standard value
        self.level = (min_level, min_level)
        self.value = self.level

    
    def sample(self, size=(0,0)):
        """
        sample the value of the position

        Args:
            size(float,float): size of the object, so its inside the borders
        """
        self.level = (np.random.randint(self.min_level, int(self.max_level - size[0]*SINGLE_IMAGE_HEIGHT)), np.random.randint(self.min_level, (self.max_level - size[1]*SINGLE_IMAGE_HEIGHT)))
        self.value = self.level


class Filling(Attribute):
    

    def __init__(self, min_level = FILLING_MIN, max_level=FILLING_MAX):
        """
        Initialize new Filling attribute

        Args:
            min_level (int): the minimum level of the filling.
            max_level (str): the maximum level of the filling.
        """
        self.min_level = min_level
        self.max_level = max_level
        self.values = FILLING_VALUES


        #standard value
        self.level = min_level
        self.value = self.values[self.level]

   
    def sample(self):
        """
        sample the value of the filling
        """
        self.level = np.random.randint(self.min_level, self.max_level+1)
        self.value = self.values[self.level]



        

