import os
import skimage.io
from mrcnn import utils
import mrcnn.model as modellib
from mrcnn import visualize
from maskrcnn import coco
import cv2


class InferenceConfig(coco.CocoConfig):
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1


def get_model(weights_path: str) -> object:
    """
    WICHTIG: Voraussetzung ist Tensorflow 1.14
    WICHTIG: Voraussetung ist masterport mask-rcnn
    -> pip install mask-rcnn-12rics
    :param weights_path: Pfad zu dem vortrainierten model
    :return: model
    """
    model_dir = os.path.abspath('./logs')
    coco_model = modellib.MaskRCNN(mode="inference", model_dir=model_dir, config=config)
    coco_model.load_weights(weights_path, by_name=True)
    return coco_model


def print_classnames(annotations_path: str):
    """
    Wichtig: Voraussetzung sind genau die (keine anderen!) ms coco annotations
        2014 Train/Val annotations [241MB]
        http://cocodataset.org/#download
    :param annotations_path: Pfad zu dem Verzeichnis, in dem die annotations liegen
    :return:
    """
    dataset = coco.CocoDataset()
    dataset.load_coco(annotations_path, "train")
    dataset.prepare()
    print(dataset.class_names)


def get_classnames() -> list:
    return ['BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane',
            'bus', 'train', 'truck', 'boat', 'traffic light',
            'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird',
            'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear',
            'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie',
            'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
            'kite', 'baseball bat', 'baseball glove', 'skateboard',
            'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
            'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
            'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
            'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed',
            'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote',
            'keyboard', 'cell phone', 'microwave', 'oven', 'toaster',
            'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
            'teddy bear', 'hair drier', 'toothbrush']


def download_coco_model_if_needed():
    if not os.path.exists(WEIGHTS_PATH):
        utils.download_trained_weights(WEIGHTS_PATH)


def getBboxes(imagepath):
    im = cv2.imread(imagepath)
    results = model.detect([image], verbose=0)
    r = results[0]
    # extract ids and bboxes for riders
    rois = r['rois']
    ids = []
    bbox = []
    counter = -1
    #filter boxes to only detect horse and person
    for i in r['class_ids']:
        counter += 1
        if i == get_classnames().index('horse') or i == get_classnames().index('person'):
            ids.append(i)
            bbox.append(rois[counter])
    # cut pictures here
    drawBox(imagepath,bbox)
    return ids, bbox


def drawBox(image, bbox):
    im = cv2.imread(image)
    for b in bbox:
        y1=b[0]
        x1=b[1]
        y2=b[2]
        x2=b[3]



        im[y1:y2, x1:x1+5] = (0, 0, 0)
        im[y1:y2, x2:x2 + 5] = (0, 0, 0)
        im[y1:y1+5, x1:x2] = (0, 0, 0)
        im[y2:y2 + 5, x1:x2] = (0, 0, 0)
    im = cv2.resize(im,None,fx=0.3,fy=0.3)
    cv2.imshow('title', im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


ANNOTATIONS_PATH = os.path.abspath('./coco')
# IMAGE_PATH = os.path.abspath('./pferde_bilder/00019.png')
IMAGE_PATH = "D:\\Programming\\rimondo_frames\\GOPR8291\\00167.png"
WEIGHTS_PATH = os.path.abspath('mask_rcnn_coco.h5')

# download_coco_model_if_needed()

config = InferenceConfig()
# config.display()
model = get_model(WEIGHTS_PATH)
# print_classnames(ANNOTATIONS_PATH)
classnames = get_classnames()

image = cv2.imread(IMAGE_PATH)
results = model.detect([image], verbose=0)

# Visualize results
r = results[0]

getBboxes(IMAGE_PATH)
# visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'], classnames, r['scores'])
