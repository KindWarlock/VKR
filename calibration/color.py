import numpy as np
import cv2
import pygame

from calibration.calibration_window import CalibrationWindow
import utils.utils as utils
import utils.cv_utils as cv_utils


class ColorCalibration(CalibrationWindow):
    def __init__(self, surface):
        super().__init__(surface)
        self.calibParams = None
        self.ref = cv2.imread('./calibration/colors.png')
        self.cardSize = (4, 6)  # rows, cols
        self._cropCard()
        self.manualCalib = False

    def _cropCard(self):
        # Изначальное изображение слишком большое
        self.ref = cv2.resize(self.ref, (0, 0), fx=0.3, fy=0.3)

        # Из-за сжатия изображения и перехода цвета, для кооректного определения
        # черного будем бинаризовать
        gray = cv2.cvtColor(self.ref, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)

        # Ищем черные границы
        indices = np.nonzero(thresh)
        y1, y2 = np.min(indices[0]), np.max(indices[0])
        x1, x2 = np.min(indices[1]), np.max(indices[1])

        # Теперь находим размер квадрата. Для этого по одной из оси находим суммарную длину цветных квадратов
        thresh = thresh[y1:y2+1, x1:x2+1]

        patchesOnly = np.count_nonzero(thresh[0, :])

        # Делим ее на количество квадратов, получая размер одного
        self.patchSize = patchesOnly / self.cardSize[1]

        # И находим размер промежутков
        self.gap = (thresh.shape[1] - patchesOnly) / (self.cardSize[1] - 1)
        self.ref = self.ref[y1:y2+1, x1:x2 + int(self.gap)]

        # cv2.imshow('Cropped', self.ref)

    def _displayWaiting(self):
        super()._displayTemplate('Калибровка цвета',
                                 'Перед калибровкой цвета убедитесь, что была пройдена калибровка камеры и поверхности и нажмите Enter')

    def _displayRunning(self):
        self._displayColors()

    def _displayEnd(self):
        if not self.manualCalib:
            super()._displayTemplate('Калибровка завершена',
                                     'Если результат вас не устраивает, повторите калибровку, нажав R. Для ручной калибровки нажмите M (после калибровки - Enter). Для выхода нажмите Enter')
            return
        self._displayColors()

    def _displayRunningCv(self):
        ...

    def _displayEndCv(self):
        if self.manualCalib:
            self.getAdjustments()
        ret, frame = self.cap.read()
        if ret:
            frame = self._preprocess(frame)
            # cv2.imshow('Source image', frame)
            cv2.imshow('Source image', utils.surfToArray(self.surf))
            corrected = self._colorCorrection(frame)
            cv2.imshow('Color corrected', corrected)

    def _displayColors(self):
        width, height = self.config.getScreenParams()[:2]
        resized = cv2.resize(self.ref, dsize=(width, height))
        rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        self.surf.blit(utils.arrayToSurf(rgb), (0, 0))

    def _getPatchColors(self, image):
        # Для более простой цветокоррекции
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

        imgSize = image.shape[:2]
        # Create arrays of x and y coordinates
        y = np.linspace(0,
                        imgSize[0], self.cardSize[0], dtype='int', endpoint=False)
        x = np.linspace(0,
                        imgSize[1], self.cardSize[1], dtype='int', endpoint=False)

        # Create a grid of (x, y) coordinates
        X, Y = np.meshgrid(y, x)

        # Stack x and y coordinates into a single array
        offset = int(self.patchSize / 2)
        patchCoordinates = np.stack((X, Y), axis=-1) + offset
        # Extract color values from patches
        patchColors = []
        for coord in patchCoordinates.reshape(24, 2):
            # Для координат OpenCV
            coord = (coord[0], coord[1])
            color = lab[coord]
            patchColors.append(color)
        patchColors = np.array(patchColors)

        return patchColors

    def _preprocess(self, frame):
        mtx, dist, rvecs, tvecs = self.config.getCameraDistortions()
        warpMatrix = self.config.getWarpMatrix()

        undistorted = cv2.undistort(frame, mtx, dist)
        transformed = cv2.warpPerspective(
            undistorted, warpMatrix, self.surf.get_size())
        return transformed

    def _calibrate(self):
        ret, frame = self.cap.read()
        if ret:
            frame = self._preprocess(frame)

            self.ref = cv2.resize(
                self.ref, (frame.shape[1], frame.shape[0]))
            refColors = self._getPatchColors(self.ref)
            frameColors = self._getPatchColors(frame)
            difference = refColors.astype('int') - frameColors.astype('int')

            meanValues = np.mean(difference, axis=0)
            # stdValues = np.std(difference, axis=0)
            meanValues[0] += 30
            meanValues[1] -= 15
            meanValues[2] -= 10
            self.calibParams = meanValues
            # for i in range(3):  # Iterate over the L, a, and b channels
            #     frameLab[:, :, i] = ((frameLab[:, :, i] - np.mean(frameLab[:, :, i])) * (
            #         stdValues[i] / np.std(frameLab[:, :, i]))) + meanValues[i]

    def _colorCorrection(self, frame):
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        lab = cv2.add(lab, self.calibParams)
        bgr = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        return bgr

    def _calibToConfig(self):
        self.config.setColors(self.calibParams)

    def keypressed(self, key, unicode):
        super().keypressed(key, unicode)
        if self.state == self.State.RUNNING:
            self._displayColors()
            pygame.display.update()
            self.cap = cv_utils.openCam()
            self._calibrate()
            self.state = self.state.next()
        elif self.state == self.State.END:
            if key == pygame.K_m:
                self.createTrackbar()
                self.manualCalib = True
        elif self.state == None:
            if key == pygame.K_RETURN:
                cv2.destroyWindow('Color corrected')
                cv2.destroyWindow('Source image')
                cv2.destroyWindow('Manual Calibration')
                self._calibToConfig()

    def run(self):
        return super().run()

    def createTrackbar(self):
        # Create a window
        cv2.namedWindow('Manual Calibration',  cv2.WINDOW_AUTOSIZE)
        # Create trackbars for L, A, and B adjustments
        cv2.createTrackbar('L', 'Manual Calibration', int(
            self.calibParams[0]), 512, lambda x: None)
        cv2.createTrackbar('A', 'Manual Calibration', int(
            self.calibParams[1]), 512, lambda x: None)
        cv2.createTrackbar('B', 'Manual Calibration', int(
            self.calibParams[2]), 512, lambda x: None)

        cv2.setTrackbarMin('L', 'Manual Calibration', -255)
        cv2.setTrackbarMin('A', 'Manual Calibration', -255)
        cv2.setTrackbarMin('B', 'Manual Calibration', -255)

    def getAdjustments(self):
        l_adjust = cv2.getTrackbarPos('L', 'Manual Calibration')
        a_adjust = cv2.getTrackbarPos('A', 'Manual Calibration')
        b_adjust = cv2.getTrackbarPos('B', 'Manual Calibration')
        self.calibParams = np.array([l_adjust, a_adjust, b_adjust])
