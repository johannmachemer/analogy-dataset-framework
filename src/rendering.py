import numpy as np
from numpy import ndarray
from numpy.f2py.auxfuncs import throw_error

from Tree import (AnalogySample, SingleImage, Group)
from PIL import Image, ImageDraw
import math
import random
import os
from const import (SINGLE_IMAGE_HEIGHT, SINGLE_IMAGE_WIDTH, STAR_PEAKS)

def safe_root_as_single_images(root, id):
    """
    Saves a Root as single images

    Args:
        root (AnalogySample): root to save
        id (int): id of the analogy
    """
    assert isinstance(root, AnalogySample)

    images = []

    for single_image in root.analogy:
        images.append(render_single_image(single_image))

    for single_image in root.candidates:
        images.append(render_single_image(single_image))

    if not os.path.isdir("data"):
        os.mkdir("data")

    for (idx,image) in enumerate(images):

        if not os.path.isdir(f"data/{id}"):
            os.mkdir(f"data/{id}")

        image.save(f"data/{id}/{id}-{idx}.png")



    

def safe_root_as_collage(root, id):
    """
    Saves a Root as a collage

    Args:
        root (AnalogySample): root to save
        id (int): id of the analogy
    """

    assert isinstance(root, AnalogySample)

    images = []

    for single_image in root.analogy:
        images.append(render_single_image(single_image))

    analog_image = concatenate_images_horizontally(images)

    images = []

    for single_image in root.candidates:
        images.append(render_single_image(single_image))

    answer_images_1 = concatenate_images_horizontally(images[0:3])

    answer_images_2 = concatenate_images_horizontally(images[3:6])

    all_images = concatenate_images_vertical([analog_image, answer_images_1, answer_images_2])

    if not os.path.isdir("data"):
        os.mkdir("data")
        
    all_images.save(f"data/{id}/{id}-collage.png")


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

def convert_coordinates(coordinates:ndarray[:2]) -> list[tuple[float, float]]:
    return [ (x,y) for x,y in coordinates]

class RenderingObject:

    def __init__(self, position, width, angle, fill):
        w = width / 2
        self.fill = fill
        self.boundingBox = translate_and_rotate(
            np.array([[-w, -w], [w, -w], [w, w], [-w, w]]),
            position,
            angle)

    def translate_and_rotate(self, center, angle):
        self.boundingBox =  translate_and_rotate(self.boundingBox, center, angle)

    def draw(self, canvas):
        raise NotImplementedError()

class Circle(RenderingObject):

    def __init__(self, component, width, super_fill):
        circle_diameter = int(width * component.size.get_value())
        super().__init__(component.position.value, circle_diameter, 0, filling(component, super_fill))

    def translate_and_rotate(self, center, angle):
        self.boundingBox =  super().translate_and_rotate(center, 0)

    def draw(self, canvas):
        canvas.ellipse(convert_coordinates([self.boundingBox[0], self.boundingBox[2]]), outline="black", width=2, fill=self.fill)

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



def render_single_image(single_image):
    """
    Render a single image

    Args:
        single_image (SingleImage): the single image to render

    Returns:
        img (Image): The rendered Image
    """
    assert isinstance(single_image, SingleImage)

    img = Image.new("RGB", (SINGLE_IMAGE_WIDTH, SINGLE_IMAGE_HEIGHT), "white")

    draw = ImageDraw.Draw(img)

    rendering_objects = determine_all_rendering_objects(single_image.components)

    for rendering_object in rendering_objects:
        rendering_object.draw(draw)

    return img


def concatenate_images_horizontally(images):
    """
    concatenate multiple images horizontally

    Args:
        images (List(Image)): All Images to concatenate

    Returns:
        new_img (Image): All images put together horizontally
    """
    # Calculate the total width and maximum height of the final image
    total_width = sum(img.width for img in images)
    max_height = max(img.height for img in images)

    # Create a new blank image with the calculated size
    new_image = Image.new('RGB', (total_width, max_height), 'white')
    draw = ImageDraw.Draw(new_image)

    # Paste each image into the new image
    current_x = 0
    for i, img in enumerate(images):
        new_image.paste(img, (current_x, 0))
        current_x += img.width
        if i < len(images) - 1:  # Draw the line except after the last image
            draw.line([(current_x, 0), (current_x, max_height)], fill="black", width=5)
            current_x += 5

    return new_image

def concatenate_images_vertical(images):
    """
    concatenate multiple images vertically

    Args:
        images (List(Image)): All Images to concatenate

    Returns:
        new_img (Image): All images put together vertically
    """
    total_width = max(img.width for img in images)
    max_height = sum(img.height for img in images)

    new_image = Image.new('RGB', (total_width, max_height), 'white')
    draw = ImageDraw.Draw(new_image)

    current_y = 0
    for i,img in enumerate(images):
        new_image.paste(img, (0, current_y))
        current_y += img.height
        if i < len(images) - 1:  # Draw the line except after the last image
            if i == 0:
                draw.line([(0, current_y), (total_width, current_y)], fill="red", width=5)
            else:
                draw.line([(0, current_y), (total_width, current_y)], fill="black", width=5)
                current_y += 5

    return new_image


        