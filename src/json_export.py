import os
from Tree import (Root,Component)
import json


def component_to_json(idx, component:Component):
    component_dict = {}
    component_dict["component_id"] = idx
    component_dict["type"] = component.type.get_value()
    component_dict["size"] = component.size.get_value()
    component_dict["position"] = component.position.get_value()
    
    return component_dict


def single_image_to_json(idx, child):
    single_image_dict = {}
    
    single_image_dict["img_id"] = idx
    single_image_dict["components"] = []


    for (component_idx, component) in enumerate(child.components):
        single_image_dict["components"].append(component_to_json(component_idx, component))

    return single_image_dict
    

def safe_json(root:Root, analogie_id,):
    root_dict = {}

    meta_dict = {}

    meta_dict["id"] = analogie_id

    root_dict["meta"] = meta_dict

    root_dict["rules"] = []

    for(rule_idx, rule) in enumerate(root.getRules()):
        rule_dict = {}
        rule_dict["rule_id"] = rule_idx
        rule_dict["rule_type"] = rule.__class__.__name__
        rule_dict["component_idx"] = rule.component_idx
        rule_dict["attr"] = rule.attr
        root_dict["rules"].append(rule_dict)

    analogie_list = []

    for (idx,child) in enumerate(root.children_analogie):
        
        analogie_list.append(single_image_to_json(idx, child))


    root_dict["analogie"] = analogie_list

    answer_list = []

    for (idx,child) in enumerate(root.children_answer):
        
        answer_list.append(single_image_to_json(idx + len(root.children_analogie), child))

    root_dict["candidates"] = answer_list
    	
    if not os.path.isdir("data"):
        os.mkdir("data")
        

    with open(f"data/{analogie_id}/{analogie_id}.json", "w") as f:
        json.dump(root_dict, f)





