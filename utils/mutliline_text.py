import numpy as np

from utils.text_animation import TextAnimation
import utils.utils as utils


class MultilineText:
    def __init__(self, text, font, color, width, animationType=None):
        self.font = font
        self.color = color

        lines = self._textToLines(text, width)
        self._renderMultiline(lines)
        self.size = (width, self.getHeight())
        if animationType == None:
            self.animation = None
        else:
            self.animation = TextAnimation(
                0.3, TextAnimation.AnimtaionType.OPENING, (width, 0), (width, self.getHeight()))

    def _renderMultiline(self, lines):
        self.rendered = []
        for line in lines:
            self.rendered.append(self.font.render(line, True, self.color))

    def _textToLines(self, text, maxWidth):
        textRendered = self.font.render(text, True, (0, 0, 0))
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
        lines.append(' ')
        return lines

    def draw(self, surf, x, y, alignCenter=False):
        if self.animation != None:
            if self.animation.state == TextAnimation.AnimationState.NONE:
                return
            self.size = self.animation.getNextPos()

            size = self.size.copy()
            lineHeight = self.rendered[0].get_height()
            for idx, line in enumerate(self.rendered):
                width, height = size[0], size[1]
                if size[1] >= lineHeight:
                    height = lineHeight
                size[1] -= height
                offsetY = lineHeight
                y += offsetY

                surf.blit(line, (x, y), (0, 0, width, height))
            return
        for line in (self.rendered):
            if alignCenter:
                line_rect = line.get_rect(
                    center=utils.getCenter(surf, y=y))
            else:
                line_rect = line.get_rect()
                line_rect.x = x,
                line_rect.y = y
            y += line_rect.height

            surf.blit(line, line_rect)

    def getHeight(self):
        lineHeight = self.rendered[0].get_height()
        return lineHeight * len(self.rendered)

    def getDrawnHeight(self):
        return self.size[1]
