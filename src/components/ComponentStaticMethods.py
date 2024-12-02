import numpy as np


def rotate_and_translate(points, center, angle):
        theta = angle / 180 * np.pi
        c, s = np.cos(angle), np.sin(theta)
        rotation_matrix = np.array(((c, -s), (s, c)))
        return np.matmul(points, rotation_matrix) + center

def filling(value):
    fill_color = int(255 * value)
    return fill_color, fill_color, fill_color


def convert_coordinates(coordinates: np.ndarray[:2]) -> list[tuple[float, float]]:
    return [(x, y) for x, y in coordinates]


def bounding_edges(bounding_box):
    bounding_box_length = len(bounding_box)
    result = []
    for i in range(bounding_box_length):
        j = (bounding_box_length - 1 + i) % bounding_box_length
        result.append((bounding_box[i], bounding_box[j]))
    return result

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


def edge_collision(first_bounding_box, other_bounding_box):
    object_edges = bounding_edges(other_bounding_box)
    for edge in bounding_edges(first_bounding_box):
        for other_edge in object_edges:
            if intersect(edge, other_edge):
                return True
    return False

def any_corner_inside(first_bounding_box, other_bounding_box):
    for corner in other_bounding_box:
        if inside(first_bounding_box, corner):
            return True
    return False

def inside(first_bounding_box, point):
    """
    ray - casting algorithm based on
    https: // wrf.ecse.rpi.edu / Research / Short_Notes / pnpoly.html
    """
    x, y = point
    result = False
    for edge in bounding_edges(first_bounding_box):
        x0, y0 = edge[0]
        x1, y1 = edge[1]

        if ((y0 > y) != (y1 > y)) and (x < (x1 - x0) * (y - y0) / (y1 - y0) + x0):
            result = not result

    return result

def is_outside_image(bounding_box, image_width, image_height):
    for x, y in bounding_box:
        if not( 0 <= int(x) <= image_width):
            return True
        if not( 0 <= int(y) <= image_height):
            return True
    return False