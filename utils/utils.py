import numpy as np
import pygame
import os


def flipy(y):
    return -y + 600

# Pygame и OpenCV


def surfToArray(surf):
    return pygame.surfarray.array3d(surf).swapaxes(0, 1)


def arrayToSurf(image):
    image_t = np.swapaxes(image, 0, 1)
    return pygame.surfarray.make_surface(image_t)


def returnValue(value):
    return value


def getCenter(image, x=None, y=None):
    if isinstance(image, pygame.Surface):
        size = image.get_size()
    # elif isinstance(image, np.ndarray):
    else:
        size = image.shape

    if x == None:
        x = size[0] // 2
    if y == None:
        y = size[1] // 2
    return (x, y)


def darken(screen, alpha=60):
    darken_surface = pygame.Surface(screen.get_size())
    darken_surface.fill((0, 0, 0))

    darken_surface.set_alpha(alpha)
    screen.blit(darken_surface, (0, 0))


def calculateLuminance(color):
    r, g, b = color
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


# Получение файлов

def getAssetsDir():
    currentDir = os.path.dirname(__file__)
    assetsDir = os.path.join(currentDir, '../assets/')
    return assetsDir


def getImgDir():
    assets = getAssetsDir()
    imgPath = os.path.join(assets, 'img/')
    return imgPath


def getImg(path, name):
    fullPath = os.path.join(path, name)
    return pygame.image.load(fullPath)


def getFontsDir():
    assets = getAssetsDir()
    fontPath = os.path.join(assets, 'fonts/')
    return fontPath


def getSound(name):
    assets = getAssetsDir()
    soundDir = os.path.join(assets, f'sounds/{name}')
    return soundDir
