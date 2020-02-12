import cv2
class BoundingBox:
    def __init__(self,x1,x2,y1,y2,class_id):
        self.x1= x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.class_id=class_id

    def getX1(self):
        return self.x1

    def getX2(self):
        return self.x2

    def getY1(self):
        return self.y1

    def getY2(self):
        return self.y2

    def getClassId(self):
        return self.class_id

    # scale bbox with scale_factor >0
    def scale_bbox(self,scale):
        self.x1 *=  scale
        self.x2 *= scale
        self.y1 *= scale
        self.y2 *= scale

    # draw BBox on a frame
    def drawBBox(self, image):
        # cv2 colors are in BGR instead of RGB
        colors = {0: (0, 255, 2550), 1: (0, 0, 255), 2: (255, 255, 0), 3: (255, 0, 0)}
        start_point=(int(self.getX1()), int(self.getY1()))
        end_point=(int(self.getX2()), int(self.getY2()))
        pixelsum=image.shape[0]+image.shape[1]
        line_thickness=1
        if(pixelsum>1000):
            line_thickness=5
        elif(pixelsum>1500):
            line_thickness=8
        elif(pixelsum>2000):
            line_thickness=12


        img = cv2.rectangle(image, start_point, end_point, colors[self.getClassId()], line_thickness)
        return img

    def printBBox(self):
        print('x1:',self.getX1(),'x2:',self.getX2(),'y1:',self.getY1(),'y2:',self.getY2(),'class_id:',self.getClassId())

