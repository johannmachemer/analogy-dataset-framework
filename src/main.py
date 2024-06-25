from Attribute import Size
from Rule import (Progression,Const, Rule)
from Tree import Root
from Tree import SingleImage
from Tree import Component
import copy
from PIL import Image, ImageDraw
import random
from rendering import renderRoot


def create_candidates(root: Root, answer: SingleImage):

    ruleList:list(Rule) = root.getRules();

    candidates = []

    for i in range(6):
        candidate = copy.deepcopy(answer)

        for rule in ruleList:
            candidate.components[rule.component_idx].sample(rule.attr)

        candidates.append(candidate);

    return candidates

progression = Progression("size", [0.2])
progression.sample()
const = Const("type")


analog = Root([progression, const])

first = SingleImage()

first.insertComponent(Component())
first.insertComponent(Component())

first.sample()

second = copy.deepcopy(first)

second.sample()

progression.apply_rule(first, second)
const.apply_rule(first, second)

third = copy.deepcopy(second)

third.sample()

progression.apply_rule(second, third)
const.apply_rule(second, third)



analog.insertAnalogie(first)
analog.insertAnalogie(second)
analog.insertAnalogie(third)

candidates = create_candidates(analog, third)

analog.insertAnswers(candidates)

# analog.printLatex()

# analog.saveLatex("test_with_answers")

renderRoot(analog)








