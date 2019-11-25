import numpy as np
import cv2 as opencv


class SeamCarver:

    def __init__(self, image: np.array):
        self.image = image

    def compute(self) -> np.array:
        return self.medianFilter()

    def remove(self) -> np.array:
        print('remove seam called!')

    def middleFilter(self):
        f = self.convertToGray()
        n, m = f.shape
        for i in range(1, n - 1):
            for j in range(1, m - 1):
                f[i, j] = (f[i, j] + f[i, j + 1] + f[i, j - 1] + f[i - 1, j] + f[i - 1, j - 1] +
                           f[i - 1, j + 1] + f[i + 1, j] + f[i + 1, j + 1] + f[i + 1, j - 1]) // 9

        return np.array(f, np.uint8)

    def medianFilter(self):
        f = self.convertToGray()
        n, m = f.shape
        for i in range(1, n - 1):
            for j in range(1, m - 1):
                f[i, j] = np.median(np.array([f[i, j], f[i, j + 1], f[i, j - 1], f[i - 1, j], f[i - 1, j - 1],
                                              f[i - 1, j + 1], f[i + 1, j], f[i + 1, j + 1], f[i + 1, j - 1]],
                                             np.uint16))

        return np.array(f, np.uint8)

    def convertToGray(self):
        # uint16 wegen arithmetic overflow
        return np.array(opencv.cvtColor(self.image, opencv.COLOR_BGR2GRAY), np.uint16)
