from Tree import (AnalogySample, SingleImage, Group)
from PIL import Image, ImageDraw
import os
from const import (SINGLE_IMAGE_HEIGHT, SINGLE_IMAGE_WIDTH, STAR_PEAKS)
from src.RenderingObjectGenerator import determine_all_rendering_objects


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


        