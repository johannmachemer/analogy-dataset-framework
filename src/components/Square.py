from src.components.Attribute import *
from src.components.Component import Component
from src.components.ComponentStaticMethods import convert_coordinates

class Square(Component):
    def __init__(self, component_identifier, superior_component = None, previous_version = None):
        super().__init__(component_identifier, Type("Square"), superior_component, previous_version)

    def draw(self, canvas):
        canvas.polygon(convert_coordinates(self.boundingBox), fill=self.filling_color(), outline="black", width=2)

    def determine_feasible_rule_parameter(self, attr, parameters):
        if attr == "rotation":
            return [param for param in parameters if param != 90]
        return super().determine_feasible_rule_parameter(attr, parameters)