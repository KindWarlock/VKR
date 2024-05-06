import numpy as np
import pygame
import json


def flipy(y):
    """Small hack to convert chipmunk physics to pg coordinates"""
    return -y + 600


def resizeWindow(size):
    with open('config.json', 'r+') as f:
        data = json.load(f)
        data['General']['screenWidth'] = size[0]
        data['General']['screenHeight'] = size[1]
        f.seek(0)        # <--- should reset file position to the beginning.
        json.dump(data, f, indent=4)
        f.truncate()


def surfToArray(surf):
    return pygame.surfarray.array3d(surf).swapaxes(0, 1)


def arrayToSurf(image):
    image_t = np.swapaxes(image, 0, 1)
    return pygame.surfarray.make_surface(image_t)


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


def renderMultiline(lines, font, color):
    out = []
    for line in lines:
        out.append(font.render(line, True, color))
    return out


def textToLines(text, font, maxWidth):
    textRendered = font.render(text, True, (0, 0, 0))
    width = textRendered.get_width()
    linesNum = np.ceil(width / maxWidth).astype(np.uint8)
    charsNum = np.ceil(len(text) / linesNum).astype(np.uint8)
    lines = []
    lastEnd = 0
    while lastEnd < len(text):
        start = lastEnd
        end = lastEnd + charsNum
        if end >= len(text):
            end = len(text)
        elif text[end] != ' ':
            while text[end] != ' ':
                end += 1
                if end == len(text):
                    break
        lines.append(text[start:end].strip())
        lastEnd = end
    return lines


def configRead(func):
    def wrapper():
        config = None
        with open("config.json", "r") as file:
            config = json.load(file)
        return func(config)
    return wrapper


@configRead
def getScreenParams(config):
    screenWidth = config['General']['screenWidth']
    screenHeight = config['General']['screenHeight']
    fps = config['General']['fps']
    return screenWidth, screenHeight, fps


@configRead
def getWarpMatrix(config):
    warpMatrix = np.array(config['Surface'])
    return warpMatrix


@configRead
def getCameraDistortions(config):
    mtx = np.array(config['Camera']['mtx'])
    dist = np.array(config['Camera']['dist'])
    rvecs = np.array(config['Camera']['mtx'])
    tvecs = np.array(config['Camera']['mtx'])
    return mtx, dist, rvecs, tvecs
