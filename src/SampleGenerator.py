import numpy as np

from Rule import (Progression,Const, Rule)
from Tree import AnalogySample
from Tree import SingleImage
from Tree import Component
import copy
from src.Attribute import KindsOfAttributes
from src.InvalidImageHandler import save_invalid_image
from src.RenderingObjectGenerator import RenderingObject, determine_all_rendering_objects
from src.const import NUMBER_OF_SAMPLES, MIN_COMPONENTS, MAX_COMPONENTS, SINGLE_IMAGE_HEIGHT, SINGLE_IMAGE_WIDTH, \
    SAVE_INVALID_IMAGES


def create_analogy_sample():

    first = create_valid_image()
    third = create_valid_image()

    analog = create_samples_with_valid_rules(first, third)

    candidates = create_candidates(analog)

    analog.insert_candidates(candidates)
    return analog


def create_samples_with_valid_rules(first, third):
    rules:[Rule] = create_analogy_rules()
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


def create_image():
    image = SingleImage()
    for i in range(0, np.random.randint(MIN_COMPONENTS, MAX_COMPONENTS+1)):
        image.insert_component(Component())
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
    objects = determine_all_rendering_objects(image.components)
    for obj in objects:
        if not obj.is_valid(SINGLE_IMAGE_WIDTH, SINGLE_IMAGE_HEIGHT):
            return False
    for first_index in range(len(objects) - 1):
        first = objects[first_index]
        for second_index in range(first_index + 1, len(objects)):
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

def create_analogy_rules():
    rules = []
    for component_idx in range(0, MAX_COMPONENTS):
        for kindOfAttribute in list(KindsOfAttributes):
            if component_idx == 0 and np.random.random() < 0.5:
                rules.append(Progression(kindOfAttribute.value, [], component_idx))

    for rule in rules:
        rule.sample()
    if len(rules) == 0:
        return create_analogy_rules()
    return rules