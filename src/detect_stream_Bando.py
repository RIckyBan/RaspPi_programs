from picamera.array import PiRGBArray
from picamera import PiCamera
import sys, os
import subprocess
import time
import cv2
import dlib

interval = 0

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

# allow the camera to warmup
time.sleep(0.1)

# dlibで学習したモデルを読み込む
detector = dlib.simple_object_detector("detector.svm")

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array
    image = cv2.flip(image, 0)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rectangles = detector(gray)

    if len(rectangles) == 1:
        print("Bando deteced.")

    for rect in rectangles:
        cv2.rectangle(image, (rect.left(), rect.top()), (rect.right(), rect.bottom()), (147, 20, 255), 2)

    interval += 1
    print("interval:", interval)

    # show the frame
    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
