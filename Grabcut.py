import numpy as np
import cv2
from matplotlib import pyplot as plt


class Grabcut:

    def grabC(self, img):
        mask = np.zeros(img.shape[:2], np.uint8)

        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)

        #this is with the rectangle method, you'll need to manually input your own rect parameters
        # rect = (544, 170, 300, 310)
        # cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
        #
        # mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
        # img3 = img * mask2[:, :, np.newaxis]

        # .............................
        # newmask is the mask image I manually labelled
        # newmask = cv2.imread('images/sidewalk31.png', 0)
        newmask = cv2.imread('images/d435colored_4_masked.png', 0)

        mask = np.where(((newmask > 0) & (newmask < 255)), cv2.GC_PR_FGD, 0).astype('uint8')

        # whereever it is marked white (sure foreground), change mask=1
        # whereever it is marked black (sure background), change mask=0
        mask[newmask == 0] = 0
        mask[newmask == 255] = 1

        mask, bgdModel, fgdModel = cv2.grabCut(img, mask, None, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_MASK)

        mask = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
        img2 = img * mask[:, :, np.newaxis]

        return img2

    def GC(self, img):
        image = self.grabC(img)
        return image

