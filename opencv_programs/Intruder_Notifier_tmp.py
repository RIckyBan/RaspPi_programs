from picamera.array import PiRGBArray
from picamera import PiCamera
import sys, os
import subprocess
import time
import cv2

interval = 0
TOKEN = "mGUFLaGcg6V19NMZOqenoXgWEr1tbe0laB9jStFgKT8"

def notify(interval):
	cmd_IFT = "../post.sh "+ "Riki "+"Welcome " +"Home!"
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

cascPath = sys.argv[1]
faceCascade = cv2.CascadeClassifier(cascPath)

# allow the camera to warmup
time.sleep(0.1)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array
    image = cv2.flip(image, 0)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    for	 (x, y, w, h) in faces:
        cv2.rectangle( image, (x, y), (x+w, y+h), (0, 255, 0), 2)

    if len(faces) == 1:
        print("face\tdeteced!")
        print(faces)

        if interval == 100:
           interval = 0
        else:
           interval += 1

        cv2.imwrite("image.jpg",image)
        notify(interval
)

    # show the frame
    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
