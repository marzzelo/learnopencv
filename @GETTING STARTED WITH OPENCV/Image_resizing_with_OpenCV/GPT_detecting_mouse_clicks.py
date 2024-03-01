import cv2
import numpy as np


# Define the callback function
def click_event(event, x, y, flags, param):
    """
    In this example, data is a dictionary passed as the param parameter to the click_event function through cv2.setMouseCallback().
    The click_event function checks for left button clicks. When such an event occurs, it appends the click coordinates to the
    click_positions list within the data dictionary and draws a small circle at the click location as visual feedback.
    Finally, after closing the window, it prints all the stored click positions to the console.
    """
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Left button click at ({x}, {y})")

        # Append the click position to the list in param
        param["click_positions"].append((x, y))

        # For demonstration, let's also mark the click in the image
        cv2.circle(param["image"], (x, y), 5, (255, 0, 0), -1)
        cv2.imshow("image", param["image"])


# Create a black image and a window
image = cv2.imread("image.jpg")
cv2.namedWindow("image")

# Dictionary to pass as param
data = {"image": image, "click_positions": []}

# Set the mouse callback function with the param
cv2.setMouseCallback("image", click_event, data)

cv2.imshow("image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Print the stored click positions
print("Click positions:", data["click_positions"])

# the string should be separated into a list of words
