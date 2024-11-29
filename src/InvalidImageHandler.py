import json
import os

from src.json_export import single_image_to_json
from src.rendering import render_single_image


def save_invalid_image(image):

    if not os.path.isdir("data/invalid"):
        os.mkdir("data/invalid")

    id = len([name for name in os.listdir('data/invalid') if os.path.isfile("data/invalid/" + name)]) / 2 + 1
    img = render_single_image(image)


    img.save(f"data/invalid/{id}.png")

    dict = single_image_to_json(id, image)

    with open(f"data/invalid/{id}.json", "w") as f:
        json.dump(dict, f, indent=4)
