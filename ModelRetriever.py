import os
import mrcnn.model as modellib

from maskrcnn import coco


class ModelRetriever:

    def get_model(self, weights_path: str) -> object:
        """
        WICHTIG: Voraussetzung ist Tensorflow 1.14
        WICHTIG: Voraussetung ist masterport mask-rcnn
        -> pip install mask-rcnn-12rics
        :param weights_path: Pfad zu dem vortrainierten model
        :return: model
        """
        config = InferenceConfig()
        model_dir = os.path.abspath('./logs')
        coco_model = modellib.MaskRCNN(mode="inference", model_dir=model_dir, config=config)
        coco_model.load_weights(weights_path, by_name=True)

        return coco_model


class InferenceConfig(coco.CocoConfig):
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
