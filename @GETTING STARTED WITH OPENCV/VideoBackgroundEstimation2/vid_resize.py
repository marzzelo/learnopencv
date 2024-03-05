import cv2
import os

class VideoResizer:
    def __init__(self, orig_file):
        self.orig_file = orig_file
        self.frame_size = None
        self.fps = None
        self.nframes = None
        self.vid_capture = None
        self.output = None

    def open_video(self):
        # Create a video capture object
        self.vid_capture = cv2.VideoCapture(self.orig_file)

        # Print error message if object is not in open state
        if not self.vid_capture.isOpened():
            print("Error opening video file")
            return False

        # Get height and width of the frame
        self.frame_width = int(self.vid_capture.get(3))
        self.frame_height = int(self.vid_capture.get(4))
        
        self.fps = self.vid_capture.get(cv2.CAP_PROP_FPS)
        self.nframes = self.vid_capture.get(cv2.CAP_PROP_FRAME_COUNT)
        print(f"frame count: {self.nframes}, fps: {self.fps}, new frame size: {self.frame_size}")

        return True

    def create_output(self, resize_factor=0.5):
        self.resize_factor = resize_factor
        new_frame_size = (int(self.frame_width * resize_factor), int(self.frame_height * resize_factor))  # used by VideoWriter() method
        out_file = self.orig_file.split('.')[0] + '_r.mp4'
        self.output = cv2.VideoWriter(out_file, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), self.fps, new_frame_size)

    def process_video(self):
        nf = 0
        print('Processing video...')
        print('Press "q" to stop processing the video and close the window.')
        
        while self.vid_capture.isOpened():
            ret, frame = self.vid_capture.read()
            print(f"frame {nf}")
            nf += 1
            if ret:
                frame = cv2.resize(frame, (0, 0), fx=self.resize_factor, fy=self.resize_factor)
                self.output.write(frame)
                if nf % 100 == 0:
                    cv2.imshow("Frame", frame)
                key = cv2.waitKey(1)
                if key == ord('q') or key == 27:
                    break
            else:
                print('Stream disconnected')
                break

    def release_resources(self):
        self.vid_capture.release()
        self.output.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
        
    resizer = VideoResizer("chorro_r.mp4")
    
    if resizer.open_video():
        resizer.create_output(resize_factor=0.5)
        resizer.process_video()
        resizer.release_resources()
    else:
        print("Error opening video file")

