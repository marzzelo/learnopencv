import os

import cv2
import numpy as np

# change directory to the folder where the image is stored
os.chdir(
    "D:\Python\learnopencv\@GETTING STARTED WITH OPENCV\VideoBackgroundEstimation2"
)


# Open Video
cap = cv2.VideoCapture("cam1_r.avi", cv2.CAP_FFMPEG)
print(f"cap: {cap}")

# Randomly select 25 frames
nframes = cap.get(cv2.CAP_PROP_FRAME_COUNT)
print(f"frame count: {nframes}")

selector = np.random.uniform(size=200)
print(f"selector: {selector}")

frameIds = (nframes * selector).astype(int)


print(f"selected frames: {frameIds}")
cv2.waitKey(0)

# Store selected frames in an array
frames = []

# for i in frameIds:
#     cap.set(cv2.CAP_PROP_POS_FRAMES, i)
#     ret, frame = cap.read()
#     if ret:
#         frames.append(frame)

for fid in frameIds:
    cap.set(cv2.CAP_PROP_POS_FRAMES, fid)
    ret, frame = cap.read()
    frames.append(frame)

# Calculate the median along the time axis
medianFrame = np.median(frames, axis=0).astype(dtype=np.uint8)

# Display median frame
cv2.imshow("frame", medianFrame)
cv2.waitKey(0)

# Reset frame number to 0
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

# Convert background to grayscale
grayMedianFrame = cv2.cvtColor(medianFrame, cv2.COLOR_BGR2GRAY)

# Loop over all frames
ret = True
while ret:
    # Read frame
    ret, frame = cap.read()
    # Convert current frame to grayscale
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Calculate absolute difference of current frame and
    # the median frame
    dframe = cv2.absdiff(frame, grayMedianFrame)
    # Treshold to binarize
    th, dframe = cv2.threshold(dframe, 30, 255, cv2.THRESH_BINARY)
    # Display image
    cv2.imshow("frame", dframe)
    key = cv2.waitKey(20)
    if key == 27:
        break

# Release video object
cap.release()

# Destroy all windows
cv2.destroyAllWindows()
