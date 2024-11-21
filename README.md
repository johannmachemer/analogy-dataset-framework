# Analogies Dataset

## Create Dataset
The following flow chart should visualize how to create a dataset:
[Flow chart to visualize process](https://gitlab.isp.uni-luebeck.de/Johann.Machemer/analogies-dataset/-/wikis/uploads/fcb2274be710465463290c25fabe86a3/analogies-flow-chart.pdf)

## How to extend

### Add New Rule
When you want to add a new rule, you have to extend the code at the following places:
- Create Rule subclass in src/Rule.py

Please pay attention to adding a behavior for every attribute inside the apply_rule function.

### Add New Attribute
When you want to add a new attribute, you have to extend the code at the following places:
- Create an Attribute subclass in src/Attribute.py
- consider to add attribute parameters to src/const.py
- add behavior for new attribute to all existing rules in src/Rules.py
- add new attribute to the render function in src/rendering.py
- add attribute in sample function of a component in src/Tree.py


## Documentation


### Python docs
You can find Python docs in the repository: docs/src

Created/Updated with: `$ pdoc --html .  --output-dir docs `
from the project root folder.






