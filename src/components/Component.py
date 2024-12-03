import copy

from src.components.Attribute import *
from src.components.ComponentStaticMethods import *


class Component:
    """Component node"""

    def __init__(self, component_identifier, type, superior_component = None, previous_version = None):
        """
        Instantiate a component node.
        """

        # init Attributes
        self.type = type
        self.component_identifier = str(component_identifier)
        self.boundingBox = []
        if previous_version is None:
            self.superior_component = superior_component
            self.size = Size()
            self.rotation = Rotation()
            self.position = Position()
            self.filling = Filling()
        else:
            self.superior_component = previous_version.superior_component
            self.size = copy.deepcopy(previous_version.size)
            self.rotation = copy.deepcopy(previous_version.rotation)
            self.position = copy.deepcopy(previous_version.position)
            self.filling = copy.deepcopy(previous_version.filling)
        self.calculate_bounding_box()

    def get_width(self):
        """
            the absolute width of the component on the canvas in pixels.
        """
        return  int(self.superior_component.get_width() * self.size.value)

    def add_size(self, value):
        self.size.value += value
        self.calculate_bounding_box()

    def get_filling(self):
        return  self.superior_component.get_filling() * self.filling.value

    def add_filling(self, value):
        self.filling.value += value

    def get_rotation(self):
        return  self.rotation.value

    def add_rotation(self, value):
        self.rotation.value += value
        self.calculate_bounding_box()

    def get_unique_component_identifier(self):

        if self.superior_component is None:
            return self.component_identifier
        superior_identifier = self.superior_component.get_unique_component_identifier()
        if superior_identifier == "-1":
            return self.component_identifier
        return superior_identifier + ":" + self.component_identifier

    def get_absolut_position(self):
        """
            determine the absolute position of the component inside the canvas
        """
        return rotate_and_translate(self.get_relative_position(), self.superior_component.get_absolut_position(), self.superior_component.get_rotation())

    def get_relative_position(self):
        """
            determine the position relative to the bounding box of the superior component
        """
        return self.position.value * self.superior_component.get_width() / 2

    def add_position(self, value):
        self.position.value += value
        self.calculate_bounding_box()

    def filling_color(self):
        return filling(self.get_filling())

    def calculate_bounding_box(self):
        w = self.get_width() / 2
        self.boundingBox = rotate_and_translate(
            np.array([[-w, -w], [w, -w], [w, w], [-w, w]]),
            self.get_absolut_position(),
            self.get_rotation())

    def get_top_left_corner(self):
        return self.boundingBox[0]

    def get_bottom_right_corner(self):
        return self.boundingBox[2]

    def draw(self, canvas):
        raise NotImplementedError()

    def is_valid(self, image_width, image_height):
        return (not is_outside_image(self.boundingBox, image_width, image_height)) and 0 <= self.get_filling() <= 1

    def overlap(self, other_object):
        return (any_corner_inside(self.boundingBox, other_object.boundingBox)
                or any_corner_inside(other_object.boundingBox, self.boundingBox)
                or edge_collision(self.boundingBox, other_object.boundingBox))

    def determine_feasible_rule_parameter(self, attr, parameters):
        if attr == "type":
            return [param for param in parameters if param != self.type.value]
        elif attr == "position":
            return [param for param in parameters if 0 <= self.position.value[0] + param <= 1 and 0 <= self.position.value[1] + param <= 1]
        elif attr == "size":
            return [param for param in parameters if 0.1 <= self.size.value + param <= 1]
        elif attr == "filling":
            return [param for param in parameters if 0.1 <= self.filling.value + param <= 1]
        return parameters

    def sample(self, attr=None):
        """
        sample a Single Image node. Sample either all attributes or one single attribute.

        Args:
            attr (String): The attribute that should be sampled (size, type, position or filling). If not set, ever attribute will be sampled
        """

        if attr is None:
            # sample every attribute
            self.size.sample()
            self.rotation.sample()
            self.position.sample(self.size.get_value())
            self.filling.sample()
        elif attr == "size":
            self.size.sample()
            self.position.sample(self.size.get_value())
        elif attr == "position":
            self.position.sample()
        elif attr == "filling":
            self.filling.sample()
        elif attr == "rotation":
            self.rotation.sample()

        self.calculate_bounding_box()

    def print(self, comp_number):
        """
        print component

        Args:
            comp_number (int): Index of component inside single image
        """
        print("     |")
        print("     --Component ", comp_number)
        print("       |")
        print("        --Type: ", self.type.get_value())
        print("        --Size: ", self.size.get_value())
        print("        --Position: ", self.position.get_value())
        print("        --Filling: ", self.filling.get_value())
        print("        --Rotation: ", self.rotation.get_value())

    def print_latex(self):
        """
        print component in latex syntax
        """
        output = ""
        output += "Component"
        output += "[ Type: "
        output += f"{self.type.get_value()}"
        output += "]"
        output += "[ Size: "
        output += f"{self.size.get_value()}"
        output += "]"
        output += "[ Position: "
        output += f"\({self.position.get_value()[0]} \, {self.position.get_value()[1]}\)"
        output += "]"
        output += "[ Rotation: "
        output += f"\({self.rotation.get_value()}\)"
        output += "]"
        output += "[ Filling: "
        output += f"\({self.filling.get_value()}\)"
        output += "]"

        return output