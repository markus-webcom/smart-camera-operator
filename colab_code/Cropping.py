from colab_code.BoundingBox import BoundingBox
# Cutting of frames according to the rider
class Cropping:
    def __init__(self):
        pass

        # crop one frame

    # Main Control-Flow for a Bbox
    # Input:    Bboxes  List of Bboxes
    # Return:   A final cropped Bbox for the output image
    def complete_bbox(self, frame, bboxes):
        sizeX = 1280  # HD
        sizeY = 720
        pair_list = list()

        pair_list = self.filter_riderhorseoverlap(bboxes)   # Calc all paires
        box = self.filter_boxes_pairs(frame, pair_list)     # Create one big Bbox which should contain all horse pairs
        box = self.calculate_box(box, sizeX, sizeY, frame)  # Create final crop points

        return box

    # Compares all horses with all riders. Checks if the pair overlaps
    # Input:    box_list    Bbox-List which contains rider and horses (with ids)
    # Returns:  pair_list   List of Horse/Rider tuples that overlap
    def filter_riderhorseoverlap(self, box_list):
        rider_list = list()
        horse_list = list()
        pair_list = list()

        # Seperate Rider/Horses into different lists
        for Obj in box_list:
            if Obj.getClassId() == 1:
                horse_list.append(Obj)
            if Obj.getClassId() == 2:
                rider_list.append(Obj)

        # Compare every horse with every rider in the current Frame
        # If their bboxes match, return the combined pair
        for horse in horse_list:
            for rider in rider_list:
                overlapping = True
                if horse.getX1() > rider.getX2() or horse.getX2() < rider.getX1():
                    overlapping = False

                if horse.getY1() > rider.getY2() or horse.getY2() < rider.getY1():
                    overlapping = False

                if overlapping:
                    pair_list.append((horse, rider))
        return pair_list

    # Creates one Big Bbox from multiple smaller bboxes (Max/Min)
    # Input:    Frame:      For default maximal bbox)
    #           box_list:   List of bboxes
    # Return:   box         One Big Bbox which contains all pairs
    def filter_boxes(self, frame, box_list):
        if len(box_list) == 0:
            height = frame.shape[0]
            width = frame.shape[1]
            calculated_box = BoundingBox(0,height, 0, width, 0)  # Creates a Bbox
        else:
            # collect all x, y values
            X1arr = list()
            Y1arr = list()
            X2arr = list()
            Y2arr = list()

            for j in box_list:
                X1arr.append(j.getX1())
                Y1arr.append(j.getY1())
                X2arr.append(j.getX2())
                Y2arr.append(j.getY2())

            X1 = min(X1arr)
            Y1 = min(Y1arr)
            X2 = max(X2arr)
            Y2 = max(Y2arr)
            calculated_box = BoundingBox(X1,X2,Y1,Y2,0)
        return calculated_box

    # Creates one Big Bbox from all smaller boxes within all pair (Max/Min)
    # Input:    Frame:      For default maximal bbox)
    #           pair_list:   Horse/Rider Pairs
    # Return:   box         One Big Bbox which contains all pairs
    def filter_boxes_pairs(self, frame, pair_list):
        if len(pair_list) == 0:
            height = frame.shape[0]
            width = frame.shape[1]
            calculated_box = BoundingBox(0,height, 0, width, 0)  # Creates a Bbox
        else:
            # collect all x, y values
            X1arr = list()
            Y1arr = list()
            X2arr = list()
            Y2arr = list()
            # for every pair in pair_list
            for i in pair_list:
                # for every object in a pair (2 objects)
                for j in i:
                    X1arr.append(j.getX1())
                    Y1arr.append(j.getY1())
                    X2arr.append(j.getX2())
                    Y2arr.append(j.getY2())

            X1 = min(X1arr)
            Y1 = min(Y1arr)
            X2 = max(X2arr)
            Y2 = max(Y2arr)
            calculated_box = BoundingBox(X1,X2,Y1,Y2,0)
        return calculated_box

    # consider borders and ratio of frames for cropping
    def calculate_box(self, box, sizeX, sizeY, img):
        X1 = box.getX1()
        Y1 = box.getY1()
        X2 = box.getX2()
        Y2 = box.getY2()

        TotalYPixels = Y2 - Y1  # Total amount of pixels of the bounding box in Y direction
        TotalXPixels = X2 - X1
        TotalYPixels = 1.2 * TotalYPixels
        TotalXPixels = 1.2 * TotalXPixels

        # Apply Ratio to the BBox total pixel size
        if (TotalXPixels > TotalYPixels):
            # Dont let the cropped pic be too small
            if TotalXPixels < 800: TotalXPixels = 800
            XRatio = sizeX / TotalXPixels
            YRatio = sizeY / XRatio
            TotalYPixels = YRatio  # Total amount of pixel of the bounding box in X direction
        else:
            # Dont let the cropped pic be too small
            if TotalYPixels < 450: TotalYPixels = 450
            YRatio = sizeY / TotalYPixels
            XRatio = sizeX / YRatio
            TotalXPixels = XRatio  # Total amount of pixel of the bounding box in X direction

        # Calculate optimal Crop points to maintain ratio
        CropX1 = ((X2 + X1) / 2) - (TotalXPixels / 2)  # Defines the left most pos to crop the pic
        CropX2 = ((X2 + X1) / 2) + (TotalXPixels / 2)  # Defines the right most pos to crop the pic
        CropY1 = ((Y2 + Y1) / 2) - (TotalYPixels / 2)  # Defines the top most pos to crop the pic
        CropY2 = ((Y2 + Y1) / 2) + (TotalYPixels / 2)  # Defines the bottom most pos to crop the pic

        # Out of Bounds check
        if CropX1 < 0:  # If we are out of bounds to the left side, adjust both X pos to the right
            CropX2 += -1 * CropX1
            CropX1 = 0

        if CropX2 > img.shape[1]:  # If we are out of bounds to the right side, adjust both X pos to the left
            CropX1 += (img.shape[1] - CropX2)
            CropX2 = img.shape[1]

        if CropY1 < 0:  # If we are out of bounds to the upper side, adjust both Y pos down
            CropY2 += -1 * CropY1
            CropY1 = 0

        if CropY2 > img.shape[0]:  # If we are out of bounds to the lower side, adjust both Y pos up
            CropY1 += (img.shape[0] - CropY2)
            CropY2 = img.shape[0]

        CropX1 = int(CropX1)
        CropX2 = int(CropX2)
        CropY1 = int(CropY1)
        CropY2 = int(CropY2)
        return BoundingBox(CropX1, CropX2, CropY1, CropY2, 0)

    # Crops an image by a given bbox
    def crop_image(self, box, img):
        X1 = box.getX1()
        Y1 = box.getY1()
        X2 = box.getX2()
        Y2 = box.getY2()
        img = img[Y1:Y2, X1:X2]
        return img


        # crop list of frames

    # Crops all Frames with their respective calculated BBoxes
    # Input:    frames              Array of all frames of a given video
    #           calculated_boxes    List of final cropped bboxes for every frame
    # Reutrn:   cropped_frames      List of final cropped frames
    def crop_image_list(self, calculated_boxes, frames):
        cropped_frames = list()
        for i in range(len(frames)):
            cropped_frames.append(self.crop_image(calculated_boxes[i], frames[i]))
        return cropped_frames
