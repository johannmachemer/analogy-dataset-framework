from src.components.Attribute import *
from src.components.Component import Component
from src.components.ComponentStaticMethods import convert_coordinates

class Square(Component):
    def __init__(self, superior_component = None, previous_version = None):
        super().__init__(Type("Square"), superior_component, previous_version)

    def draw(self, canvas):
        canvas.polygon(convert_coordinates(self.boundingBox), fill=self.filling_color(), outline="black", width=2)