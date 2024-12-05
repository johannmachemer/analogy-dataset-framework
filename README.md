# Analogies Dataset

## Create Dataset
The following flow chart should visualize how to create a dataset:
[Flow chart to visualize process](https://gitlab.isp.uni-luebeck.de/Johann.Machemer/analogies-dataset/-/wikis/uploads/fcb2274be710465463290c25fabe86a3/analogies-flow-chart.pdf)

## How to extend

### Add New Rule
When you want to add a new rule, you have to extend the code at the following places:
- create Rule subclass in src/Rule.py
- add creation of this rule in feasible_rules function in src/SampleGenerator.py  
- consider to use or create a similar methode as the determine_feasible_rule_parameter methods from Component classes

Please pay attention to adding a behavior for every attribute inside the apply_rule function.

### Add New Attribute
When you want to add a new attribute, you have to extend the code at the following places:
- extends enum KindOfAttributes
- create an Attribute subclass in src/Attribute.py
- consider to add attribute bounding parameters to src/const.py
- add behavior for new attribute to all existing rules in src/Rules.py
- add creation of rules with this attribute in function feasible_rules in src/SampleGenerator.py  
- add attribute in sample function of a component in src/components/Component.py to initial the attribute
- add attribute to the draw function in every Component implementing class in package src/components 
- export attribute into json data by src/json_export.py
- import attribute from json data into binaries by src/json_importer.py 

### Add New Component
When you want to add a new component, you have to extend the code at the following places:
- Add new class in package src/components that extends Component class
  - draw method has to implemented
  - \_\_init__ method should perhaps be individualized
  - consider to override the determine_feasible_rule_parameter in order to prevent infeasible progressions on this components 
- in order to create initially this component:
  - extends ALL_TYPE_VALUES in src/const.py 
  - extends create_component method in src/SampleGenerator.yp 
- in order to allow the progression rules modifying components into this component
  - extends TYPE_VALUES in src/const.py
  - extends apply_rule method in class Progression in src/Rule.py 


## Documentation


### Python docs
You can find Python docs in the repository: docs/src

Created/Updated with: `$ pdoc --html .  --output-dir docs `
from the project root folder.






