import cv2
from utils.config_utils import ConfigUtils
import utils.cv_utils as cv_utils


cap = cv_utils.openCam()

while True:
    ret, frame = cap.read()
    print(ret)
    if ret:
        cv2.imshow('No fix', frame)
        undistorted = cv_utils.fixCamera(frame)
        cv2.imshow('Fixed', undistorted)
    cv2.waitKey(0)
