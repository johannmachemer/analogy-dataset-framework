from Tree import (Root,Component)
import json


def to_json(root:Root, filename="analogies.json"):
    root_dict = {}

    root_dict["rules"] = []

    for(rule_idx, rule) in enumerate(root.getRules()):
        rule_dict = {}
        rule_dict["component_idx"] = rule.component_idx
        rule_dict["attr"] = rule.attr
        root_dict["rules"].append(rule_dict)

    analogie_list = []

    for child in root.children_analogie:
        single_image_dict = {}
        
        single_image_dict["components"] = []

        for component in child.components:
            
            component_dict = {}
            component_dict["type"] = component.type.get_value()
            component_dict["size"] = component.size.get_value()
            component_dict["position"] = component.position.get_value()
            single_image_dict["components"].append(component_dict)        
        analogie_list.append(single_image_dict)


    root_dict["analogie"] = analogie_list

    anser_list = []

    for child in root.children_answer:
        single_image_dict = {}
        
        single_image_dict["components"] = []

        for component in child.components:
            
            component_dict = {}
            component_dict["type"] = component.type.get_value()
            component_dict["size"] = component.size.get_value()
            component_dict["position"] = component.position.get_value()
            single_image_dict["components"].append(component_dict)        
        anser_list.append(single_image_dict)

    root_dict["candidates"] = anser_list



    with open(filename, "w") as f:
        json.dump(root_dict, f)
            


