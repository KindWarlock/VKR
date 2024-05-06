import cv2
import numpy as np
import calibration.aruco_utils as aruco_utils
from math import sqrt
from enum import Enum
import pygame as pg
from utils.utils import flipy

from skimage.exposure import match_histograms


def open_cam(url=1):
    # url = "http://192.168.43.1:8080/video"
    _cap = cv2.VideoCapture(url, cv2.CAP_DSHOW)
    if (_cap.isOpened() == False):
        print("Error opening video stream or file")
    _cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3)  # auto mode
    _cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)  # manual mode

    return _cap


def colorCorrection(frame):
    ref = cv2.imread('./calibration/colors.png')

    return match_histograms(frame, ref, channel_axis=-1)


def get_calibration_aruco():
    _arucoUtils = aruco_utils.ArucoUtils(100)
    _arucoUtils.generate_markers()
    _image = np.empty(
        (config.SCREEN_HEIGHT, config.SCREEN_WIDTH, 3), dtype='uint8')
    _image.fill(255)
    _arucoUtils.place_markers(_image)
    cv2.imshow('Display', _image)
    cv2.imshow('Warped', _image)

    # Надо сдвигать за границы экрана, но на винде это глючит
    cv2.moveWindow('Display', 3000, 150)
    return _arucoUtils, _image


def filter_black(blur):
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    # mask = cv2.inRange(hsv, (80, 30, 0), (100, 75, 235))
    mask = cv2.inRange(hsv, (80, 40, 0), (140, 255, 255))

    cv2.imshow('Blacks', mask)
    return mask


def find_planets(blur):
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (20, 40, 200), (40, 255, 255))
    circles = cv2.HoughCircles(
        mask, cv2.HOUGH_GRADIENT, 1, 50, param1=10, param2=10, minRadius=10)
    cv2.imshow('Planets', mask)

    if circles is not None:
        # circles = np.uint16(np.around(circles))[0]
        circles = np.around(circles)[0]
        # cv2.circle(blur, (circles[0, 0], circles[0, 1]),
        #    circles[0, 2], (0, 255, 0), 2)
        # cv2.imshow('Circles', blur)
    return circles
    # return planets


def check_planets(frame, planets):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (20, 40, 200), (40, 255, 255))

    remove_planets = []
    for p in planets:
        if not mask[flipy(int(p.body.position.y) - 1), int(p.body.position.x - 1)]:
            remove_planets.append(p)

    return remove_planets


def process(frame, warp_matrix):
    frame = cv2.warpPerspective(
        frame, warp_matrix, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))

    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    blur = cv2.medianBlur(frame, 3)
    # smooth = cv2.GaussianBlur(frame, (25, 25), 0)
    norm = cv2.normalize(blur, None, 0, 100, cv2.NORM_MINMAX)
    # norm = cv2.divide(frame, 255 - smooth, scale=20)
    cv2.imshow('Normalized', norm)
    blacks = filter_black(norm)

    th = cv2.morphologyEx(blacks, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    # cv2.imshow('TH', th)

    contours, _ = cv2.findContours(
        th, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        c = cv2.approxPolyDP(c, 1, True)
        cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
    cv2.imshow('Warped', frame)

    planets = []
    planets = find_planets(norm)
    return frame, contours, planets


def get_warp_matrix(aruco_utils, frame, markers_image):
    corners = aruco_utils.detect_corners(frame)
    aruco_utils.outline_markers(frame)
    warpMatrix = None

    if type(corners) == np.ndarray:
        # x, y format
        out = np.float32([[0, 0],
                          [0, markers_image.shape[0] - 1],
                          [markers_image.shape[1] - 1,
                           markers_image.shape[0] - 1],
                          [markers_image.shape[1] - 1, 0]])
        # print(corners, out)
        warpMatrix = cv2.getPerspectiveTransform(corners, out)
    return warpMatrix


def pg_to_cv2(pg_screen):
    result = pg.surfarray.array3d(
        pg_screen).swapaxes(0, 1)
    result = cv2.cvtColor(result, cv2.COLOR_RGB2BGR)
    return result
