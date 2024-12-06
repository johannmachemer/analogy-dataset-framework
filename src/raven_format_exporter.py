from src.AnalogySample import AnalogySample, SingleImage
from src.components.Component import Component
from src.components.Group import Group


def convert_image_to_line(image:SingleImage):
    return [line for comp in image.components for line in convert_component_to_line(comp)]

def convert_component_to_line(component:Component):
    if isinstance(component, Group):
        return ["(:GROUP \n"] +  ["\t" + line for comp in component.components for line in convert_component_to_line(comp)] + [")\n"]
    position = component.get_absolut_position()
    return [f"(:POS-X {int(position[0])} " +
            f":POS-Y {int(position[1])} " +
            f":ORIENTATION {int(component.get_absolut_rotation())} " +
            f":BRIGHTNESS {int(component.filling_color()[0])} " +
            f":TYPE {component.type.value} " +
            f":SIZE {int(component.get_width())})\n"]


def write_sample(sample:AnalogySample, analogy_id:int):

    image_number = 0
    sample_lines = []

    for image in sample.all_images():
        image_lines = convert_image_to_line(image)

        with open(f"data/{analogy_id}/{analogy_id}-{image_number}.txt", 'w') as data:
            data.writelines(image_lines)

        sample_lines.append(f"(:image {image_number} \n")
        sample_lines.extend(["\t" + line for line in image_lines])
        sample_lines.append(")\n")
        image_number += 1


    with open(f"data/{analogy_id}/{analogy_id}-collection.txt", 'w') as data:
        data.writelines(sample_lines)