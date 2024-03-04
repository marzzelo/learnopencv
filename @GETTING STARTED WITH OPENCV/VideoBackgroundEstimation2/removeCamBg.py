import os
import threading
import time
import winsound

import cv2
import numpy as np

# change directory to the folder where the image is stored
os.chdir(
    "D:\Python\learnopencv\@GETTING STARTED WITH OPENCV\VideoBackgroundEstimation2"
)


# Function to play beep sound asynchronously
def play_beep():
    winsound.Beep(1000, 200)


# Open Camera
# cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# Open Video
cap = cv2.VideoCapture("cam1_r.avi", cv2.CAP_FFMPEG)
print(f"cap: {cap}")

def compute_medianframe():
    
    frames = []
    nframes = 50

    # append n frames to the frames array
    print("Capturing frames...")
    print("." * nframes)

    for i in range(nframes):
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        frames.append(frame)
        print(".", end="", flush=True)

    # Calculate the median along the time axis
    medianFrame = np.median(frames, axis=0).astype(dtype=np.uint8)

    # save the median frame
    cv2.imwrite("median_frame.png", medianFrame)

    return medianFrame


def run_video(medianFrame, threshold=500):
    # Reset frame number to 0
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    # Convert background to grayscale
    grayMedianFrame = cv2.cvtColor(medianFrame, cv2.COLOR_BGR2GRAY)

    # Loop over all frames
    ret = True

    _last_time = time.time()
    nwarn = 0

    while ret:
        # Read frame
        ret, frame = cap.read()

        # Convert current frame to grayscale
        bwframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Calculate absolute difference of current frame and
        # the median frame
        dframe = cv2.absdiff(bwframe, grayMedianFrame)

        # Treshold to binarize
        th, dframe = cv2.threshold(dframe, 50, 255, cv2.THRESH_BINARY)

        # count the pixels that are not black
        count = cv2.countNonZero(dframe)

        # if more than 10 pixels are not black.
        if count > threshold:
            # detect and draw contour around the non-black pixels
            contours, _ = cv2.findContours(dframe, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)      

            current_time = time.time()
            if current_time - _last_time >= 10:
                print(f"delta time: {current_time - _last_time}")
                _last_time = current_time
                
                # write the frame to disk
                cv2.imwrite(f"warning_{nwarn}.png", frame)
                nwarn += 1

                threading.Thread(target=play_beep).start()
                

        # multiply dframe with frame using and operator
        # fframe = cv2.bitwise_or(frame, frame, mask=dframe)

        # Display image
        cv2.imshow("frame", frame)

        key = cv2.waitKey(10)
        if key == ord("q") or key == 27:
            break


if __name__ == "__main__":
    
    if os.path.exists("median_frame.png"):
        medianframe = cv2.imread("median_frame.png")
    else:
        medianframe = compute_medianframe()

    run_video(medianframe, threshold=2000)

    # if exists, remove the median frame
    # if os.path.exists("median_frame.png"):
    #     os.remove("median_frame.png")

    # Release video object
    cap.release()

    # Destroy all windows
    cv2.destroyAllWindows()
