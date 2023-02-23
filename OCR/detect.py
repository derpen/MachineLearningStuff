import cv2
import numpy as np
import pytesseract

# original_image = cv2.imread('idPics/test1.jpg', cv2.IMREAD_COLOR)
# original_image = cv2.imread('idPics/itsme.jpeg', cv2.IMREAD_COLOR) # Reading my KTP :D

# Try template matching
target = cv2.imread('idPics/test1.jpg', cv2.IMREAD_GRAYSCALE)
template = cv2.imread('idPics/itsme.jpeg', cv2.IMREAD_GRAYSCALE) # Reading my KTP :D

result = cv2.matchTemplate(target, template, cv2.TM_CCOEFF_NORMED)

min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

h, w = template.shape
top_left = max_loc
bottom_right = (top_left[0] + w, top_left[1] + h)
cv2.rectangle(target, top_left, bottom_right, 255, 2)

# # Applying Gaussian Blur
# image = cv2.GaussianBlur(original_image, (1,1), 0)

# Grayscale the image
# image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

# Normalize
# norm_image = np.zeros((image.shape[0], image.shape[1]))
# image = cv2.normalize(image, norm_image, 0, 255, cv2.NORM_MINMAX)

# # Applying erode and dilate
# kernel = np.ones((3,3), np.uint8)
# image = cv2.erode(image, kernel, iterations=1)
# image = cv2.dilate(image, kernel, iterations=1)

# Applying threshold
# image = cv2.threshold(image, 65, 255, cv2.THRESH_BINARY)[1]

# # Finding contours
# contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
# for contour in contours:
#     x, y, w, h = cv2.boundingRect(contour)
#     cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 0), 1)

# Some other way of doing this contour thing
# rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
 
# Applying dilation on the threshold image
# dilation = cv2.dilate(image, rect_kernel, iterations = 1)
 
# # Finding contours
# contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
#                                                  cv2.CHAIN_APPROX_NONE)

# contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

# curr = 0
# result = []
# for cnt in contours:
#     x, y, w, h = cv2.boundingRect(cnt)
     
    # Drawing a rectangle on copied image
    # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
     
    # Cropping the text block for giving input to OCR
    # cropped = image[y:y + h, x:x + w]

    # text = pytesseract.image_to_string(cropped)
    # if(text != ""):
    #     result.append(text)
    
    # curr += 100
    # if(curr % 1000 == 0):
    #     print("Detecting...")

# print(result)

cv2.imshow("Its le Match", target)

cv2.waitKey(0)

cv2.destroyAllWindows()