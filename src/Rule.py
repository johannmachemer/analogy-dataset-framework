import numpy as np

from const import (TYPE_VALUES, CORNER_ORDER)
from src.const import SIZE_PROGRESSIONS, FILLING_PROGRESSIONS, ROTATION_PROGRESSIONS, POSITION_PROGRESSIONS


class Rule:
    """ Superclass of all rules """

    def __init__(self, attr, params=[], component_idx=0):
        """Instantiate a rule.
            Args:
                attr (str): pre-defined name of the attribute where to apply the rule
                params (list): a list of possible params to sample for the progression value
                component_idx (int): index of the component to apply the rule to
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

    def __init__(self, attr, params = [], component_idx=0):
        super().__init__( attr, params, component_idx)

    def apply_rule(self, image_before, new_image):

        rule_component = new_image.components[self.component_idx]

        #apply progression
        if self.attr == "size":
            rule_component.size.value = rule_component.size.value + self.value
                
        if self.attr == "position":
            rule_component.position.value = rule_component.position.value + self.value * np.ones(2)

        if self.attr == "type":
            rule_component.type.value = self.value

        if self.attr == "filling":
            rule_component.filling.value = rule_component.filling.value + self.value

        if self.attr == "rotation":
            rule_component.rotation.value = rule_component.rotation.value + self.value

        return new_image

class Const(Rule):
    """ Rule for Const """

    def __init__(self, attr, params=[],component_idx=0):
        super().__init__( attr, params, component_idx)

    def sample(self):
        pass

    def apply_rule(self, image_before, new_image):
        rule_component_new = new_image.components[self.component_idx]
        rule_component_before = image_before.components[self.component_idx]

        #apply const
        if self.attr == "size":
            rule_component_new.size.value = rule_component_before.size.value
        if self.attr == "type":
            rule_component_new.type.value = rule_component_before.type.value
        if self.attr == "filling":
            rule_component_new.filling.value = rule_component_before.filling.value

        return new_image


        
        
        