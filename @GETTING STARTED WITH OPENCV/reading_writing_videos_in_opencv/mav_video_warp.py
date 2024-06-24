# Import packages
import os

import cv2
import numpy as np

savevideo = True

file_directory = os.path.dirname(__file__)

os.chdir(file_directory)

vid_path = os.path.join(file_directory, "resources", "lluvia1.mp4")
# "Resources/lluvia1.mp4"
print(f"vid_path: {vid_path}")

# Create a video capture object
vid_capture = cv2.VideoCapture(vid_path)

# Print error message if object is not in open state
if vid_capture.isOpened() is False:
    print("Error opening video file")

# Get height and width of the frame
# CAP_PROP_FRAME_WIDTH = 3, CAP_PROP_FRAME_HEIGHT = 4
frame_width = int(vid_capture.get(3))
frame_height = int(vid_capture.get(4))
n_frames = int(vid_capture.get(7))
frame_size = (frame_width // 4, frame_height // 4)  # used by VideoWriter() method
fps = 20

# Create a video writer object
output = cv2.VideoWriter(
    "Resources/warpzx.avi", cv2.VideoWriter_fourcc("M", "J", "P", "G"), 40, frame_size
)

# Rotation parameters
width, height = frame_size
center = (width / 2, height / 2)

ret, frame = vid_capture.read()
w = frame.shape[1]
h = frame.shape[0]
cx = w // 2
cy = h // 2

angle = 0
scale = 1

# Reset the video capture object to the start of the video
vid_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)

while vid_capture.isOpened():
    # vCapture.read() methods returns a tuple, first element is a bool
    # and the second is frame
    ret, frame = vid_capture.read()

    if ret is True:
        # Make annotations on the frame BEFORE transformations
        cv2.line(
            frame,
            (cx, cy // 2),
            (cx, cy),
            (0, 0, 255),
            thickness=10,
            lineType=cv2.LINE_AA,
        )
        cv2.line(
            frame,
            (cx, cy),
            (cx + cy // 2, cy),
            (0, 0, 255),
            thickness=10,
            lineType=cv2.LINE_AA,
        )
        cv2.circle(
            frame, (cx, cy), h // 20, (0, 255, 255), thickness=10, lineType=cv2.LINE_AA
        )

        frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rotate_matrix = cv2.getRotationMatrix2D(center=center, angle=angle, scale=scale)
        frame = cv2.warpAffine(src=frame, M=rotate_matrix, dsize=(width, height))

        # Make annotations on the frame AFTER transformations
        cv2.rectangle(frame, (30, height - 75), (400, height - 40), (0, 0, 0), -1)
        text = f"Angle: {angle:.2f} Scale: {scale:.2f}"
        cv2.putText(
            frame,
            text,
            (50, height - 50),
            fontFace=cv2.FONT_HERSHEY_COMPLEX,
            fontScale=0.75,
            color=(250, 0, 250),
            thickness=1,
            lineType=cv2.LINE_AA,
        )

        # Update transformations parameters
        angle += 0.5
        if angle > 360:
            angle = 0
        scale = 0.5 * np.sin(angle * np.pi / 180) + 1

        cv2.imshow("Frame", frame)

        if savevideo:
            output.write(frame)

        # k == 113 is ASCII code for q key. You can try to replace that
        # with any key with its corresponding ASCII code, try 27 which is for ESCAPE
        key = cv2.waitKey(1)
        if key == ord("q") or key == 27:
            break
        if key == ord("p"):
            cv2.waitKey(-1)  # wait until any key is pressed.

    else:
        # print("Stream disconnected")
        vid_capture = cv2.VideoCapture(vid_path)
        # break

# Release the video capture and output objects.
vid_capture.release()
output.release()
cv2.destroyAllWindows()
