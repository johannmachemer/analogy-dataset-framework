from src.components.Component import *
from src.components.ComponentStaticMethods import *


class Circle(Component):

    def __init__(self, component_identifier, superior_component = None, previous_version = None):
        super().__init__(component_identifier, Type("Circle"), superior_component, previous_version)

    def calculate_bounding_box(self):
        self.rotation.value = 0
        super().calculate_bounding_box()

    def draw(self, canvas):
        canvas.ellipse(convert_coordinates([self.get_top_left_corner(), self.get_bottom_right_corner()]), outline="black", width=2, fill=self.filling_color())

    def determine_feasible_rule_parameter(self, attr, parameters):
        if attr == "rotation":
            return []
        return super().determine_feasible_rule_parameter(attr, parameters)