import numpy as np
import cv2
import sys, os

img = sys.argv[1]

img = cv2.imread(img)
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
