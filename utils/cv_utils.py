import cv2
import numpy as np

from utils.config_utils import ConfigUtils


def openCam():
    # url = "http://192.168.1.39:8080/video"
    # url = "/dev/video2"
    url = ConfigUtils().getCameraUrl()
    _cap = cv2.VideoCapture(url)
    if (_cap.isOpened() == False):
        print("Error opening video stream or file")
    return _cap


def fixColor(frame):
    diff = ConfigUtils().getColors()

    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    lab = cv2.add(lab, diff)
    bgr = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    return bgr


def fixFrame(frame):
    size = ConfigUtils().getScreenParams()[:2]

    mtx, dist, rvecs, tvecs = ConfigUtils().getCameraDistortions()
    warpMatrix = ConfigUtils().getWarpMatrix()

    undistorted = cv2.undistort(frame, mtx, dist)
    transformed = cv2.warpPerspective(
        undistorted, warpMatrix, size)
    colored = fixColor(transformed)
    return colored


def normalize(frame):
    # rgb_planes = cv2.split(frame)

    # result_planes = []
    # result_norm_planes = []

    # #  Нормализуем по каждому из каналов
    # for plane in rgb_planes:
    #     dilated_img = cv2.dilate(plane, np.ones((7, 7), np.uint8))
    #     bg_img = cv2.medianBlur(dilated_img, 21)
    #     diff_img = 255 - cv2.absdiff(plane, bg_img)
    #     norm_img = cv2.normalize(
    #         diff_img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
    #     result_planes.append(diff_img)
    #     result_norm_planes.append(norm_img)

    # result_norm = cv2.merge(result_norm_planes)

    # Split the image into R, G, B channels
    b, g, r = cv2.split(frame)

    # Apply histogram equalization to each channel
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(16, 16))
    b = clahe.apply(b)
    g = clahe.apply(g)
    r = clahe.apply(r)

    normalized_frame = cv2.merge((b, g, r))

    return normalized_frame
