# import numpy as np
import cv2
# from pathlib import Path
import requests

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

table_occupied = False
chair_occupied = False
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    grayImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(grayImage)
    if faces == ():
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if table_occupied:
            table_occupied = False
            print("table free")
            requests.get('http://responsivespaces.herokuapp.com/tablefree')

        # if chair_occupied:
        #     chair_occupied = False
        #     print("chair free")
        #     requests.get('http://responsivespaces.herokuapp.com/chairfree')

        continue

    # if not table_occupied:
    #     table_occupied = True
    #     print("table in use")
    #     requests.get('http://responsivespaces.herokuapp.com/tableinuse')

    centers = []
    for (x, y, w, h) in faces:
        # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
        center = (x + w)/2, (y + h)/2
        if w > 100 and h > 100:
            centers.append(center)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)

    if centers and not table_occupied:
        table_occupied = True
        print("table in use")
        requests.get('http://responsivespaces.herokuapp.com/tableinuse')

    if not centers and table_occupied:
        table_occupied = False
        print("table free")
        requests.get('http://responsivespaces.herokuapp.com/tablefree')

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
