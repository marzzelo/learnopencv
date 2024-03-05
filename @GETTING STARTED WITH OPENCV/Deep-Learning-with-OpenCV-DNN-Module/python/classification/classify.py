"""
This script performs image classification using a pre-trained neural network model.
It loads an image from disk, preprocesses it, passes it through the model, and displays the predicted class label and probability on top of the image.

The script uses the OpenCV library and requires the following files:
- classification_classes_ILSVRC2012.txt: A text file containing the ImageNet class names.
- DenseNet_121.caffemodel: The pre-trained DenseNet-121 model weights.
- DenseNet_121.prototxt: The model configuration file.

The script performs the following steps:
1. Reads the ImageNet class names from the classification_classes_ILSVRC2012.txt file.
2. Loads the DenseNet-121 model using cv2.dnn.readNet() function.
3. Loads the image from disk using cv2.imread() function.
4. Creates a blob from the image using cv2.dnn.blobFromImage() function.
5. Sets the input blob for the neural network using model.setInput() function.
6. Performs a forward pass of the image blob through the model using model.forward() function.
7. Processes the output to get the predicted class label and probability.
8. Displays the predicted class label and probability on top of the image using cv2.putText() function.
9. Shows the image with the predicted class label and probability using cv2.imshow() function.
10. Saves the image with the predicted class label and probability to the outputs/result_image.jpg file using cv2.imwrite() function.
"""

import cv2
import numpy as np

# read the ImageNet class names
with open("../../input/classification_classes_ILSVRC2012.txt", "r") as f:
    image_net_names = f.read().split("\n")
    
# final class names (just the first word of the many ImageNet names for one image)
class_names = [name.split(",")[0] for name in image_net_names]

# load the neural network model
model = cv2.dnn.readNet(
    model="../../input/DenseNet_121.caffemodel",
    config="../../input/DenseNet_121.prototxt",
    framework="Caffe",
)

# Also can use the following code to load the model
# model = cv2.dnn.readNetFromCaffe(
#     prototxt="../../input/DenseNet_121.prototxt",
#     caffeModel="../../input/DenseNet_121.caffemodel",
# )

# load the image from disk
image = cv2.imread("../../input/image_1.jpg")

# Show the image
cv2.imshow("Image", image)
cv2.waitKey(0)

# create blob from image
# This function performs mean subtraction and scaling. 
# It also optionally resizes and crops the image from the center, subtracting the mean values, 
# scaling the values by scalefactor, and then resizing the image to size size × size.
blob = cv2.dnn.blobFromImage(
    image=image, scalefactor=0.01, size=(224, 224), mean=(104, 117, 123)
)

# set the input blob for the neural network
model.setInput(blob)

# forward pass image blog through the model
outputs = model.forward()

final_outputs = outputs[0]

# make all the outputs 1D
final_outputs = final_outputs.reshape(1000, 1)

# get the class label
label_id = np.argmax(final_outputs)
# convert the output scores to softmax probabilities
probs = np.exp(final_outputs) / np.sum(np.exp(final_outputs))
# get the final highest probability
final_prob = np.max(probs) * 100.0
# map the max confidence to the class label names
out_name = class_names[label_id]
out_text = f"{out_name}, {final_prob:.3f}"

# put the class name text on top of the image
cv2.putText(image, out_text, (25, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.imwrite("../../outputs/result_image.jpg", image)
