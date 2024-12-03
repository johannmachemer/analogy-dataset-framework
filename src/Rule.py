import numpy as np

from const import (TYPE_VALUES, CORNER_ORDER)
from src.components.Circle import Circle
from src.components.Square import Square
from src.components.Star import Star
from src.const import SIZE_PROGRESSIONS, FILLING_PROGRESSIONS, ROTATION_PROGRESSIONS, POSITION_PROGRESSIONS


class Rule:
    """ Superclass of all rules """

    def __init__(self, attr, params=[], component_idx=0):
        """Instantiate a rule.
            Args:
                attr (str): pre-defined name of the attribute where to apply the rule
                params (list): a list of possible params to sample for the progression value
                component_idx (str): unique index of the component to apply the rule to
        """
        self.attr = attr
        self.params = params
        self.component_idx = component_idx
        self.value = None

    def apply_rule(self, image_before, new_image):
        """
        apply rule on single image

        Args:
            image_before (SingleImage): the image where the rule is being applied
            new_image (SingleImage): the image where the applied rule is saved in

        Returns:
            new_image(SingleImage): the new image with applied rules
        """
        pass

    def sample(self):
        """
        sample the value of the rule
        """
        if len(self.params) == 0:
            if self.attr == "size":
                self.params = SIZE_PROGRESSIONS
            elif self.attr == "position":
                self.params = POSITION_PROGRESSIONS
            elif self.attr == "type":
                self.params = TYPE_VALUES
            elif self.attr == "filling":
                self.params = FILLING_PROGRESSIONS
            elif self.attr == "rotation":
                self.params = ROTATION_PROGRESSIONS
            else:
                raise ValueError
        self.value = np.random.choice(self.params)



class Progression(Rule):
    """ Rule for progression """

    def __init__(self, attr, params, component_idx):
        super().__init__( attr, params, component_idx)

    def apply_rule(self, image_before, new_image):

        rule_component = new_image.get_component_by_identifier(self.component_idx)

        #apply progression
        if self.attr == "size":
            rule_component.add_size(self.value)
                
        if self.attr == "position":
            rule_component.add_position(self.value * np.ones(2))

        if self.attr == "type":
            if self.value == "Circle":
                new_component = Circle(rule_component.component_identifier, previous_version= rule_component)
            elif self.value == "Square":
                new_component = Square(rule_component.component_identifier, previous_version= rule_component)
            elif self.value == "Star":
                new_component = Star(rule_component.component_identifier, previous_version= rule_component)
            else:
                raise ValueError

            superior_components = rule_component.superior_component.components
            index = superior_components.index(rule_component)
            superior_components[index] = new_component

        if self.attr == "filling":
            rule_component.add_filling(self.value)

        if self.attr == "rotation":
            rule_component.add_rotation(self.value)

        return new_image
