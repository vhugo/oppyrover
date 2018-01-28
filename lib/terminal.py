import pygame
import re

from lib.imageloader import imageLoader
from lib.gameobjects import Sprite


class Terminal(Sprite):
    keyRepeatTimeout = 0

    def __init__(self, columns, lines, rover):
        self.frameSize = (10, 14)
        self.availableKeys = "1234567890qwertyuiopasdfghjkl'zxcvbnm\"?!_.> "

        self.rover = rover

        self.columns = columns
        self.lines = lines
        self.width = self.frameSize[0] * self.columns
        self.height = (self.frameSize[1] * (self.lines + 1)) + 10
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()

        self.newLine = []
        self.linesInput = []
        self.linesResponse = []
        self.linesHistory = []
        self.linesHistoryIdx = 0
        self.cursor = -2
        self.cursorBlink = True
        self.cursorBlinkCycles = 0
        self.keyPressed = ()
        super().__init__("images/text.png")

    def loadSprite(self):
        posy = 0
        posx = 0
        for idx, key in enumerate(self.availableKeys):
            posx = idx % 10
            if posx == 0 and idx > 0:
                posy += 1

            px = (self.frameSize[0] * posx)
            py = (self.frameSize[1] * posy)

            image = imageLoader(
                self.asset,
                1,
                (px, py, self.frameSize[0], self.frameSize[1])
            )
            # image.set_colorkey(image.get_at((0, 0)))
            self.sprite.append(image)

    def update(self):
        self.playerInput()
        self.updateDisplay()

    def allowNewLineEntry(self):
        return (len(self.newLine) <= (self.columns - 4))

    def playerInput(self):
        for event in pygame.event.get(pygame.KEYUP):
            if event.key == pygame.K_BACKSPACE:
                if len(self.newLine) > 0:
                    del self.newLine[-1]

            elif event.key == pygame.K_RETURN:
                self.pushNewLine()

            elif event.key == pygame.K_QUOTE:
                if self.allowNewLineEntry():
                    self.newLine.append(self.availableKeys.find("'"))

            elif event.key == pygame.K_QUOTEDBL:
                if self.allowNewLineEntry():
                    self.newLine.append(self.availableKeys.find("\""))

            elif event.key == pygame.K_EXCLAIM:
                if self.allowNewLineEntry():
                    self.newLine.append(self.availableKeys.find("!"))

            elif event.key == pygame.K_EXCLAIM:
                if self.allowNewLineEntry():
                    self.newLine.append(self.availableKeys.find("!"))

            elif event.key == pygame.K_QUESTION:
                if self.allowNewLineEntry():
                    self.newLine.append(self.availableKeys.find("?"))

            elif event.key == pygame.K_UP:
                historyCount = len(self.linesHistory)
                if historyCount < 1:
                    return

                if self.linesHistoryIdx >= historyCount:
                    self.linesHistoryIdx = historyCount - 1

                history = [h for h in reversed(self.linesHistory)]
                self.newLine = history[self.linesHistoryIdx]
                self.linesHistoryIdx += 1

            elif event.key == pygame.K_DOWN:
                self.linesHistoryIdx -= 1
                if self.linesHistoryIdx < 0:
                    self.linesHistoryIdx = 0
                    self.newLine = []
                    return

                history = [h for h in reversed(self.linesHistory)]
                self.newLine = history[self.linesHistoryIdx]

            elif event.key == pygame.K_CLEAR:
                self.runCommand("clear")

            else:
                if self.allowNewLineEntry():
                    self.newLine.append(
                        self.availableKeys.find(chr(event.key)))

    def pushNewLine(self):
        self.linesHistory.append(self.newLine)
        self.linesInput.append(
            [self.translate(">")[0]] + self.newLine)
        playerInput = "".join(self.translate(self.newLine)).lower()

        computerResponse = self.runCommand(playerInput)
        if computerResponse is not None:
            self.linesResponse.append([self.translate(computerResponse)])

        if (len(self.linesInput) * 2) > self.lines:
            del self.linesInput[0]
            del self.linesResponse[0]

        self.newLine = []

    def runCommand(self, cmd):
        cmdMove = re.compile(r"move (\d+)(\w{,2})")
        cmdClear = re.compile(r"^clear$")
        # cmdHelp = re.compile(r"^help$")

        match = cmdClear.match(cmd)
        if match:
            self.linesInput = []
            self.linesResponse = []
            return None

        match = cmdMove.match(cmd)
        if match:
            distance = int(match.group(1))
            direction = match.group(2)
            directionName = None

            if direction == "n":
                directionName = "north"

            elif direction == "ne":
                directionName = "northeast"

            elif direction == "e":
                directionName = "east"

            elif direction == "se":
                directionName = "southeast"

            elif direction == "s":
                directionName = "south"

            elif direction == "sw":
                directionName = "southwest"

            elif direction == "w":
                directionName = "west"

            elif direction == "w":
                directionName = "northwest"

            if directionName is not None:
                return "moving %d meters %s..." % (
                    distance, directionName)
            else:
                return "can't move towards '%s'" % direction

        return "command not found.try 'help'"

    def translate(self, text):
        newText = []

        for k in text:
            if isinstance(text, str):
                newText.append(self.availableKeys.find(k))
            else:
                newText.append(self.availableKeys[k])

        return newText

    def updateDisplay(self):
        self.image = pygame.Surface((self.width, self.height))

        lastLineX = 0
        lastLineY = (self.image.get_height() - self.frameSize[1])

        lastLineX += self.frameSize[0]
        self.image.blit(
            self.sprite[self.translate(">")[0]], (lastLineX, lastLineY))

        # user typing
        for k in self.newLine:
            lastLineX += self.frameSize[0]
            self.image.blit(self.sprite[k], (lastLineX, lastLineY))

        # cursor
        if self.cursorBlinkCycles == 0:
            self.cursorBlinkCycles = 30

            if self.cursorBlink:
                self.cursor = -1
                self.cursorBlink = False
            else:
                self.cursor = self.translate("_")[0]
                self.cursorBlink = True

        if self.cursorBlinkCycles > 0:
            self.cursorBlinkCycles -= 1

        lastLineX += self.frameSize[0]
        self.image.blit(self.sprite[self.cursor], (lastLineX, lastLineY))

        # history
        lineIdx = 0
        for idx, line in reversed(list(enumerate(self.linesInput))):
            # response
            lineIdx += 1
            lastLineX = 0
            lastLineY -= self.frameSize[1] * 1
            for rline in self.linesResponse[idx]:
                for k in rline:
                    lastLineX += self.frameSize[0]
                    self.image.blit(self.sprite[k], (lastLineX, lastLineY))

            # user
            lineIdx += 1
            lastLineX = 0
            lastLineY -= self.frameSize[1] * 1
            for k in line:
                lastLineX += self.frameSize[0]
                self.image.blit(self.sprite[k], (lastLineX, lastLineY))
