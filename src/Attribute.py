import numpy as np

from const import(SIZE_VALUES,SIZE_MAX,SIZE_MIN, TYPE_VALUES, TYPE_MAX, TYPE_MIN)

class Attribute():
    """
    superclass of all atributes

    Should not be instanciated. The level of an atribute is the chosen level between the maximum level
    and the minimum level of the Attribute

    """

    def __init__(self):
        pass

    def sample():
        pass

    def get_value():
        pass

    def set_value():
        pass

class Size(Attribute):

    def __init__(self, min_level=SIZE_MIN, max_level=SIZE_MAX):
        """
        Initalize new size attribute

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

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

class Type(Attribute):

    def __init__(self, min_level=TYPE_MIN, max_level=TYPE_MAX):
        self.min_level = min_level
        self.max_level = max_level
        self.values = TYPE_VALUES
        
        # standard value
        self.level = min_level
        self.value = self.values[self.level]

    def sample(self):

        self.level = np.random.randint(self.min_level, self.max_level+1)
        self.value = self.values[self.level]

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value
