import json
import numpy as np
import os


class ConfigUtils:
    # Класс является синглтоном, поскольку изменения конфига могут происходить из разных точек программы
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        self.configRead()
        self._getFontsDir()

    def _getFontsDir(self):
        currentDir = os.path.dirname(__file__)
        self.fontPath = os.path.join(currentDir, '../assets/fonts/')

    def configRead(self):
        with open("config.json", "r") as file:
            self.config = json.load(file)

    def getScreenParams(self):
        screenWidth = self.config['General']['screenWidth']
        screenHeight = self.config['General']['screenHeight']
        fps = self.config['General']['fps']
        pos = self.config['General']['pos']
        return screenWidth, screenHeight, fps, pos

    def getWarpMatrix(self):
        warpMatrix = np.array(self.config['Surface'])
        return warpMatrix

    def getCameraDistortions(self):
        mtx = np.array(self.config['Camera']['mtx'])
        dist = np.array(self.config['Camera']['dist'])
        rvecs = np.array(self.config['Camera']['rvecs'])
        tvecs = np.array(self.config['Camera']['rvecs'])
        return mtx, dist, rvecs, tvecs

    def getColors(self):
        colors = np.array(self.config['Colors'])
        return colors

    def getFonts(self):
        titleName = self.config['General']['fonts']['title']
        generalName = self.config['General']['fonts']['general']

        title = os.path.join(self.fontPath, titleName)
        general = os.path.join(self.fontPath, generalName)

        return title, general

    def configWrite(self):
        with open('config.json', 'w') as f:
            json.dump(self.config, f, indent=4)

    def setScreenParams(self, width, height, pos=None):
        if width != None and height != None:
            self.config['General']['screenWidth'] = width
            self.config['General']['screenHeight'] = height
        if pos != None:
            self.config['General']['pos'] = pos
        self.configWrite()

    def setWarpMatrix(self, value):
        self.config['Surface'] = value.tolist()
        self.configWrite()

    def setCameraDistortions(self, paramsDict):
        self.config['Camera']['mtx'] = paramsDict['mtx'].tolist()
        self.config['Camera']['dist'] = paramsDict['dist'].tolist()
        self.config['Camera']['rvecs'] = paramsDict['rvecs'].tolist()
        self.config['Camera']['tvecs'] = paramsDict['tvecs'].tolist()
        self.configWrite()

    def setColors(self, value):
        self.config['Colors'] = value.tolist()
        self.configWrite()
