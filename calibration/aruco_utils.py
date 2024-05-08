import cv2
import numpy as np


class ArucoUtils:
    def __init__(self, size: int, markersDictionary: dict = cv2.aruco.DICT_4X4_50):
        self.size = size
        self.availableMarkers = markersDictionary
        self.markers = []
        self.ids = [4, 7, 13, 24]
        self.detectedMarkers = {"Ids": np.array([]), "Corners": np.array([])}
        self.offset = 3

        # self.detectedCorners = np.array([])
        # self.detectedIds = np.array([])

    def _generateMarker(self, idx: int):
        marker = np.zeros((self.size, self.size, 1), dtype="uint8")
        markersDict = cv2.aruco.getPredefinedDictionary(self.availableMarkers)
        markersDict.generateImageMarker(idx, self.size, marker)
        return marker

    def generateMarkers(self):
        for i in self.ids:
            self.markers.append(self._generateMarker(i))

    def placeMarkers(self, image):
        size = self.size + self.offset
        image[self.offset:size, self.offset:size] = self.markers[0]
        image[-size:-self.offset, -size:-
              self.offset] = self.markers[2]
        image[self.offset:size, -size:-
              self.offset] = self.markers[1]
        image[-size:-self.offset, self.offset:size] = self.markers[3]

    def detectCorners(self, image):
        # self.detectMarkers(image)
        if type(self.detectedMarkers["Ids"]) == np.ndarray and len(self.detectedMarkers["Ids"]) == len(self.ids):
            allCorners = self.detectedMarkers["Corners"]
            return np.array([allCorners[0][0][0], allCorners[3][0][3], allCorners[2][0][2], allCorners[1][0][1]])
        return None

    def detectMarkers(self, image):
        greyImg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        detectorParams = cv2.aruco.DetectorParameters()
        markersDict = cv2.aruco.getPredefinedDictionary(self.availableMarkers)
        detector = cv2.aruco.ArucoDetector(markersDict, detectorParams)

        self.detectedMarkers["Corners"], self.detectedMarkers["Ids"], _ = detector.detectMarkers(
            greyImg)

        # Если маркеры были найдены
        if type(self.detectedMarkers["Ids"]) == np.ndarray:

            # Преобразование в ndarray для более удобной работы
            self.detectedMarkers["Corners"] = np.array(
                self.detectedMarkers["Corners"])

            # Сортировка обоих списков по возрастанию id; для соотнесения
            self._sortMarkers()
        else:
            self.detectedMarkers["Ids"] = np.array([])

    def outlineMarkers(self, image, pg=False):
        if not pg:
            cv2.aruco.drawDetectedMarkers(
                image, self.detectedMarkers["Corners"], self.detectedMarkers["Ids"])
            return

        thickness = 2
        for idx, id in enumerate(self.ids):
            if id not in self.detectedMarkers["Ids"]:
                color = (255, 0, 0)
            else:
                color = (0, 255, 0)

            if idx == 0:
                pt1 = (self.offset - thickness // 2,
                       self.offset - thickness // 2)
                pt2 = (self.offset + self.size + thickness // 2,
                       self.offset + self.size + thickness // 2)
            elif idx == 1:
                pt1 = (image.shape[1] - self.size - self.offset -
                       thickness // 2, self.offset - thickness // 2)
                pt2 = (image.shape[1] - self.offset + thickness // 2,
                       self.size + self.offset + thickness // 2)
            elif idx == 2:
                pt1 = (image.shape[1] - self.size - self.offset - thickness // 2,
                       image.shape[0] - self.size - self.offset - thickness // 2)
                pt2 = (image.shape[1] - self.offset + thickness // 2,
                       image.shape[0] - self.offset + thickness // 2)
            else:
                pt1 = (self.offset - thickness // 2,
                       image.shape[0] - self.size - self.offset - thickness // 2)
                pt2 = (self.offset + self.size + thickness // 2,
                       image.shape[0] - self.offset + thickness // 2)

            cv2.rectangle(image, pt1, pt2, color, thickness)

    def _sortMarkers(self):
        sortedIds = self.detectedMarkers["Ids"].argsort(0)[
            :, 0]
        self.detectedMarkers["Ids"] = self.detectedMarkers["Ids"][sortedIds]
        self.detectedMarkers["Corners"] = self.detectedMarkers["Corners"][sortedIds]

    def countMarkers(self):
        return len(self.detectedMarkers['Ids'])

    def getWarpMatrix(self, frame, markersImage):
        corners = self.detectCorners(frame)
        if type(corners) == np.ndarray:
            # x, y format
            out = np.float32([[0, 0],
                              [0, markersImage.shape[0] - 1],
                              [markersImage.shape[1] - 1,
                               markersImage.shape[0] - 1],
                              [markersImage.shape[1] - 1, 0]])
            warpMatrix = cv2.getPerspectiveTransform(corners, out)
            return warpMatrix
