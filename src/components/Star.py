import math

from src.components.Attribute import *
from src.components.Component import Component
from src.components.ComponentStaticMethods import rotate_and_translate, convert_coordinates


class Star(Component):

    def __init__(self, component_number, superior_component = None, previous_version = None):
        self.star_corners = np.empty((0, 2))
        super().__init__(component_number, Type("Star"), superior_component, previous_version)

    def calculate_bounding_box(self):
        super().calculate_bounding_box()

        radius = self.get_width() / 2
        angle = math.pi / STAR_PEAKS
        rotation_offset = math.pi / 2

        self.star_corners = np.empty((0, 2))
        for i in range(2 * STAR_PEAKS):
            r = radius if i % 2 == 0 else radius / 2
            x = r * math.cos(i * angle + rotation_offset)
            y = r * math.sin(i * angle + rotation_offset)
            self.star_corners = np.concatenate((self.star_corners, [(x, y)]))

        self.star_corners = rotate_and_translate(
            self.star_corners,
            self.get_absolut_position(),
            self.get_rotation())

    def draw(self, canvas):
        canvas.polygon(convert_coordinates(self.star_corners), fill=self.filling_color(), outline="black", width=2)
