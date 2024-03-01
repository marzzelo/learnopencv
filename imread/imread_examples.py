import cv2

import os
# change directory to the location of the image, imread/
os.chdir(r"imread")


# Read 8-bit grayscale image
im = cv2.imread(r"earth-16-bit-per-channel.png", cv2.IMREAD_GRAYSCALE)
if im is None:
    print("Could not read the image.")
    exit()

print("flags :  cv2.IMREAD_GRAYSCALE")

# print("Size %s, type %s\n" % (im.shape, im.dtype))º
print(f'Size {im.shape}, type {im.dtype}\n')

# Read 8-bit color image
im = cv2.imread("earth-16-bit-per-channel.png", cv2.IMREAD_COLOR)
print("flags : cv2.IMREAD_COLOR")
print("Size %s, type %s\n" % (im.shape, im.dtype))

# Read 16-bit color image
im = cv2.imread(
    "earth-16-bit-per-channel.png", cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH
)
print("flags :  cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH")
print("Size %s, type %s\n" % (im.shape, im.dtype))

# Read transparent PNG / TIFF image
im = cv2.imread("earth-16-bit-per-channel.png", cv2.IMREAD_UNCHANGED)
print("flags : cv2.IMREAD_UNCHANGED")
print("Size %s, type %s\n" % (im.shape, im.dtype))
