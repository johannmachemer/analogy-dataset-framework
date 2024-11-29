import numpy as np

from Attribute import Size
from Rule import (Progression,Const, Rule)
from Tree import AnalogySample
from Tree import SingleImage
from Tree import Component
import copy
from PIL import Image, ImageDraw
import random
from rendering import (safe_root_as_collage, safe_root_as_single_images)
from json_export import safe_json
from src.Attribute import KindsOfAttributes
from src.const import NUMBER_OF_SAMPLES, MIN_COMPONENTS, MAX_COMPONENTS

def create_analogy_sample():
    rules:[Rule] =  create_analogy_rules()
    analog = AnalogySample(rules)

    first = SingleImage()
    third = SingleImage()
    for i in range(0, np.random.randint(MIN_COMPONENTS, MAX_COMPONENTS+1)):
        first.insert_component(Component())
        third.insert_component(Component())
    first.sample()
    third.sample()

    second = copy.deepcopy(first)
    fourth = copy.deepcopy(third)
    for rule in rules:
        rule.apply_rule(first, second)
        rule.apply_rule(third, fourth)

    analog.insert_analogy(first)
    analog.insert_analogy(second)
    analog.insert_analogy(third)
    #analog.insertAnalogy(fourth)
    analog.insert_candidates([fourth])

    candidates = create_candidates(analog, third)

    analog.insert_candidates(candidates)
    return analog


def create_candidates(root: AnalogySample, answer: SingleImage):
    """
        create answer candidates based on root and correct answer


    Attr:
        root (Root): root of the analogy
        answer (SingleImage): the image that builds the correct analogy

    Ret:
        candidates (List(SingleImage)): List of answer candidates

    """

    rule_list = root.get_rules()

    candidates = []

    for i in range(5):
        candidate = copy.deepcopy(answer)

        for rule in rule_list:
            # just sample attr component and just attr attribute
            candidate.components[rule.component_idx].sample(rule.attr)

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