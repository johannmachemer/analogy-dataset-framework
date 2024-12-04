import json

from src.Rule import Progression
from src.AnalogySample import SingleImage, AnalogySample
from src.components.Circle import *
from src.components.Component import Component
from src.components.Group import Group
from src.components.Square import Square
from src.components.Star import Star


def import_json(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
        return convert_dict(data)

def convert_dict(dict):
    rules = []
    for rule_input in dict["rules"]:
        if rule_input["rule_type"] == "Progression":
            rule = Progression(rule_input["attr"])
            rule.value = float(rule_input["value"])
            rule.params = [rule.value]
            rule.component_idx = rule_input["component_idx"]
            rules.append(rule)

    sample = AnalogySample(rules)
    for image_input in dict["analogy"]:
        image = convert_image(image_input)
        sample.insert_analogy(image)

    candidates = []
    for image_input in dict["candidates"]:
        image = convert_image(image_input)
        candidates.append(image)

    sample.insert_candidates(candidates)

    return sample

def import_json_image(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
        return convert_image(data)

def convert_image(image_input):
    image = SingleImage()
    for component_input in image_input["components"]:
        component = convert_component(component_input, image)
        image.insert_component(component)
    return image


def convert_component(component_input, superior):
    type = component_input["type"]
    component_number = component_input["component_id"]
    component = Component(component_number, Type(type), superior_component=superior)
    component.size.value = float(component_input["size"])
    component.position.value = np.array(component_input["position"])
    component.rotation.value = int(component_input["rotation"])
    component.filling.value = float(component_input["filling"])

    if type == "Circle":
        component = Circle(component_number, previous_version=component)
    elif type == "Group":
        component = Group(component_number, previous_version=component)
        for subcomponent in component_input["components"]:
            component.insert_component(convert_component(subcomponent, component))
    elif type == "Square":
        component = Square(component_number, previous_version=component)
    elif type == "Star":
        component = Star(component_number, previous_version=component)
    else:
        raise ValueError
    return component