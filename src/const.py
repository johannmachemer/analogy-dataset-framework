

"""
    Consts
"""

"""
    ***Attributes***
"""

"""
    Size
"""
SIZE_MIN = 0.1
SIZE_MAX = 0.5
SIZE_PROGRESSIONS = [-0.2, -0.1, 0.1, 0.2]

"""
    Type
"""
TYPE_VALUES = ["Square", "Circle", "Star"]
TYPE_MIN = 0
TYPE_MAX = len(TYPE_VALUES) -1

"""
    Filling
"""
FILLING_MIN = 0.1
FILLING_MAX = 1
FILLING_PROGRESSIONS = [-0.2, -0.1, 0.1, 0.2]

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
POSITION_PROGRESSIONS = [-20, -10, 10, 20] # pixel numbers


"""
    ***Order of special progression***
"""

"""
    Corner order
"""
CORNER_ORDER = ["Circle", "Square", "Star"]

MIN_COMPONENTS = 2
MAX_COMPONENTS = 2
NUMBER_OF_SAMPLES = 10

STAR_PEAKS = 5

SAVE_INVALID_IMAGES = False
