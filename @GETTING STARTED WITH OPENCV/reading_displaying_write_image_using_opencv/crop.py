import cv2
import numpy as np

import os

# os.chdir("@GETTING STARTED WITH OPENCV/reading_displaying_write_image_using_opencv")

img = cv2.imread(r"celda.png")
print(f"Original Image Shape: {img.shape}")

h, w, c = img.shape
print(f"Height: {h}, Width: {w}, Channels: {c}")

imgResize = cv2.resize(img, (w // 2, h // 2))
print(f"Resized Image Shape: {imgResize.shape}")

# x0, y0 = 647, 238
# x1, y1 = 773, 403

# imgCropped = img[238:403, 647:773]

cv2.imshow("Image", img)
# cv2.imshow("Image Resize",imgResize)
# cv2.imshow("Image Cropped",imgCropped)

state = 0
x0, y0 = 0, 0
x1, y1 = 0, 0
imgCropped = img.copy()
img1 = img.copy()


def click_event(event, x, y, flags, param):
    global state, x0, y0, x1, y1, img, imgCropped
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)
        # plot the points on the image
        cv2.circle(img1, (x, y), 3, (0, 0, 255), -1)
        cv2.imshow("Image", img1)

        if state == 0:
            x0, y0 = x, y
            state = 1
            print("New State:", state)
        elif state == 1:
            if x < x0:
                x0, x = x, x0
            if y < y0:
                y0, y = y, y0

            x1, y1 = x, y
            state = 0
            print("New State:", state)
            imgCropped = imgCropped[y0:y1, x0:x1]
            cv2.imshow("Image Cropped", imgCropped)
            imgCropped = img.copy()


cv2.setMouseCallback("Image", click_event)

try:
    while True:
        if cv2.waitKey(10) & 0xFF == ord("q") or cv2.waitKey(10) & 0xFF == 27:
            break
except:
    print("Interrupted by user")

cv2.destroyAllWindows()
