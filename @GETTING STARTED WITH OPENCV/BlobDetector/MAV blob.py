#!/usr/bin/python

# Standard imports
import os

import cv2
import numpy as np

os.chdir("D:\Python\learnopencv\@GETTING STARTED WITH OPENCV\BlobDetector")

# Read image
im = cv2.imread("../RESOURCES/bananas.jpg", cv2.IMREAD_GRAYSCALE)

# Scale the image
im = cv2.resize(im, (0, 0), fx=0.25, fy=0.25)

# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()

# Change thresholds
params.minThreshold = 0
params.maxThreshold = 255
params.thresholdStep = 5
print(
    f"Thresholds: {params.minThreshold} - {params.maxThreshold}, Step: {params.thresholdStep}"
)


# Filter by Area.
params.filterByArea = True
params.minArea = 500

# Filter by Circularity
params.filterByCircularity = True
params.minCircularity = 0.1

# Filter by Convexity
params.filterByConvexity = False
params.minConvexity = 0.87

# Filter by Inertia
params.filterByInertia = False
params.minInertiaRatio = 0.01

# Create a detector with the parameters
ver = (cv2.__version__).split(".")
if int(ver[0]) < 3:
    detector = cv2.SimpleBlobDetector(params)
else:
    detector = cv2.SimpleBlobDetector_create(params)


# Detect blobs.
keypoints = detector.detect(im)

# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures
# the size of the circle corresponds to the size of blob

im_with_keypoints = cv2.drawKeypoints(
    im, keypoints, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
)

# Show blobs
cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey(0)
