import cv2
import os
from os import listdir
from os.path import isfile, join



def saveImages(img_dir,new_dir):
    path = os.path.normpath(img_dir)
    path=path.split(os.sep)
    img_dir_vid_name=path[-2]
    print(img_dir_vid_name)
    images = [f for f in listdir(img_dir) if isfile(join(img_dir, f))]
    for img in images:
        img_path=join(img_dir,img)
        #print(img_path)
        image=cv2.imread(img_path)
        new_img_path=join(new_dir,img_dir_vid_name+'_'+img)
        print(new_img_path)
        cv2.imwrite(new_img_path,image)

def saveCSV(db_dir,new_dir):
    path = os.path.normpath(db_dir)
    path = path.split(os.sep)
    vid_name = path[-3]
    print(vid_name)
    db = [f for f in listdir(db_dir) if isfile(join(db_dir, f))]
    for file in db:
        print(file)
        os.rename( (join(db_dir,file)),(join(db_dir,vid_name+'_'+file)))



if __name__ == '__main__':
    img_dir='C:\\Users\\Tabea\\Horse\\Horse_Detection\\rimondo_frames\\GP028294\\accepted_images'
    new_dir='C:\\Users\\Tabea\\Horse\\Horse_Detection\\rimondo_frames\\accepted_images'
    img_dir=os.path.normpath(img_dir)
    new_dir = os.path.normpath(new_dir)


    db_dir=join(img_dir,'annotations')
    new_db_dir=join(new_dir,'annotations')

    saveImages(img_dir,new_dir)
    saveCSV(db_dir,new_db_dir)
