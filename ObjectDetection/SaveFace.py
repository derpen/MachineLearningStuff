import cv2
import os
import uuid

# TODO Automate file dir creation

cap = cv2.VideoCapture(0)

label = ["mask", "nomask"]
currentLabel = 0
wait = 0
pictureTaken = 0
limit = 30 # Limit per label/class

lab = label[currentLabel]
print("Taking pic for " + lab)
while(True):

    if pictureTaken == limit:
        pictureTaken = 0
        currentLabel += 1
        try:
            lab = label[currentLabel] # Check if ran out of label
            print("Taking pic for " + lab)
        except:
            print("We are done!")
            break

    ret, frame = cap.read()
    cv2.imshow("YourFace", frame)

    key = cv2.waitKey(50)

    wait = wait + 100

    if wait == 5000:
        filename = lab + "-" + str(uuid.uuid1())
        path = "datasets/Face/" + lab + "/" + filename + ".jpg"
        cv2.imwrite(path, frame)
        print(lab + " picture no:" + str(pictureTaken + 1) + " succesfully saved")
        wait = 0
        pictureTaken += 1
    
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()