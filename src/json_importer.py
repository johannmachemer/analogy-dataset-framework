import json

import numpy as np

from src.Rule import Progression
from src.Tree import SingleImage, Component, AnalogySample

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
        component = convert_component(component_input)
        image.insert_component(component)
    return image


def convert_component(component_input):
    component = Component()
    component.type.value = component_input["type"]
    component.size.value = component_input["size"]
    component.position.value = np.array(component_input["position"])
    component.rotation.value = int(component_input["rotation"])
    component.filling.value = int(component_input["filling"])
    return component