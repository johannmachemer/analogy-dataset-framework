

"""
    Consts
"""

"""
    ***Attributes***
"""

"""
    Size
"""
SIZE_MIN = 0.2
SIZE_MAX = 0.6
SIZE_PROGRESSIONS = [-0.4, -0.2, -0.1, 0.1, 0.2, 0.4]

"""
    Type
"""
TYPE_VALUES = ["Square", "Circle", "Star"]
ALL_TYPE_VALUES = ["Square", "Circle", "Star", "Group"]
TYPE_MIN = 0
TYPE_MAX = len(TYPE_VALUES) -1

"""
    Filling
"""
FILLING_MIN = 0.1
FILLING_MAX = 1
FILLING_PROGRESSIONS = [-0.4, -0.2, -0.1, 0.1, 0.2, 0.4]

"""
    Rotation
"""
ROTATION_MIN = 0
ROTATION_MAX = 360
ROTATION_PROGRESSIONS = [15, 30, 45, 60, 75] # degrees

"""
    Image Size
"""
SINGLE_IMAGE_WIDTH = 224
SINGLE_IMAGE_HEIGHT = 224
POSITION_PROGRESSIONS = [-0.2, -0.1, 0.1, 0.2]


"""
    ***Order of special progression***
"""

"""
    Corner order
"""
CORNER_ORDER = ["Circle", "Square", "Star"]

MIN_COMPONENTS = 2
MAX_COMPONENTS = 5
MIN_PROGRESSIONS = 1
MAX_PROGRESSIONS = 3
MAX_DEPTH = 2
NUMBER_OF_SAMPLES = 10000

STAR_PEAKS = 5

SAVE_INVALID_IMAGES = False
