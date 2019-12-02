import random
import os
from os.path import join

import subprocess
import sys


def split_data_set(image_dir):
    print("func")
    f_val = open("test.txt", 'a+')
    f_train = open("train.txt", 'a+')

    path, dirs, files = next(os.walk(image_dir))
    data_size = len(files)
    print(data_size)

    ind = 0
    data_test_size = int(0.1 * data_size)
    test_array = random.sample(range(data_size), k=data_test_size)

    for f in os.listdir(image_dir):
        print(f)
        ind += 1
        path = join(image_dir, f)

        if ind in test_array:
            f_val.write(path + '\n')
        else:
            f_train.write(path + '\n')
    f_val.close()
    f_train.close()


def main():
    print("python main function")
    FRAME_SOURCE = "..\\rimondo_frames"
    videos = [d for d in os.listdir(FRAME_SOURCE) if os.path.isdir(join(FRAME_SOURCE, d))]
    print(len(videos))
    for v in videos:
        video_path = join(FRAME_SOURCE, v)
        split_data_set(video_path)


if __name__ == '__main__':
    main()
