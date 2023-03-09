import cv2
import numpy as np
from calc_coor import get_second_point, get_relative_dist_ang

class Draw:
    def __init__(self, image, template, template2):
        # Resize the images , template matching requires same size
        self.image = cv2.resize(image, (970, 632), interpolation=cv2.INTER_AREA) # Original image size of my ID
        self.template = cv2.resize(template, (73, 36), interpolation=cv2.INTER_AREA) # Original size of NIK template from my ID
        self.template2 = cv2.resize(template2, (178, 26), interpolation=cv2.INTER_AREA) # Original size of Berlaku Hingga template from my ID
        self.IDReference = cv2.imread("idPics/Me.jpeg", cv2.IMREAD_GRAYSCALE) # My ID :) (this might cause trouble)
        self.is_template_drawn = False
        self.drawn_box = []

    def template_match(self, custom_Image=None):
        # Match the first template
        if custom_Image is None:
            image = self.image
        else:
            image = custom_Image
        result = cv2.matchTemplate(image, self.template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        tl = max_loc

        # Match for 2nd template
        result = cv2.matchTemplate(image, self.template2, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        tl2 = max_loc
        return tl, tl2 
    
    def get_bottom_right(self, top_left, template):
        h, w = template.shape[:2]
        return (top_left[0] + w, top_left[1] + h)
    
    def locate_template_box(self):
        top_left, top_left2 = self.template_match()
        bottom_right = self.get_bottom_right(top_left, self.template)
        bottom_right2 = self.get_bottom_right(top_left2, self.template2)
        self.drawn_box = [top_left, top_left2, bottom_right, bottom_right2]
        self.is_template_drawn = True

    def draw_box(self):
        cv2.rectangle(self.image, self.drawn_box[0], self.drawn_box[1], (0, 0, 255), 2)
        cv2.rectangle(self.image, self.drawn_box[2], self.draw_box[3], (0, 0, 255), 2)

    def show_image(self):
        cv2.imshow("ID", self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def get_coor(self):
        if not self.is_template_drawn:
            print("No template drawn yet, please call locate_template_box() first!")
        else:   
            return self.drawn_box

    def text_coordinates(self):
        coor = self.get_coor()
        if coor != None:
            x = coor[0]
            res = get_relative_dist_ang()
            for section in res:
                boxi = []
                for coord in section:
                    leX, leY = get_second_point(x, coord[0], coord[1])
                    boxi.append((leX, leY))
                
                # Temporary draw just to see where things are
                # TODO save the coordinates to be used later
                cv2.rectangle(self.image, boxi[0], boxi[1], (0, 0, 255), 2) 
    
    def transpose_image(self):
        """
        Align image with reference ID. This ensures that the text coordinates would be at the correct position (hopefully)
        """
        max_loc1, max_loc2 = self.template_match(self.image)
        max_loc3, max_loc4 = self.template_match(self.IDReference)

        diff_x1 = max_loc3[0] - max_loc1[0]
        diff_y1 = max_loc3[1] - max_loc1[1]

        h, w = self.image.shape[:2]

        first = cv2.warpAffine(self.image, np.float32([[1, 0, diff_x1], [0, 1, diff_y1]]), (w, h))

        max_loc5, max_loc6 = self.template_match(first)
        diff_x2 = max_loc6[0] - max_loc4[0]
        diff_y2 = max_loc6[1] - max_loc4[1]
        final = cv2.warpAffine(first, np.float32([[1, 0, diff_x2], [0, 1, diff_y2]]), (w, h))

        # self.image = first
        self.image = final