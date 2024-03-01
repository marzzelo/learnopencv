import cv2

# Create a video capture object, in this case we are reading the video from a file
vid_capture = cv2.VideoCapture("Resources/rain.mp4")

if not vid_capture.isOpened():
    print("Error opening the video file")

# Read fps and frame count
else:
    # Get frame rate information
    # You can replace 5 with CAP_PROP_FPS as well, they are enumerations
    fps = vid_capture.get(cv2.CAP_PROP_FPS)
    print("Frames per second : ", fps, "FPS")

    # Get frame count
    # You can replace 7 with CAP_PROP_FRAME_COUNT as well, they are enumerations
    frame_count = vid_capture.get(7)
    print("Frame count : ", frame_count)
    
    print("Video duration : ", frame_count/fps, "seconds")


#########################################
# Read the video frame by frame
#########################################
while vid_capture.isOpened():

    # vid_capture.read() methods returns a tuple, first element is a bool
    # and the second is frame
    ret, frame = vid_capture.read()

    if ret:
        # Display the frame scaled to 50% of the original size
        frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

        cv2.imshow("Frame", frame)

        # 20 is in milliseconds, try to increase the value, say 50 and observe
        key = cv2.waitKey(1)

        if key == ord("q") or key == 27:
            break
    else:
        break

# Release the video capture object
vid_capture.release()
cv2.destroyAllWindows()
