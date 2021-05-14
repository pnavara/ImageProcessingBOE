import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('D435/walk.png')
# img = cv2.imread('L515/walk.png')
mask = np.zeros(img.shape[:2],np.uint8)

bgdModel = np.zeros((1,65),np.float64)
fgdModel = np.zeros((1,65),np.float64)

# newmask is the mask image I manually labelled
newmask = cv2.imread('D435/walkm.png',0)


# whereever it is marked white (sure foreground), change mask=1
# whereever it is marked black (sure background), change mask=0
mask = np.where(((newmask>0) & (newmask<255)),cv2.GC_PR_FGD,0).astype('uint8')
mask[newmask == 0] = 0 #black
mask[newmask == 255] = 1 #white

cv2.grabCut(img,mask,None,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_MASK)
mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
img2 = img*mask2[:,:,np.newaxis]

# to find horizontal displacement
result = np.where(mask2[150] == 1)

# font
font = cv2.FONT_HERSHEY_SIMPLEX

# org
org = (10, 30)

# fontScale
fontScale = 1

# Blue color in BGR
color = (255, 0, 0)

# Line thickness of 2 px
thickness = 2
# text = 'Width: ' + str(euclid)
# text = 'Pixel Distance: ' + str(euclid)
# Using cv2.putText() method
# img3 = cv2.putText(img2, text, org, font,
#                     fontScale, color, thickness, cv2.LINE_AA)

def mousePoint(event, x, y, flags, params):
    h, w, c = img.shape
    global x_star, x_end, y_start, y_end, width, mInInches
    # if event == cv2.EVENT_LBUTTONDOWN:
    #     cv2.line(img, pt1=(0, y), pt2=(x,2000), color=(0, 0, 255), thickness=10)
    #     print(x, y)
    #     # print(h,w,c)
    # if event == cv2.EVENT_LBUTTONUP:
    #     print(x,y)
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img2, (x, y), 3, (0, 0, 255), 3, cv2.FILLED)
        print(x, y)
        x_star = x
        y_start = y
        # print(x_star, y_start)
        # points.append((x, y))
        # if len(points) >= 2:

        cv2.line(img2, pt1=(x, y), pt2=(2000, y), color = (255, 0, 0), thickness=1)
        # cv2.circle(img2, (x, y), 3, (0, 0, 255), 3, cv2.FILLED)
        cv2.line(img2, pt1=(x, y), pt2=(x, 2000), color=(255, 0, 0), thickness=1)
        cv2.imshow('Image', img2)
        # print(h, w, c)
    elif event == cv2.EVENT_RBUTTONDOWN:
        cv2.circle(img2, (x, y), 3, (0, 0, 255), 3, cv2.FILLED)
        cv2.line(img2, pt1=(x, y), pt2=(x, 2000), color=(255, 0, 0), thickness=1)
        # points.clear()
        print(x, y)


# plt.subplot(231),plt.imshow(img)
# plt.title('Original'), plt.xticks([]), plt.yticks([])
# plt.subplot(232),plt.imshow(mask2,cmap = 'gray')
# plt.title('mask'), plt.xticks([]), plt.yticks([])
# plt.subplot(231),plt.imshow(img2,cmap = 'gray')
# plt.title('Image'), plt.xticks([]), plt.yticks([])
# plt.subplot(234),plt.imshow(newmask,cmap='gray')
# plt.title('Manually Masked'), plt.xticks([]), plt.yticks([])
# plt.subplot(234),plt.imshow(newmask,cmap='gray')
# plt.title('Manually Masked'), plt.xticks([]), plt.yticks([])

#fit to screen
screen_res = 1280, 720
scale_width = screen_res[0] / img.shape[1]
scale_height = screen_res[1] / img.shape[0]
scale = min(scale_width, scale_height)
#resized window width and height
window_width = int(img.shape[1] * scale)
window_height = int(img.shape[0] * scale)

cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Image', window_width, window_height)

cv2.imshow('Image', img2)
# points = []
cv2.setMouseCallback('Image', mousePoint)
cv2.waitKey(0)
plt.show()