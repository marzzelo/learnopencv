import cv2
import numpy as np

# LOAD AN IMAGE USING 'IMREAD'
img = cv2.imread("celda.png")

# DISPLAY
cv2.imshow("Celda de Carga", img)

# GRAYSCALE
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# cv2.imshow("Celda de Carga Gris", imgGray)

# BLUR
imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 0)
# cv2.imshow("Celda de Carga Gris Borrosa", imgBlur)

# CANNY EDGE DETECTION
imgCanny = cv2.Canny(img, 100, 100)
cv2.imshow("Celda de Carga Canny", imgCanny)

# DILATION
kernel = np.ones((2,2), np.uint8)
imgDilation = cv2.dilate(imgCanny, kernel, iterations=1)
cv2.imshow("Celda de Carga Dilatada", imgDilation)

# EROSION
imgEroded = cv2.erode(imgDilation, kernel, iterations=1)
cv2.imshow("Celda de Carga Erosionada", imgEroded)



cv2.waitKey(0)
