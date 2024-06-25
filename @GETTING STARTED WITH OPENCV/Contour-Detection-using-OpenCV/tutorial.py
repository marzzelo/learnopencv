import cv2
import numpy as np

from stackImg import stackImages
from getContours import getContours


# def getContours(img, process=False, area_threshold=0, color=(255, 0, 0), thickness=6, fontScale=0.7, fontThickness=2):
#     if process is True:
#         imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)
#         imgCanny = cv2.Canny(imgBlur, 50, 50)
#         img = imgCanny
        
#     imgContour = img.copy()

#     contours, hierarchy = cv2.findContours(
#         img,
#         cv2.RETR_EXTERNAL,  # to get the outer contours
#         cv2.CHAIN_APPROX_NONE,  # to get all the points of the contours (no approximation)
#     )
#     print(f'Contours: {len(contours)}')
    
#     for cnt in contours:
#         area = cv2.contourArea(cnt)
#         print(f"\n---------------\nArea: {area}")
#         if area > area_threshold:  # to avoid noise (small areas)
#             cv2.drawContours(
#                 image=imgContour, 
#                 contours=cnt, 
#                 contourIdx=-1,  # -1 to draw all the contours
#                 color=color, 
#                 thickness=thickness
#             )
#             peri = cv2.arcLength(cnt, True)
#             # print(peri)

#             approx = cv2.approxPolyDP(
#                 cnt, 0.02 * peri, True
#             )  # this method approximates a polygonal curve with the specified precision
            
#             print(f"Number of corners: {len(approx)}")
#             objCor = len(approx)

#             x, y, w, h = cv2.boundingRect(
#                 approx
#             )  # this function returns the x, y, width, and height of the bounding rectangle for the contour

#             if objCor == 3:
#                 objectType = "Tri"
#             elif objCor == 4:
#                 aspRatio = w / float(h)
#                 if aspRatio > 0.98 and aspRatio < 1.03:
#                     objectType = "Square"
#                 else:
#                     objectType = "Rectangle"
#             elif objCor == 5:
#                 objectType = "Pentagon"
#             elif objCor == 6:
#                 objectType = "Hexagon"
#             elif objCor > 6:
#                 objectType = "Circle"
#             else:
#                 objectType = "None"

#             cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 2)
#             cv2.putText(
#                 imgContour,
#                 objectType,
#                 (x + 10, y + (h // 2) - 10),
#                 cv2.FONT_HERSHEY_COMPLEX,
#                 fontScale=fontScale,
#                 color=(0, 0, 0),
#                 thickness=fontThickness,
#             )
            
#     return [img, imgGray, imgBlur, imgCanny, imgContour]


path = "input/shapes.png"
img = cv2.imread(path)


img_out, imgGray, imgBlur, imgCanny, imgContour = getContours(img, process=True, area_threshold=500, color=(0, 0, 0), thickness=3, fontScale=0.7, fontThickness=1)

# imgBlank = np.zeros_like(img)
imgStack = stackImages(0.8, ([img, imgGray, imgBlur], [imgCanny, imgContour, img_out]))

cv2.imshow("Stack", imgStack)

cv2.waitKey(0)
