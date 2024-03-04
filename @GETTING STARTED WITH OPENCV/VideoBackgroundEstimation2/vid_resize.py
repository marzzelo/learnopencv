# Import packages
import cv2
import os

# change directory to the folder where the image is stored
os.chdir("D:\Python\learnopencv\@GETTING STARTED WITH OPENCV\VideoBackgroundEstimation2")

orig_file = "cam1.mp4"
# Create a video capture object
vid_capture = cv2.VideoCapture(orig_file)

# Print error message if object is not in open state
if(vid_capture.isOpened() is False):
	print("Error opening video file")

# Get height and width of the frame
#CAP_PROP_FRAME_WIDTH = 3, CAP_PROP_FRAME_HEIGHT = 4
frame_width = int(vid_capture.get(3))
frame_height = int(vid_capture.get(4))
frame_size = (frame_width//2,frame_height//2) # used by VideoWriter() method
fps = vid_capture.get(cv2.CAP_PROP_FPS)
nframes = vid_capture.get(cv2.CAP_PROP_FRAME_COUNT)
print(f"frame count: {nframes}, fps: {fps}, new frame size: {frame_size}")

# Create a video writer object
out_file = orig_file.split('.')[0] + '_r.avi'
output = cv2.VideoWriter(out_file, cv2.VideoWriter_fourcc('M','J','P','G'), fps, frame_size)

nf = 0
print('Processing video...')
print('Press "q" to stop processing the video and close the window.')

while(vid_capture.isOpened()):
    # vCapture.read() methods returns a tuple, first element is a bool 
    # and the second is frame
    ret, frame = vid_capture.read()
    print(f"frame {nf}")
    nf += 1
    if ret is True:
        frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        output.write(frame) # Write the frame to the output file
        cv2.imshow("Frame",frame)
        # k == 113 is ASCII code for q key. You can try to replace that 
        # with any key with its corresponding ASCII code, try 27 which is for ESCAPE
        key = cv2.waitKey(1)
        if key == ord('q') or key == 27:
            break
    else:
        print('Stream disconnected')
        break
    
# Release the video capture and output objects.
vid_capture.release()
output.release()
cv2.destroyAllWindows()
