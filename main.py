import sys
import cv2
from utils import Webcam

cam = Webcam(sys.argv[1])
while True:
    cv2.waitKey(1)
    frame = cam.next_frame()
    cv2.imshow('original', frame)
