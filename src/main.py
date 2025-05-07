from rendering import (safe_root_as_collage, safe_root_as_single_images)
from json_export import safe_json
from src.SampleGenerator import create_analogy_sample, validate_image
from src.const import NUMBER_OF_SAMPLES, MIN_COMPONENTS, MAX_COMPONENTS
from src.json_importer import import_json, import_json_image
from src.raven_format_exporter import write_sample
from tqdm import tqdm


def build_random_samples():
    for id in tqdm(range(0, NUMBER_OF_SAMPLES), desc="Samples generated"):
        analogy = create_analogy_sample()
        safe_root_as_single_images(analogy, id)
        safe_json(analogy, id)
        safe_root_as_collage(analogy, id)
        write_sample(analogy, id)

build_random_samples()

#image = import_json_image("data\\invalid\\1.json")
#print(validate_image(image))
#for image in sample.analogy:
#    print(validate_image(image))
#for image in sample.candidates:
#    print(validate_image(image))

