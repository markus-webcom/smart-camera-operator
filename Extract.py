import os
import pandas as pd
from os.path import join
import cv2
from numpy import zeros
from numpy import asarray
import math
from colab_code.RiderDetector import RiderDetector
from colab_code.BoundingBox import BoundingBox





def extract_boxes(img_path):
    dir_name = os.path.dirname(img_path)
    img_name = os.path.splitext(os.path.basename(img_path))[0]
    db_path = join(dir_name, 'annotations')
    db_path = join(db_path, img_name + '.csv')
    db_path = os.path.normpath(db_path)

    allEntries = pd.read_csv(db_path)

    img = cv2.imread(img_path)
    height = img.shape[0]
    width = img.shape[1]
    bbox = []
    for _, entry in allEntries.iterrows():

        x = entry["x"] * width
        y = entry["y"] * height
        w = entry["width"] * width
        h = entry["height"] * height
        # Eckpunkte bbox berechnen
        xmin = round(x - w // 2)
        xmax = round(x + w // 2)
        ymin = round(y - h // 2)
        ymax = round(y + h // 2)

        if entry["label"] == 1 or entry["label"] == 2:
            box = BoundingBox(xmin,xmax, ymin,  ymax,entry['label'])
            bbox.append(box)
    return bbox, height, width

def main(img_path):
    bbox,height,width=extract_boxes(img_path)
    print(height,width)
    img=cv2.imread(img_path)
    x_min=[]
    x_max=[]
    y_min=[]
    y_max=[]

    for box in bbox:
        box.printBBox()
        x_min.append(box.getX1())
        y_min.append(box.getY1())
        x_max.append(box.getX2())
        y_max.append(box.getY2())

        img = box.drawBBox(img)

    x1=max(0,min(x_min)-int(0.1*width))
    x2=min(width,max(x_max)+int(0.1*width))
    y1=max(0,min(y_min)-int(0.1*height))
    y2=min(height,max(y_max)+int(0.1*height))
    img=img[y1:y2, x1:x2]

    #img = cv2.resize(img, (0, 0), fx=0.35, fy=0.35)
    cv2.imshow('im', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    img='E:\\Videos\\accepted_images\\ZOOM0004_0_frame(80).png'
    img3='E:\\Videos\\Ausschnitte2\\accepted_images\\outdoor4_frame(32).png'
    img2='C:\\Users\\Tabea\\Horse\\Rider_Dataset\\accepted_images\\GOPR8291_00017.png'

    img4='E:\\Bilder\\accepted_images\\image (76).png'

    main(img3)