import math

import numpy as np

from src.Tree import Group
from src.const import SINGLE_IMAGE_WIDTH, STAR_PEAKS

def intersect(edge, other_edge):
    """
        line intercept math by Paul Bourke http://paulbourke.net/geometry/pointlineplane/
    """
    x1, y1 = edge[0]
    x2, y2 = edge[1]
    x3, y3 = other_edge[0]
    x4, y4 = other_edge[1]

    if (x1 == x2 and y1 == y2) or (x3 == x4 and y3 == y4):
        return False
    denominator = ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1))

    if denominator == 0:
        return False
    ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denominator
    ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / denominator

    if ua < 0 or ua > 1 or ub < 0 or ub > 1:
        return False

    return True



class RenderingObject:

    def __init__(self, position, width, angle, fill):
        w = width / 2
        self.fill = fill
        self.boundingBox = translate_and_rotate(
            np.array([[-w, -w], [w, -w], [w, w], [-w, w]]),
            position,
            angle)

    def is_valid(self, image_width, image_height):
        return (not self.is_outside_image(image_width, image_height)) and 0 <= self.fill[0] <= 255

    def is_outside_image(self, image_width, image_height):
        for x, y in self.boundingBox:
            if not( 0 <= int(x) <= image_width):
                return True
            if not( 0 <= int(y) <= image_height):
                return True
        return False

    def overlap(self, other_object):
        return self.any_corner_inside(other_object) or other_object.any_corner_inside(self) or self.edge_collision(other_object)

    def any_corner_inside(self, other_object):
        for corner in other_object.boundingBox:
            if self.inside(corner):
                return True
        return False

    def edge_collision(self, other_object):
        object_edges = other_object.bounding_edges()
        for edge in self.bounding_edges():
            for other_edge in object_edges:
                if intersect(edge, other_edge):
                    return True
        return False

    def inside(self, point):
        """
        ray - casting algorithm based on
        https: // wrf.ecse.rpi.edu / Research / Short_Notes / pnpoly.html
        """
        x, y = point
        result = False
        for edge in self.bounding_edges():
            x0, y0 = edge[0]
            x1, y1 = edge[1]

            if ((y0 > y) != (y1 > y)) and (x < (x1 - x0) * (y - y0) / (y1 - y0) + x0):
                result = not result

        return result

    def bounding_edges(self):
        bounding_box_length = len(self.boundingBox)
        result = []
        for i in range(bounding_box_length):
            j = (bounding_box_length - 1 + i) % bounding_box_length
            result.append((self.boundingBox[i], self.boundingBox[j]))
        return result


    def translate_and_rotate(self, center, angle):
        self.boundingBox =  translate_and_rotate(self.boundingBox, center, angle)

    def get_top_left_corner(self):
        return self.boundingBox[0]

    def get_bottom_right_corner(self):
        return self.boundingBox[2]

    def draw(self, canvas):
        raise NotImplementedError()

class Circle(RenderingObject):

    def __init__(self, component, width, super_fill):
        circle_diameter = int(width * component.size.get_value())
        super().__init__(component.position.value, circle_diameter, 0, filling(component, super_fill))

    def translate_and_rotate(self, center, angle):
        self.boundingBox =  super().translate_and_rotate(center, 0)

    def draw(self, canvas):
        canvas.ellipse(convert_coordinates([self.get_top_left_corner(), self.get_bottom_right_corner()]), outline="black", width=2, fill=self.fill)

class Square(RenderingObject):

    def __init__(self, component, width, super_fill):
        rect_width = int(width * component.size.get_value())
        super().__init__(component.position.value, rect_width, component.rotation.value % 90, filling(component, super_fill))

    def draw(self, canvas):
        canvas.polygon(convert_coordinates(self.boundingBox), fill=self.fill, outline="black", width=2)

    def translate_and_rotate(self, center, angle):
        super().translate_and_rotate(center, 0)

class Star(RenderingObject):

    def __init__(self, component, width, super_fill):
        center = component.position.get_value()
        radius = int(width * component.size.get_value() / 2)
        angle = math.pi / STAR_PEAKS
        rotation_offset = math.pi / 2

        self.coordinates = np.empty((0, 2))
        for i in range(2 * STAR_PEAKS):
            r = radius if i % 2 == 0 else radius / 2
            x = center[0] + r * math.cos(i * angle + rotation_offset)
            y = center[1] + r * math.sin(i * angle + rotation_offset)
            self.coordinates = np.concatenate((self.coordinates, [(x, y)]))
        super().__init__(component.position.value, radius * 2, component.rotation.value, filling(component, super_fill))

    def translate_and_rotate(self, center, angle):
        super().translate_and_rotate(center, angle % (360 / STAR_PEAKS))
        self.coordinates = translate_and_rotate(self.coordinates, center, angle % (360 / STAR_PEAKS))

    def draw(self, canvas):
        canvas.polygon(convert_coordinates(self.coordinates), fill=self.fill, outline="black", width=2)

def determine_all_rendering_objects(components_list, super_width = SINGLE_IMAGE_WIDTH, super_fill = 1):
    result = []
    for component in components_list:
        if isinstance(component, Group):
            subcomponents = determine_all_rendering_objects(component.components, super_width * component.size.get_value(),
                                                            super_fill * component.filling.get_value())
            for subcomponent in subcomponents:
                subcomponent.translate_and_rotate(component.position.value, component.rotation.value)
            result.extend(subcomponents)
        else:
            if component.type.get_value() == "Square":
                rendering_object = Square(component, super_width, super_fill)
            elif component.type.get_value() == "Circle":
                rendering_object = Circle(component, super_width, super_fill)
            else:
                rendering_object = Star(component, super_width, super_fill)
            result.append(rendering_object)
    return result

def translate_and_rotate(points, center, angle):
        theta = angle / 180 * np.pi
        c, s = np.cos(angle), np.sin(theta)
        rotation_matrix = np.array(((c, -s), (s, c)))
        return np.matmul(points, rotation_matrix) + center


def filling(component, super_fill):
    value = component.filling.get_value()
    fill_color = int(255 * value * super_fill)
    return fill_color, fill_color, fill_color


def convert_coordinates(coordinates: np.ndarray[:2]) -> list[tuple[float, float]]:
    return [(x, y) for x, y in coordinates]