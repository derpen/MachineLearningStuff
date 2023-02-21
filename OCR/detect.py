import cv2
import numpy as np
import pytesseract

# TODO: Feature Extraction (HOG preferably) + image segmentation
# GET WAY TO AUTOMATICALLY GET CORRECT THRESHOLD

original_image = cv2.imread('idPics/test1.jpg', cv2.IMREAD_COLOR)
# original_image = cv2.imread('idPics/itsme.jpeg', cv2.IMREAD_COLOR) # Reading my KTP :D

# Applying Gaussian Blur
image = cv2.GaussianBlur(original_image, (1,1), 0)

# Grayscale the image
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# # # Normalize
# norm_image = np.zeros((image.shape[0], image.shape[1]))
# image = cv2.normalize(image, norm_image, 0, 255, cv2.NORM_MINMAX)

# # Applying erode and dilate
kernel = np.ones((2,2), np.uint8)
image = cv2.erode(image, kernel, iterations=1)
image = cv2.dilate(image, kernel, iterations=1)

# Applying threshold
image = cv2.threshold(image, 65, 255, cv2.THRESH_BINARY)[1]

# # Finding contours
# contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

# for contour in contours:
#     x, y, w, h = cv2.boundingRect(contour)
#     cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 0), 1)

text = pytesseract.image_to_string(image)
print(text)

cv2.imshow("Its the ID", image)

cv2.waitKey(0)

cv2.destroyAllWindows()