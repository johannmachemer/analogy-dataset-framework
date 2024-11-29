from rendering import (safe_root_as_collage, safe_root_as_single_images)
from json_export import safe_json
from src.SampleGenerator import create_analogy_sample
from src.const import NUMBER_OF_SAMPLES, MIN_COMPONENTS, MAX_COMPONENTS


def build_random_samples():
    for id in range(0, NUMBER_OF_SAMPLES):
        analogy = create_analogy_sample()
        safe_root_as_single_images(analogy, id)
        safe_json(analogy, id)
        safe_root_as_collage(analogy, id)

build_random_samples()




