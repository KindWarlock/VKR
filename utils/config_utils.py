import json
import numpy as np
import os
import utils.utils as utils


class ConfigUtils:
    # Класс является синглтоном, поскольку изменения конфига могут происходить из разных точек программы
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        self.configRead()
        self.fontPath = utils.getFontsDir()

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

    def getFont(self, type='general', size='m'):
        if type == 'general':
            font = self.config['General']['fonts']['general']
        else:
            font = self.config['General']['fonts']['title']
        fontLink = os.path.join(self.fontPath, font['family'])

        fontSize = font['size'][size]
        return fontLink, fontSize

    def getCameraUrl(self):
        url = self.config['Camera']['url']
        # if url.isdigit():
        # url = int(url)
        return url

    def getPlayer(self, game=0):
        if game == 0:
            player = self.config['Shooter']['Player']
        else:
            player = self.config['Lines']['Player']
        return player

    def setPlayer(self, player, game=0):
        if game == 0:
            self.config['Shooter']['Player'] = player
        else:
            self.config['Lines']['Player'] = player
        self.configWrite()

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

    def getColorScheme(self, game):
        return self.config[game]['Colors']
