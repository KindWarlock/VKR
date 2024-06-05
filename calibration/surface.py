import numpy as np
import cv2

from calibration.aruco_utils import ArucoUtils
from calibration.calibration_window import CalibrationWindow
import utils.utils as utils


class SurfaceCalibration(CalibrationWindow):
    def __init__(self, surface):
        super().__init__(surface)
        self.aruco = ArucoUtils(100)
        self.aruco.generateMarkers()
        self.warpMatrix = None

    def _displayMarkers(self, outline=False):
        image = utils.surfToArray(self.surf)
        self.aruco.placeMarkers(image)
        if outline:
            image = np.ascontiguousarray(image, dtype=np.uint8)
            self.aruco.outlineMarkers(image, True)
        self.surf.blit(utils.arrayToSurf(image), (0, 0))

    def _displayWaiting(self):
        super()._displayTemplate('Калибровка поверхности',
                                 'Измените размер окна, чтобы углы маркеров соответствовали углам поверхности и нажмите Enter')
        self._displayMarkers()

    def _displayRunning(self):
        super()._displayTemplate('Поиск маркеров...', 'ы')
        self._displayMarkers(True)

    def _displayEnd(self):
        super()._displayTemplate('Калибровка завершена',
                                 'Если результат вас не устраивает, повторите калибровку, нажав R. Для выхода нажмите Enter')

        self._displayMarkers(True)

    def _displayRunningCv(self):
        ret, frame = self.cap.read()
        if not ret:
            return
        mtx, dist, rvecs, tvecs = self.config.getCameraDistortions()

        frame = cv2.undistort(frame, mtx, dist)
        # frame = cv2.resize(
        #     frame, (frame.shape[1] // 2, frame.shape[0] // 2))
        self.aruco.detectMarkers(frame)
        self.aruco.outlineMarkers(frame)
        cv2.imshow('Markers', frame)

        if self.aruco.countMarkers() == 4:
            self.warpMatrix = self.aruco.getWarpMatrix(
                frame, utils.surfToArray(self.surf))
            self.state = self.state.next()

    def _displayEndCv(self):
        ret, frame = self.cap.read()
        if ret:
            # frame = cv2.resize(
            #     frame, (frame.shape[1] // 2, frame.shape[0] // 2))
            mtx, dist, rvecs, tvecs = self.config.getCameraDistortions()

            frame = cv2.undistort(frame, mtx, dist)
            frame = cv2.warpPerspective(
                frame, self.warpMatrix, self.surf.get_size())
            cv2.imshow('Markers', frame)

    def _calibToConfig(self):
        self.config.setWarpMatrix(self.warpMatrix)

    def keypressed(self, key, unicode):
        super().keypressed(key, unicode)
        if self.state == self.State.RUNNING:
            # self.cap = cv2.VideoCapture('http://192.168.43.1:8080/video')
            self.cap = cv2.VideoCapture(1)

        if self.state == None:
            if isinstance(self.warpMatrix, np.ndarray):
                self._calibToConfig()
                cv2.destroyWindow('Markers')
