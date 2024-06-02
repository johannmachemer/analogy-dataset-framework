from Attribute import Size
from Rule import (Progression,Const)
from Tree import Root
from Tree import SingleImage
from Tree import Component
import copy
from PIL import Image, ImageDraw
import random
from rendering import renderRoot


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

renderRoot(analog)








