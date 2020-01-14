# define the prediction configuration
from mrcnn.config import Config


class RiderConfig(Config):
    NAME = "rider_cfg"
    NUM_CLASSES = 1 + 2
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
    STEPS_PER_EPOCH = 1000
    VALIDATION_STEPS = 50
