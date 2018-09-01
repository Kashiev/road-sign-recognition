import sys
import cv2
from utils import Webcam

cam = Webcam(sys.argv[1])

# VGA is the best suited resolution for our task, try to set it
if (640, 480) in cam.get_possible_resolutions():
    cam.set_resolution(640, 480)

while True:
    cv2.waitKey(1)
    try:
        frame = cam.next_frame()
    except:
        cam.close()
        exit(1)
    cv2.imshow('original', frame)
