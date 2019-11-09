from picamera.array import PiRGBArray
from picamera import PiCamera
import sys, os
import subprocess
import time
import cv2
import dlib

interval = 0
TOKEN = "mGUFLaGcg6V19NMZOqenoXgWEr1tbe0laB9jStFgKT8"
isBANDO = False
who = ["Stranger ", "Riki "]
value1 = ["Be ", "Welcome "]
value2 = ["Alert!", "Home!"]

def notify(interval):
	cmd_IFT = "../post.sh "+ who[isBANDO] + value1[isBANDO] + value2[isBANDO]
	cmd_LINE = "curl -X POST https://notify-api.line.me/api/notify -H 'Authorization: Bearer mGUFLaGcg6V19NMZOqenoXgWEr1tbe0laB9jStFgKT8' -F 'message=Intruder!' -F 'imageFile=@image.jpg'"

	print("interval: {}".format(interval))

	if interval == 1:
		subprocess.call(cmd_IFT, shell=True)
		print("Message sent.")
		subprocess.call(cmd_LINE, shell=True)
		print("Image sent.")

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

# dlibで学習したモデルを読み込む
BANDOdetector = dlib.simple_object_detector("detector.svm")
detector = dlib.get_frontal_face_detector()

# allow the camera to warmup
time.sleep(0.1)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array
    image = cv2.flip(image, 0)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    rectangles = BANDOdetector(gray)

    if len(rectangles) == 1:
        isBANDO = True
        print("Bando deteced.")
    else:
        isBANDO = False

    for rect in rectangles:
        cv2.rectangle(image, (rect.left(), rect.top()), (rect.right(), rect.bottom()), (147, 20, 255), 2)

    rectangles = detector(gray)

    for rect in rectangles:
        cv2.rectangle(image, (rect.left(), rect.top()), (rect.right(), rect.bottom()), (0, 255, 0), 2)

    if len(rectangles) == 1:
        print("face\tdeteced!")
        print(rectangles)

        if interval == 50:
           interval = 0
        else:
           interval += 1

        cv2.imwrite("image.jpg",image)
        notify(interval)

    # show the frame
    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
