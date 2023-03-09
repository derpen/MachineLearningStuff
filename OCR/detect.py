import cv2
import numpy as np
import pytesseract
from draw import Draw

# image = cv2.imread("idPics/Me.jpeg", cv2.IMREAD_GRAYSCALE) # This my ID :D
template = cv2.imread("idPics/NIK.jpeg", cv2.IMREAD_GRAYSCALE)
template2 = cv2.imread("idPics/BerlakuHingga.jpeg", cv2.IMREAD_GRAYSCALE)

image = cv2.imread("idPics/Randos.jpg", cv2.IMREAD_GRAYSCALE)
# template = cv2.imread("idPics/NIK2.jpg", cv2.IMREAD_GRAYSCALE)
# template2 = cv2.imread("idPics/BerlakuHingga2.jpg", cv2.IMREAD_GRAYSCALE)

imaji = Draw(image, template, template2)
imaji.transpose_image()
imaji.locate_template_box()
print(imaji.get_coor())
imaji.text_coordinates()
imaji.show_image()

# result = pytesseract.image_to_string(imae)

# print(result)