import cv2
import numpy as np

import utils.utils as utils


def createTrackbar():
    cv2.namedWindow('Manual Calibration',  cv2.WINDOW_AUTOSIZE)
    # Create trackbars for L, A, and B adjustments
    # cv2.createTrackbar('H', 'Manual Calibration', 180, 180, lambda x: None)
    # cv2.createTrackbar('S', 'Manual Calibration', 208, 255, lambda x: None)
    # cv2.createTrackbar('V', 'Manual Calibration', 182, 255, lambda x: None)
    cv2.createTrackbar('H_low', 'Manual Calibration', 20, 180, lambda x: None)
    cv2.createTrackbar('S_low', 'Manual Calibration', 165, 255, lambda x: None)
    cv2.createTrackbar('V_low', 'Manual Calibration', 194, 255, lambda x: None)
    cv2.createTrackbar('H_high', 'Manual Calibration',
                       40, 180, lambda x: None)
    cv2.createTrackbar('S_high', 'Manual Calibration',
                       255, 255, lambda x: None)
    cv2.createTrackbar('V_high', 'Manual Calibration',
                       255, 255, lambda x: None)


def filterBlack(blur):
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    # h_adjust = cv2.getTrackbarPos('H', 'Manual Calibration')
    # s_adjust = cv2.getTrackbarPos('S', 'Manual Calibration')
    # v_adjust = cv2.getTrackbarPos('V', 'Manual Calibration')
    h_adjust = 180
    s_adjust = 255
    v_adjust = 205
    mask = cv2.inRange(hsv, (30, 0, 0), (h_adjust, s_adjust, v_adjust))
    return mask


def findPlanets(blur):
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    # h_low = cv2.getTrackbarPos('H_low', 'Manual Calibration')
    # s_low = cv2.getTrackbarPos('S_low', 'Manual Calibration')
    # v_low = cv2.getTrackbarPos('V_low', 'Manual Calibration')

    # h_high = cv2.getTrackbarPos('H_high', 'Manual Calibration')
    # s_high = cv2.getTrackbarPos('S_high', 'Manual Calibration')
    # v_high = cv2.getTrackbarPos('V_high', 'Manual Calibration')

    h_low = 20
    s_low = 165
    v_low = 194
    h_high = 40
    s_high = 255
    v_high = 255

    mask = cv2.inRange(hsv, (h_low, s_low, v_low), (h_high, s_high, v_high))
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


def preprocess(frame):
    blur = cv2.medianBlur(frame, 3)
    return blur


def findContours(frame):
    th = cv2.morphologyEx(frame, cv2.MORPH_CLOSE,
                          np.ones((5, 5), np.uint8))

    th = cv2.morphologyEx(th, cv2.MORPH_DILATE,
                          np.ones((3, 3), np.uint8))

    contours, _ = cv2.findContours(
        th, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # for c in contours:
    # c = cv2.approxPolyDP(c, 1, True)

    return contours


def findObjects(frame):
    blacks = filterBlack(frame)
    contours = findContours(blacks)
    planets = findPlanets(frame)
    return contours, planets


def checkPlanets(frame, planets):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (20, 40, 200), (40, 255, 255))

    remove_planets = []
    for p in planets:
        if not mask[utils.flipy(int(p.body.position.y)) - 1, int(p.body.position.x - 1)]:
            remove_planets.append(p)

    return remove_planets


def process(frame):
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    blur = cv2.medianBlur(frame, 3)
    # smooth = cv2.GaussianBlur(frame, (25, 25), 0)
    norm = cv2.normalize(blur, None, 0, 100, cv2.NORM_MINMAX)
    # norm = cv2.divide(frame, 255 - smooth, scale=20)
    # cv2.imshow('Normalized', norm)
    blacks = filterBlack(norm)

    th = cv2.morphologyEx(blacks, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    # cv2.imshow('TH', th)

    contours, _ = cv2.findContours(
        th, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        c = cv2.approxPolyDP(c, 1, True)
        cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
    # cv2.imshow('Warped', frame)

    planets = []
    planets = findPlanets(norm)
    return frame, contours, planets


# def findNewLines(frame, subtractor):
#     mask = subtractor.apply(frame)
#     _, thresh = cv2.threshold(mask, 244, 255, cv2.THRESH_BINARY)

#     # Use morphological operations to remove noise and fill gaps
#     kernel = np.ones((5, 5), np.uint8)
#     dilated = cv2.dilate(thresh, kernel, iterations=2)
#     eroded = cv2.erode(dilated, kernel, iterations=1)

#     # Find contours in the processed mask
#     contours, _ = cv2.findContours(
#         eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     cv2.drawContours(frame, contours, -1, (255, 0, 0))
#     # cv2.imshow('New objects')


def findNewLines(frame, allContours, oldContours):
    if len(frame.shape) == 3 and frame.shape[2] == 3:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    allContoursImg = np.zeros_like(frame)
    cv2.drawContours(allContoursImg, allContours, -1, (255, 255, 255), -1)
    # allContoursImg = cv2.morphologyEx(allContoursImg, cv2.MORPH_ERODE,
    #   np.ones((7, 7), np.uint8))

    oldContoursImg = np.zeros_like(frame)
    cv2.drawContours(oldContoursImg, oldContours, -1, (255, 255, 255), -1)
    oldContoursImg = cv2.morphologyEx(oldContoursImg, cv2.MORPH_DILATE,
                                      np.ones((7, 7), np.uint8))

    cv2.imshow('all contours', allContoursImg)
    cv2.imshow('old contours', oldContoursImg)

    newContoursImg = allContoursImg.copy()

    temp = cv2.bitwise_and(allContoursImg, oldContoursImg)
    newContoursImg = cv2.bitwise_xor(allContoursImg, temp)

    newContoursImg = cv2.morphologyEx(newContoursImg, cv2.MORPH_DILATE,
                                      np.ones((3, 3), np.uint8))

    _, th = cv2.threshold(newContoursImg, 128, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(
        th, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    cv2.imshow('new contours', newContoursImg)
    return contours
