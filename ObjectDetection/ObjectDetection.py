import torch
import numpy as np
import cv2
import pybboxes as pbx
from torchvision import transforms
from model import Network

# Model
# model = torch.hub.load("ultralytics/yolov5", "yolov5s")  # or yolov5n - yolov5x6, custom
# model = torch.hub.load("ultralytics/yolov5", "custom", path="yolov5/runs/train/exp8/weights/best.pt", force_reload=True)
# model = torch.hub.load("ultralytics/yolov5", "custom", path="best.pt", force_reload=True)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = Network().to(device)
model.load_state_dict(torch.load('SelfMade.pt'))
model.eval()

# cap = cv2.VideoCapture("Traffic\LeCCTV\cctv052x2004080517x01660.avi") # Reading from file
cap = cv2.VideoCapture(0) # Reading from cam

ret, frame = cap.read()
while(1):
    ret, frame = cap.read()
    if ret == False:
        print("No more frames")
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    else:
        with torch.no_grad():
            predict = model(torch.stack([transforms.ToTensor()(frame)] * 8).to(device))
        box_data = predict[0]
        print(box_data)
        x = box_data[0].item()
        y = box_data[1].item()
        w = box_data[2].item()
        h = box_data[3].item()
        H, W = frame.shape[:2]
        box_voc = pbx.convert_bbox((x,y,w,h), from_type="yolo", to_type="voc", image_size=(W,H))
        cv2.rectangle(frame, (box_voc[0], box_voc[1]), (box_voc[2], box_voc[3]), (0, 0, 255), 3)
        image = frame
        # image = np.squeeze(predict.render())
        cv2.imshow("Its the Video", image)
        if cv2.waitKey(30) & 0xFF == ord('q'): 
            cap.release()
            cv2.destroyAllWindows()
            break