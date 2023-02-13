import torch
import numpy as np
import cv2

# Model
model = torch.hub.load("ultralytics/yolov5", "yolov5s")  # or yolov5n - yolov5x6, custom

cap = cv2.VideoCapture("Traffic\LeCCTV\cctv052x2004080517x01660.avi") # Reading from file
# cap = cv2.VideoCapture(0) # Reading from cam

ret, frame = cap.read()
while(1):
    ret, frame = cap.read()
    if ret == False:
        print("No more frames")
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    else:
        predict = model(frame)
        image = np.squeeze(predict.render())
        cv2.imshow("Its the Video", image)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break