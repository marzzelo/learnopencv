import os
import threading
import time
import winsound

import cv2
import numpy as np


class VideoBackgroundEstimation:
    """
    Class for estimating and removing the background from a video.

    Args:
        video_path (str): Path to the video file.

    Attributes:
        video_path (str): Path to the video file.
        cap (cv2.VideoCapture): Video capture object.
        median_frame (numpy.ndarray): Median frame of the video.
        mask (numpy.ndarray): Mask for background removal.

    Methods:
        play_beep: Plays a beep sound.
        compute_median_frame: Computes the median frame of the video.
        create_mask: Creates a mask for background removal.
        run_video: Runs the video and performs background removal.
        process_video: Processes the video by estimating and removing the background.
    """

    def __init__(self, video_path):
        self.video_path = video_path
        self.cap = None
        self.median_frame = None
        self.mask = None

    def play_beep(self):
        """
        Plays a beep sound.
        """
        winsound.Beep(1000, 200)

    def compute_median_frame(self, frame_id, n_frames=10):
        """
        Computes the median frame of the video.

        Args:
            start_frame (int): Starting frame index (default: 0).
            n_frames (int): Number of frames to consider for computing the median frame (default: 150).

        Returns:
            numpy.ndarray: The computed median frame.
        """
        frames = []
        # frame_id = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))

        print(
            f"Computing median frame... (start_frame: {frame_id}, n_frames: {n_frames})"
        )
        print("*" * n_frames)

        for i in range(n_frames):

            ret, frame = self.cap.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                gray_median_frame = cv2.imread("median_frame.png", cv2.IMREAD_GRAYSCALE)
                return gray_median_frame

            frames.append(frame)
            # # skip 10 frames
            # self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id + 10)
            print("*", end="")

        median_frame = np.median(frames, axis=0).astype(dtype=np.uint8)
        self.median_frame = cv2.cvtColor(median_frame, cv2.COLOR_BGR2GRAY)

        print("\nMedian frame computed successfully.")

    def create_mask(self, base_mask=None):
        """
        Creates a mask for background removal.

        Args:
            base_mask (numpy.ndarray): Base mask to start with (default: None).

        Returns:
            numpy.ndarray: The created mask.
        """
        radius = 40
        # med_frame = cv2.imread("median_frame.png")
        med_frame = self.median_frame.copy()
        h, w = med_frame.shape[:2]
        print(f"Creating mask... (h: {h}, w: {w})")

        if base_mask is not None:
            mask = base_mask
        else:
            mask = np.ones(med_frame.shape[:2], dtype=np.uint8) * 255
            # mask the lower left corner
            cv2.rectangle(mask, (31, 1233), (820, 1394), (0, 0, 0), -1)
            cv2.rectangle(
                med_frame,
                (31, 1233),
                (820, 1394),
                (0, 0, 0),
                3,
            )

        def paint_mask(action, x, y, flags, *userdata):
            global pen

            if action == cv2.EVENT_LBUTTONDOWN:
                pen = True
                print(f"Pen down at ({x}, {y})")
            elif action == cv2.EVENT_LBUTTONUP:
                pen = False
            elif action == cv2.EVENT_MOUSEMOVE:
                if pen:
                    cv2.circle(mask, (x, y), radius, (0, 0, 0), -1)
                    cv2.circle(med_frame, (x, y), radius, (0, 0, 0), -1)

        cv2.namedWindow("image", cv2.WINDOW_NORMAL)
        cv2.setMouseCallback("image", paint_mask)

        while True:
            cv2.imshow("image", med_frame)
            key = cv2.waitKey(5)
            if key & 0xFF == 27:
                break

            if key == ord("+"):
                radius += 5  # Increase the radius of the brush

            if key == ord("-"):
                radius -= 5
                if radius < 5:  # Decrease the radius of the brush
                    radius = 5  # Minimum radius is 5

        self.mask_contours, _ = cv2.findContours(
            mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )

        cv2.imwrite("mask.png", mask)
        cv2.destroyAllWindows()

        return mask

    def run_video(self, threshold=500, start_frame=0):
        """
        Runs the video and performs background removal.

        Args:
            threshold (int): Threshold for detecting foreground objects (default: 500).
            start_frame (int): Starting frame index (default: 0).
        """
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        cv2.namedWindow("frame", cv2.WINDOW_NORMAL)

        # add a trackbar to the window
        cv2.createTrackbar("TrackBar", "frame", 0, self.length, lambda x: None)

        _last_time = time.time()
        n_warn = 0

        h, w = self.median_frame.shape[:2]

        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break

            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            d_frame = cv2.absdiff(gray_frame, self.median_frame)
            th, td_frame = cv2.threshold(d_frame, 40, 255, cv2.THRESH_BINARY)
            td_frame = cv2.bitwise_and(td_frame, self.mask)
            count = cv2.countNonZero(td_frame)
            frame_id = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
            # update Trackbar position
            cv2.setTrackbarPos("TrackBar", "frame", frame_id)

            cv2.putText(
                frame,
                f"Frame: {frame_id}, count: {count}",
                (w // 2 - 100, h - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
                cv2.LINE_AA,
            )

            cv2.drawContours(frame, self.mask_contours, -1, (0, 0, 255), 2)

            if count > threshold and count < 100000:
                contours, _ = cv2.findContours(
                    td_frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
                )
                cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)

                current_time = time.time()
                if current_time - _last_time >= 1:
                    _last_time = current_time
                    cv2.imwrite(f"warning_{n_warn}.png", frame)
                    n_warn += 1
                    threading.Thread(target=self.play_beep).start()

            cv2.imshow("frame", frame)

            if frame_id % 500 == 0:
                self.compute_median_frame(frame_id)
                # self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id)

            key = cv2.waitKey(1)
            if key == ord("q") or key == 27:
                break

            if key == ord("p"):
                cv2.waitKey(0)

            if key == ord("f"):
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id + 10000)
                self.compute_median_frame(frame_id + 10000)

            if key == ord("b"):
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id - 1000)
                self.compute_median_frame(frame_id - 1000)

            if key == ord("r"):
                self.compute_median_frame(frame_id)
                # self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id)

    def process_video(self):
        """
        Processes the video by estimating and removing the background.
        """
        self.cap = cv2.VideoCapture(self.video_path)
        # save the length of the video
        self.length = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

        self.compute_median_frame(0)
        self.mask = self.create_mask()

        self.run_video(threshold=500, start_frame=0)

        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    pen = False

    # Change dir to current file location
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    video_path = "flex2.mp4"
    video_processor = VideoBackgroundEstimation(video_path)
    video_processor.process_video()
