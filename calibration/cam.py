import os

import cv2
import numpy as np

import pygame

from calibration.calibration_window import CalibrationWindow


class CameraCalibration(CalibrationWindow):
    def __init__(self, surf):
        super().__init__(surf)

        self.calibParams = {'mtx': None, 'dist': None,
                            'rvecs': None, 'tvecs': None}
        self._createBoard()

        self.photosPath = './calibration/photos/'
        self.PHOTOS_NUM = 4
        self.count = self.PHOTOS_NUM

    def _createBoard(self):
        self.dictionary = cv2.aruco.getPredefinedDictionary(
            cv2.aruco.DICT_6X6_250)
        self.board = cv2.aruco.CharucoBoard(
            (5, 7), 0.03, 0.015, self.dictionary)

        # Если изображения вдруг нет, создаем
        if not os.path.isfile('ChArUco.png'):
            self._saveBoardImage()

    def _saveBoardImage(self):
        size_ratio = 7 / 5
        img = cv2.aruco.CharucoBoard.generateImage(
            self.board, (640, int(640*size_ratio)), marginSize=20)
        cv2.imwrite('./calibration/ChArUco.png', img)

    def _displayWaiting(self):
        self._displayTemplate(
            'Калибровка камеры', 'Для начала распечатайте листок, нажав P. Для перехода к следующему шагу нажмите Enter')

    def _displayRunning(self):
        self._displayTemplate(
            f'Осталось снимков: {self.count + 1}', 'Сфотографируйте листок под разными углами, нажимая пробел')

    def _displayEnd(self):
        self._displayTemplate(
            'Калибровка завершена!', 'Теперь можно сравнить, как повлияла калибровка на камеру. Для выхода нажмите Enter, для повтора - R')

    def _displayRunningCv(self):
        ret, frame = self.cap.read()
        if ret:
            # frame = cv2.resize(
            #     frame, (frame.shape[1] // 2, frame.shape[0] // 2))
            cv2.imshow('Camera', frame)
            self.frame = frame

    def _displayEndCv(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.resize(
                frame, (frame.shape[1] // 2, frame.shape[0] // 2))
            cv2.imshow('Camera', frame)

            undistorted = cv2.undistort(
                frame, self.calibParams['mtx'], self.calibParams['dist'])
            cv2.imshow('Camera undistorted', undistorted)

    def _printBoard(self):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'ChArUco.png')
        os.startfile(filename, "print")

    def _takePicture(self):
        self._displayTemplate('Сохранение снимка...', 'Пожалуйста, подождите')
        pygame.display.update()
        cv2.imwrite(f'{self.photosPath}p{self.count}.png', self.frame)
        self.count -= 1

    def _calibrate(self):
        all_charuco_corners = []
        all_charuco_ids = []

        image_files = [os.path.join(self.photosPath, f) for f in os.listdir(
            self.photosPath) if f.endswith(".png")]
        image_files.sort()

        params = cv2.aruco.DetectorParameters()
        for image_file in image_files:
            image = cv2.imread(image_file)
            marker_corners, marker_ids, _ = cv2.aruco.detectMarkers(
                image, self.dictionary, parameters=params)
            if isinstance(marker_ids, np.ndarray):
                charuco_retval, charuco_corners, charuco_ids = cv2.aruco.interpolateCornersCharuco(
                    marker_corners, marker_ids, image, self.board)
                if charuco_retval:
                    all_charuco_corners.append(charuco_corners)
                    all_charuco_ids.append(charuco_ids)

        self.calibParams['mtx'], self.calibParams['dist'], self.calibParams['rvecs'], self.calibParams['tvecs'] = cv2.aruco.calibrateCameraCharuco(
            all_charuco_corners, all_charuco_ids, self.board, image.shape[:2], None, None)

    def _calibToConfig(self):
        self.config.setCameraDistortions(self.calibParams)

    def keypressed(self, key, unicode):
        super().keypressed(key, unicode)
        if self.state == self.State.WAITING and key == pygame.K_p:
            self._printBoard()
        if self.state == self.State.RUNNING and key == pygame.K_SPACE:
            self._takePicture()

            if self.count < 0:
                self._calibrate()
                self.state = self.state.next()

        if self.state == None:
            # Если смена состояния произошла по нажатию Enter (=> с состояния END)
            if key == pygame.K_RETURN:
                cv2.destroyWindow('Camera')
                cv2.destroyWindow('Camera undistorted')
                self._calibToConfig()
        elif self.state == self.State.RUNNING or self.state == self.State.END and self.cap == None:
            self.cap = cv2.VideoCapture(1)

    def run(self):
        back = super().run()
        if self.state != self.State.RUNNING:
            self.count = self.PHOTOS_NUM
        return back
