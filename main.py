import cv2
import numpy as np
import dlib
from statistics import mean
from pynput.mouse import Button, Controller
import operator
import pickle
from getDOMDensityMap import getGravityVec
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
mouse = Controller()


with open('DOMMatrix', 'rb') as f:
    # dump information to that file
    DOMMatrix = pickle.load(f)

DOMMatrix = [[float(cord) for cord in DOMMatrixEle]
             for DOMMatrixEle in DOMMatrix]

counter = 0
while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # make it gray
    faces = detector(gray)  # detect face
    for face in faces:
        landmarks = predictor(gray, face)
    pos = 29 # Nose location
    x = int(landmarks.part(pos).x)  # x coordinate position
    y = int(landmarks.part(pos).y)  # y xoordinateß position
    cv2.circle(frame, (x, y), 10, (0, 0, 255))
    if counter == 0:
        initial_pos = (x, y)
        print("initial pos")
    else:
        new_pos = tuple(np.subtract((x, y), initial_pos))
        print("new pos", new_pos)
        #initial_pos = (x, y)
        #print("new initial position", initial_pos)

        if counter % 1000 == 0:
            with open('DOMMatrix', 'rb') as f:
                # dump information to that file
                DOMMatrix = pickle.load(f)

            DOMMatrix = [[float(cord) for cord in DOMMatrixEle]
                         for DOMMatrixEle in DOMMatrix]
        dom_loc = getGravityVec(
            mouse.position[0], mouse.position[1], DOMMatrix)

        mouse.move(new_pos[0]/3 + dom_loc[0], new_pos[1]/3 + dom_loc[1])
        # mouse.move(new_pos[0] / 3, new_pos[1] / 3)
    print('Now we have moved it to {0}'.format(mouse.position))
    print('The current pointer position is {0}'.format(mouse.position))
    print('Nose is on:', x, y)
    print('mouse position', mouse.position)
    counter += 1
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()
