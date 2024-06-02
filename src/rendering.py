from Tree import(Root, SingleImage)
from PIL import Image, ImageDraw
import random



from const import (SINGLE_IMAGE_HEIGHT, SINGLE_IMAGE_WIDTH)

def renderRoot(root):

    assert isinstance(root, Root)

    images = []

    for single_image in root.children_analogie:
        images.append(renderSingleImage(single_image))

    allImage = concatenate_images_horizontally(images)

    allImage.save("test.png")



def renderSingleImage(single_image):


    assert isinstance(single_image, SingleImage)

    img = Image.new("RGB", (SINGLE_IMAGE_WIDTH, SINGLE_IMAGE_HEIGHT), "white")

    draw = ImageDraw.Draw(img)

    for component in single_image.components:

        if component.type.get_value() == "Square":

            rect_width = int(SINGLE_IMAGE_HEIGHT * component.size.get_value())
            x0 = random.randint(0, SINGLE_IMAGE_HEIGHT - rect_width)
            y0 = random.randint(0, SINGLE_IMAGE_HEIGHT - rect_width)

            x1 = x0 + rect_width
            y1 = y0 + rect_width
            draw.rectangle([x0, y0, x1, y1], outline="black", width= 2)
        elif component.type.get_value() == "Circle":

            circle_diameter = int(min(SINGLE_IMAGE_HEIGHT, SINGLE_IMAGE_WIDTH) * component.size.get_value())

            x0 = random.randint(0, SINGLE_IMAGE_HEIGHT - circle_diameter)
            y0 = random.randint(0, SINGLE_IMAGE_HEIGHT - circle_diameter)
            x1 = x0 + circle_diameter
            y1 = y0 + circle_diameter

            draw.ellipse([x0, y0, x1, y1], outline="black", width= 2)
    

    return img


def concatenate_images_horizontally(images):
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
        