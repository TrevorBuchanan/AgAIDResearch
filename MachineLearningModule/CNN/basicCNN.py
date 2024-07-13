from mrcnn.config import Config
from mrcnn import model as modellib
from mrcnn import utils

class CustomConfig(Config):
    NAME = "custom_object"
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
    NUM_CLASSES = 1 + 1  # Background + Your class
    STEPS_PER_EPOCH = 100
    VALIDATION_STEPS = 50


model = modellib.MaskRCNN(mode="training", config=CustomConfig(), model_dir="./logs")
model.load_weights('path_to_pretrained_weights.h5', by_name=True,
                   exclude=["mrcnn_class_logits", "mrcnn_bbox_fc", "mrcnn_bbox", "mrcnn_mask"])
