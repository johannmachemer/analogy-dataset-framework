import os
from Tree import (AnalogySample, Component)
import json



def component_to_json(idx, component:Component):

    """
        convert single component to json

        Args:
            idx (int): index of the component inside of single image
            component (Component): the component to convert
    """

    component_dict = {}
    component_dict["component_id"] = idx
    component_dict["type"] = component.type.get_value()
    component_dict["size"] = component.size.get_value()
    component_dict["position"] = component.position.get_value().tolist()
    component_dict["rotation"] = str(component.rotation.get_value())
    component_dict["filling"] = component.filling.get_value()

    return component_dict


def single_image_to_json(idx, child):
    """
    convert single image to json

    Args:
        idx (int): index of the single image inside of the root
        child (SingleImage): the single image to convert
    """
    single_image_dict = {}

    single_image_dict["img_id"] = idx
    single_image_dict["components"] = []


    for (component_idx, component) in enumerate(child.components):
        single_image_dict["components"].append(component_to_json(component_idx, component))

    return single_image_dict
    

def safe_json(sample:AnalogySample, analogy_id:int):
    """
    convert sample to json

    Args:
        sample (AnalogySample): root to convert
        analogy_id (int): id of the analogy to convert
    """
    root_dict = {}

    meta_dict = {}

    meta_dict["id"] = analogy_id

    root_dict["meta"] = meta_dict

    root_dict["rules"] = []

    for(rule_idx, rule) in enumerate(sample.get_rules()):
        rule_dict = {}
        rule_dict["rule_id"] = rule_idx
        rule_dict["rule_type"] = rule.__class__.__name__
        rule_dict["component_idx"] = rule.component_idx
        rule_dict["attr"] = rule.attr
        rule_dict["value"] = str(rule.value)
        root_dict["rules"].append(rule_dict)

    analogy = []

    for (idx,child) in enumerate(sample.analogy):
        
        analogy.append(single_image_to_json(idx, child))


    root_dict["analogy"] = analogy

    answer_list = []

    for (idx,child) in enumerate(sample.candidates):
        
        answer_list.append(single_image_to_json(idx + len(sample.analogy), child))

    root_dict["candidates"] = answer_list
    	
    if not os.path.isdir("data"):
        os.mkdir("data")
        

    with open(f"data/{analogy_id}/{analogy_id}.json", "w") as f:
        json.dump(root_dict, f, indent=4)





