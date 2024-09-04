from Attribute import Size
from Rule import (Progression,Const, Rule)
from Tree import Root
from Tree import SingleImage
from Tree import Component
import copy
from PIL import Image, ImageDraw
import random
from rendering import (safeRootAsCollage, safeRootAsSingleImages)
from json_export import safe_json





def create_candidates(root: Root, answer: SingleImage):

    ruleList:list(Rule) = root.getRules()

    candidates = []

    for i in range(6):
        candidate = copy.deepcopy(answer)

        for rule in ruleList:
            # just sample attr component and just attr attribute
            candidate.components[rule.component_idx].sample(rule.attr)

        candidates.append(candidate)

    return candidates


def build_first_example_sample():

    for i in range(0,5):
        
        progression = Progression("size", [0.2])
        progression.sample()
        const_type = Const("type")
        const_type.sample()

        analog= Root([progression, const_type])

        first = SingleImage()
        first.insertComponent(Component())
        first.insertComponent(Component())
        first.sample()
        
        second = copy.deepcopy(first)
        second.sample()
        progression.apply_rule(first, second)
        const_type.apply_rule(first, second)


        third = copy.deepcopy(second)
        third.sample()
        progression.apply_rule(second, third)
        const_type.apply_rule(second, third)


        analog.insertAnalogie(first)
        analog.insertAnalogie(second)
        analog.insertAnalogie(third)

        candidates = create_candidates(analog, third)

        analog.insertAnswers(candidates)

        safeRootAsSingleImages(analog, i)
        safe_json(analog, i)
        safeRootAsCollage(analog, i)


    for i in range(5,10):
        
        const_size = Const("size")
        const_type = Const("type")
        const_type.sample()
        const_size.sample()

        analog= Root([const_size, const_type])

        first = SingleImage()
        first.insertComponent(Component())
        first.insertComponent(Component())
        first.sample()


        
        second = copy.deepcopy(first)
        second.sample()
        const_size.apply_rule(first, second)
        const_type.apply_rule(first, second)



        third = copy.deepcopy(second)
        third.sample()
        const_size.apply_rule(second, third)
        const_type.apply_rule(second, third)

        analog.insertAnalogie(first)
        analog.insertAnalogie(second)
        analog.insertAnalogie(third)

        candidates = create_candidates(analog, third)

        analog.insertAnswers(candidates)

        safeRootAsSingleImages(analog, i)
        safe_json(analog, i)
        safeRootAsCollage(analog, i)







    
# build_first_example_sample()




progression = Progression("corners")
progression.sample()


analog = Root([progression])

first = SingleImage()

first.insertComponent(Component())
first.insertComponent(Component())

first.sample()

second = copy.deepcopy(first)

second.sample()

progression.apply_rule(first, second)

third = copy.deepcopy(second)

third.sample()

progression.apply_rule(second, third)



analog.insertAnalogie(first)
analog.insertAnalogie(second)
analog.insertAnalogie(third)

candidates = create_candidates(analog, third)

analog.insertAnswers(candidates)

# analog.printLatex()

# analog.saveLatex("test_with_new_position")

safeRootAsSingleImages(analog, 1)
safe_json(analog, 1)
safeRootAsCollage(analog, 1)








