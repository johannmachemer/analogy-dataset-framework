import numpy as np

from Rule import (Progression, Rule)
from AnalogySample import AnalogySample
from AnalogySample import SingleImage
import copy
from src.components.Attribute import KindsOfAttributes
from src.InvalidImageHandler import save_invalid_image
from src.components.Circle import Circle
from src.components.Group import Group
from src.components.Square import Square
from src.components.Star import Star
from src.const import *


def create_analogy_sample():

    first = create_valid_image()
    third = create_valid_image()

    analog = create_samples_with_valid_rules(first, third)

    candidates = create_candidates(analog)

    analog.insert_candidates(candidates)
    return analog


def create_samples_with_valid_rules(first, third):
    rules:[Rule] = create_analogy_rules([first, third])
    second = copy.deepcopy(first)
    fourth = copy.deepcopy(third)
    for rule in rules:
        rule.apply_rule(first, second)
        rule.apply_rule(third, fourth)

    if not (validate_image(second) and validate_image(fourth)):
        return create_samples_with_valid_rules(first, third)

    analog = AnalogySample(rules)
    analog.insert_analogy(first)
    analog.insert_analogy(second)
    analog.insert_analogy(third)
    # analog.insert_analogy(fourth)
    analog.insert_candidates([fourth])
    return analog


def create_component(superior, component_number, depth):

    if depth == 0 :
        type = np.random.choice(TYPE_VALUES)
    else :
        type = np.random.choice(ALL_TYPE_VALUES)

    if type == "Circle":
        component = Circle(component_number, superior)
        component_number += 1
    elif type == "Group":
        component = Group(component_number, superior)
        component_number += 1
        for i in range(0, np.random.randint(MIN_COMPONENTS, MAX_COMPONENTS + 1)):
            component_number, subcomponent = create_component(component, component_number, depth - 1)
            component.insert_component(subcomponent)
    elif type == "Square":
        component = Square(component_number, superior)
        component_number += 1
    elif type == "Star":
        component = Star(component_number, superior)
        component_number += 1
    else:
        raise ValueError
    return component_number, component


def create_image():
    image = SingleImage()
    component_number = 0
    for i in range(0, np.random.randint(MIN_COMPONENTS, MAX_COMPONENTS+1)):
        component_number, component = create_component(image, component_number, MAX_DEPTH)
        image.insert_component(component)
    image.sample()
    return image

def create_valid_image():
    image = create_image()
    if validate_image(image):
        return image
    if SAVE_INVALID_IMAGES:
        save_invalid_image(image)
    return create_valid_image()


def invalid_component(component):
    invalid_subcomponents = component.type.value == "Group" and any(invalid_component(comp) for comp in component.components)
    return invalid_subcomponents or not(0 < component.size.value < 1) or not(0 < component.filling.value < 1)


def validate_image(image:SingleImage):
    if invalid_component(image):
        return False
    objects = image.get_all_components()
    for obj in objects:
        if not isinstance(obj, Group) and not obj.is_valid(SINGLE_IMAGE_WIDTH, SINGLE_IMAGE_HEIGHT):
            return False
    for first_index in range(len(objects) - 1):
        first = objects[first_index]
        if isinstance(first, Group):
            continue
        for second_index in range(first_index + 1, len(objects)):
            if isinstance(objects[second_index], Group):
                continue
            if first.overlap(objects[second_index]):
                return False
    return True

def create_candidates(sample: AnalogySample):
    """
        create answer candidates based on root and correct answer


    Attr:
        root (AnalogySample): root of the analogy
        answer (SingleImage): the image that builds the correct analogy

    Ret:
        candidates (List(SingleImage)): List of answer candidates

    """


    candidates = []

    for i in range(5):
        candidate = create_valid_image()

        candidates.append(candidate)

    return candidates

def create_analogy_rules(images):
    rules = []

    for i in range(0, np.random.randint(MIN_PROGRESSIONS, MAX_PROGRESSIONS+1)):
        rules.append(np.random.choice(feasible_rules(images)))
    for rule in rules:
        rule.sample()
    return rules

def feasible_rules(images):
    component_number = 0
    rules = []
    for attr in list(KindsOfAttributes):
        params = get_rule_params(attr.value)
        for image in images:
            component = image.get_component_by_index(component_number)
            params = component.determine_feasible_rule_parameter(attr.value, params)
        if len(params) != 0:
            rules.append(Progression(attr.value, params, component_number))

    return rules

def get_rule_params(attr):
    if attr == "size":
        return SIZE_PROGRESSIONS
    elif attr == "position":
        return POSITION_PROGRESSIONS
    elif attr == "type":
        return TYPE_VALUES
    elif attr == "filling":
        return FILLING_PROGRESSIONS
    elif attr == "rotation":
        return ROTATION_PROGRESSIONS
    else:
        raise ValueError
