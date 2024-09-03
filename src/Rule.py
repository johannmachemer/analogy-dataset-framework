import numpy as np
import copy

from const import (TYPE_VALUES)

class Rule():
    """ Superclass of all rules """

    def __init__(self, attr, params, component_idx=0):
        """Instantiate a rule.
            Args:
                attr (str): pre-defined name of the attribute where to apply the rule
                params (list): a list of possible params to sample for the progressionn value
                component_idx (int): index of the component to apply the rule to
        """
        self.attr = attr
        self.params = params
        self.component_idx = component_idx

    def apply_rule(self):
        pass

    def sample(self):
        self.value = np.random.choice(self.params)


class Progression(Rule):
    """ Rule for progression """

    def __init__(self, attr, params, component_idx=0):
        super().__init__( attr, params, component_idx)

    def apply_rule(self, image_before, new_image):
        rule_component_new = new_image.components[self.component_idx]
        rule_component_before = image_before.components[self.component_idx]

        #apply progression
        if self.attr == "size":
            # check if progression is possible and size will not be the whole image
            if(rule_component_before.size.value + self.value < 1):
                rule_component_new.size.value = rule_component_before.size.value + self.value
            else:
                rule_component_new.size.value = rule_component_before.size.value
                
        if self.attr == "type":
            rule_component_new.type.level = (rule_component_before.type.level+self.value) % len(TYPE_VALUES)
            rule_component_new.type.value = TYPE_VALUES[rule_component_new.type.level]

        if self.attr == "filling":
            if(rule_component_before.filling.value + self.value < 1):
                rule_component_new.filling.value = rule_component_before.filling.value + self.value
            else:
                rule_component_new.filling.value = rule_component_before.filling.value

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


        
        
        