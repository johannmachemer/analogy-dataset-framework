from Tree import(Root, SingleImage)
from PIL import Image, ImageDraw
import math
import random
import os
from const import (SINGLE_IMAGE_HEIGHT, SINGLE_IMAGE_WIDTH)



def render_star(draw, center, radius, points, fill, outline, width):
    """
    Draws a star-shaped polygon on a canvas.

    Args:
        draw: The drawing context
        center (tuple): The (x, y) coordinates of the star's center.
        radius (float): The radius of the star (distance from center to outermost points).
        points (int): The number of points (or spikes) the star should have.
        fill: The fill color of the star.
        outline: The outline color of the star.
        width (int): The width of the star's outline.
    """
    angle = math.pi / points
    rotation_offset = math.pi / 2

    coords = []
    for i in range(2 * points):
        r = radius if i % 2 == 0 else radius / 2
        x = center[0] + r * math.cos(i * angle + rotation_offset)
        y = center[1] - r * math.sin(i * angle + rotation_offset)
        coords.append((x, y))

    draw.polygon(coords, fill=fill, outline=outline, width=width)



def safeRootAsSingleImages(root,id):
    """
    Saves a Root as single images

    Args:
        root (Root): root to save
        id (int): id of the analogy
    """
    assert isinstance(root, Root)

    images = []

    for single_image in root.children_analogie:
        images.append(renderSingleImage(single_image))

    for single_image in root.children_answer:
        images.append(renderSingleImage(single_image))

    if not os.path.isdir("data"):
        os.mkdir("data")

    for (idx,image) in enumerate(images):

        if not os.path.isdir(f"data/{id}"):
            os.mkdir(f"data/{id}")

        image.save(f"data/{id}/{id}-{idx}.png")



    

def safeRootAsCollage(root, id):
    """
    Saves a Root as a collage

    Args:
        root (Root): root to save
        id (int): id of the analogy
    """

    assert isinstance(root, Root)

    images = []

    for single_image in root.children_analogie:
        images.append(renderSingleImage(single_image))

    analog_image = concatenate_images_horizontally(images)

    images = []

    for single_image in root.children_answer:
        images.append(renderSingleImage(single_image))

    answer_images_1 = concatenate_images_horizontally(images[0:3])

    answer_images_2 = concatenate_images_horizontally(images[3:6])

    all_images = concatenate_images_vertical([analog_image, answer_images_1, answer_images_2])

    if not os.path.isdir("data"):
        os.mkdir("data")
        
    all_images.save(f"data/{id}/{id}-collage.png")



def renderSingleImage(single_image):
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

    for component in single_image.components:

        filling = component.filling.get_value()
        fill_color = int(255 * (1-filling)) 
        fill = (fill_color, fill_color, fill_color)

        if component.type.get_value() == "Square":

            rect_width = int(SINGLE_IMAGE_HEIGHT * component.size.get_value())
            x0 = component.position.get_value()[0]
            y0 = component.position.get_value()[1]

            x1 = x0 + rect_width
            y1 = y0 + rect_width
            draw.rectangle([x0, y0, x1, y1], outline="black", width= 2, fill=fill)
        elif component.type.get_value() == "Circle":

            circle_diameter = int(min(SINGLE_IMAGE_HEIGHT, SINGLE_IMAGE_WIDTH) * component.size.get_value())

            

            x0 = component.position.get_value()[0]
            y0 = component.position.get_value()[1]
            x1 = x0 + circle_diameter
            y1 = y0 + circle_diameter

            draw.ellipse([x0, y0, x1, y1], outline="black", width= 2, fill=fill)

        elif component.type.get_value() == "Star":
            center = component.position.get_value()
            radius = int(min(SINGLE_IMAGE_HEIGHT, SINGLE_IMAGE_WIDTH) * component.size.get_value() / 2)
            render_star(draw, center, radius, 5, fill, "black", 2)
    

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


        