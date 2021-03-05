#!/usr/bin/python

#-----------------------------------------------------------------------------------------------------------------------
#   Imports
#-----------------------------------------------------------------------------------------------------------------------
import os
import logging
import random
import math
import utils
import pygame
import pygame.gfxdraw as pygfx


#-----------------------------------------------------------------------------------------------------------------------
#   Game Class
#-----------------------------------------------------------------------------------------------------------------------
class SpaceWarsGame:

    #-----------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        self._initVars()
        self._initGame()
        self._initCanvas()
        self._loadResources()
        self._setTitleAndIcon()
        self._gameLoop()


    #-----------------------------------------------------------------------------------------------------------------------
    def _gameLoop(self):
        self.running = True 
        while self.running:
            self._checkGameInput()
            self._drawGameFrame()

            # Clamp FPS
            self.clock.tick_busy_loop(self.fps)


    #-----------------------------------------------------------------------------------------------------------------------
    def _initVars(self):
        #   Default
        self.gameVersion = "v0.0.1"
        self.fps = 60
        self.gameWindowWidth = 1600
        self.gameWindowHeight = 900
        self.gameWindowSurface = pygame.HWSURFACE|pygame.DOUBLEBUF#|pygame.RESIZABLE
        
        #   Input
        self.mouseDown = False

        #   Timer
        self.clock = pygame.time.Clock()

        self._initLogging()
        self._initColors()
        self._initHeroVars()
        self._initEnemyVars()
        self._initResources()


    #-----------------------------------------------------------------------------------------------------------------------
    def _initGame(self):
        pygame.init()

        # window centered
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.gameScreen = pygame.display.set_mode((self.gameWindowWidth, self.gameWindowHeight), self.gameWindowSurface)

        self._initBackground()

        #   Hide mouse cursor
        pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))

    #-----------------------------------------------------------------------------------------------------------------------
    def _initCanvas(self):
        self.gameCanvas = pygame.Surface((self.gameWindowWidth, self.gameWindowHeight))
        self.gameCanvas.fill(self.blackColor)


    #-----------------------------------------------------------------------------------------------------------------------
    def _initLogging(self):
        logging.basicConfig(filename="game.log", level=logging.DEBUG, format="%(asctime)s: %(levelname)s: %(message)s")
        logging.info("Log Init:")


    #-----------------------------------------------------------------------------------------------------------------------
    def _initHeroVars(self):
        self.heroX = (self.gameWindowWidth-64)/2
        self.heroY = self.gameWindowHeight-150
        self.heroSpeed = 4 


    #-----------------------------------------------------------------------------------------------------------------------
    def _initColors(self):
        self.blackColor = ( 0, 0, 0 )
        self.whiteColor = ( 255, 255, 255 )
        self.lightGrayColor = ( 200, 200, 200 )
        self.darkGrayColor = ( 150, 150, 150 )


    #-----------------------------------------------------------------------------------------------------------------------
    def _initEnemyVars(self):
        self.enemyStartX = 200
        self.enemyStartY = 100
        self.enemyEndX = self.gameWindowWidth-200-64
        self.enemyAmountX = 10
        self.enemyAmountY = 6
        self.enemyOffsetX = (self.enemyEndX - self.enemyStartX) / (self.enemyAmountX - 1)
        self.enemyOffsetY = 60
        self.enemyCurrentOffsetX = 0
        self.enemyCurrentOffsetY = 0
        self.enemySpeedX = 0.001
        self.enemySpeedY = 0


    #-----------------------------------------------------------------------------------------------------------------------
    def _initResources(self):
        self.imagesPath = os.path.dirname(os.path.abspath(__file__)) + "\\resource\\img\\"
        self.soundsPath = os.path.dirname(os.path.abspath(__file__)) + "\\resource\\sound\\"
        logging.info("Images Path: {}".format(self.imagesPath))
        logging.info("Sounds Path: {}".format(self.soundsPath))


    #-----------------------------------------------------------------------------------------------------------------------
    def _loadResources(self):
        self.iconSurface = self._loadImage("icon.png")
        self.heroSurface = self._loadImage("hero.png")
        self.enemySurface = self._loadImage("enemy_01.png")
        self.trophySurface = self._loadImage("trophy.png")
        self.explosionSurface = self._loadImage("explosion_01.png")
        #self.hudImg = self._loadImage("hud.png")


    #-----------------------------------------------------------------------------------------------------------------------
    def _setTitleAndIcon(self):
        pygame.display.set_caption("Space Wars Game " + self.gameVersion)
        if self.iconSurface != None:
            pygame.display.set_icon(self.iconSurface)

        
    #-----------------------------------------------------------------------------------------------------------------------
    def _checkGameInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouseDown = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouseDown = False

        #   Hero movement
        keys = pygame.key.get_pressed()
        self.heroX -= keys[pygame.K_LEFT] * self.heroSpeed 
        self.heroX += keys[pygame.K_RIGHT] * self.heroSpeed 
        self.heroX = utils.clamp(self.heroX, 100, self.gameWindowWidth-100-64)


    #-----------------------------------------------------------------------------------------------------------------------
    def _drawGameFrame(self):
        self._drawBackgrond()
        self._drawHero()
        self._drawEnemies()
        #self._drawItens()
        #self._drawEffects()
        #self._drawHUD()
        #self.TEST_MouseMovement()
        self._blitCanvas()


    #-----------------------------------------------------------------------------------------------------------------------
    def TEST_MouseMovement(self):
        # Mouse Movement
        if self.mouseDown:
            self.mousePos = pygame.mouse.get_pos()
            pygame.draw.circle(self.gameCanvas, self.whiteColor, self.mousePos, 5, 0)


    #-----------------------------------------------------------------------------------------------------------------------
    def _initBackground(self):
        self.starsLayer_01 = []
        self.starsLayer_02 = []
        self.starsLayer_03 = []

        self.startLayer01_Offset = 1
        self.startLayer02_Offset = 2
        self.startLayer03_Offset = 3

        self.startLayer01_CurrentOffset = 0
        self.startLayer02_CurrentOffset = 0
        self.startLayer03_CurrentOffset = 0

        starsAmount = 700

        # First layer
        for i in range(starsAmount):
            self.starsLayer_01.append([random.randint(0, self.gameWindowWidth), random.randint(0, self.gameWindowHeight)])

        # Second layer
        for i in range(starsAmount):
            self.starsLayer_02.append([random.randint(0, self.gameWindowWidth), random.randint(0, self.gameWindowHeight)])

        # Third layer
        for i in range(starsAmount):
            self.starsLayer_03.append([random.randint(0, self.gameWindowWidth), random.randint(0, self.gameWindowHeight)])

    #-----------------------------------------------------------------------------------------------------------------------
    def _drawBackgrond(self):
        self.gameCanvas.fill(self.blackColor)

        #pygame.draw.line(self.gameCanvas, self.whiteColor, (300,300), (350,300))
        #pygame.draw.circle( self.gameCanvas, self.whiteColor, mouse_pos, 5, 0 )

        for i in range(len(self.starsLayer_01)):
            pos_x = self.starsLayer_01[i][0]
            pos_y = (self.starsLayer_01[i][1] + self.startLayer01_CurrentOffset) % self.gameWindowHeight
            pygfx.pixel(self.gameCanvas, pos_x, pos_y, self.darkGrayColor)

        for i in range(len(self.starsLayer_02)):
            pos_x = self.starsLayer_02[i][0]
            pos_y = (self.starsLayer_02[i][1] + self.startLayer02_CurrentOffset) % self.gameWindowHeight
            pygfx.pixel(self.gameCanvas, pos_x, pos_y, self.lightGrayColor)

        for i in range(len(self.starsLayer_03)):
            pos_x = self.starsLayer_03[i][0]
            pos_y = (self.starsLayer_03[i][1] + self.startLayer03_CurrentOffset) % self.gameWindowHeight
            pygfx.pixel(self.gameCanvas, pos_x, pos_y, self.whiteColor)

        self.startLayer01_CurrentOffset += self.startLayer01_Offset
        self.startLayer02_CurrentOffset += self.startLayer02_Offset
        self.startLayer03_CurrentOffset += self.startLayer03_Offset


    #-----------------------------------------------------------------------------------------------------------------------
    def _drawHUD(self):
        self.gameCanvas.blit(self.hudImg, (500, 500))


    #-----------------------------------------------------------------------------------------------------------------------
    def _drawHero(self):
        if self.heroSurface != None:
            self.gameCanvas.blit(self.heroSurface, (self.heroX, self.heroY))


    #-----------------------------------------------------------------------------------------------------------------------
    def _drawEnemies(self):
        self.enemyCurrentOffsetX = math.sin(pygame.time.get_ticks() * self.enemySpeedX) * 100

        if self.enemySurface != None:
            for y in range(0, self.enemyAmountY):
                for x in range(0, self.enemyAmountX):
                    if y % 2 == 0:
                        offsetX = self.enemyCurrentOffsetX
                    else:
                        offsetX = -self.enemyCurrentOffsetX
                    self.gameCanvas.blit(self.enemySurface, (self.enemyStartX + (self.enemyOffsetX*x) + offsetX, self.enemyStartY + (self.enemyOffsetY*y)))



    #-----------------------------------------------------------------------------------------------------------------------
    def _drawItens(self):
        if self.trophySurface != None:
            self.gameCanvas.blit(self.trophySurface, (600, 200))


    #-----------------------------------------------------------------------------------------------------------------------
    def _drawEffects(self):
        if self.explosionSurface != None:
            self.gameCanvas.blit(self.explosionSurface, (800, 200))

    
    #-----------------------------------------------------------------------------------------------------------------------
    def _blitCanvas(self):
        self.gameScreen.blit(self.gameCanvas, (0, 0))
        pygame.display.flip()
        #pygame.display.update()


    #-----------------------------------------------------------------------------------------------------------------------
    def _loadImage(self, image):
        path = self.imagesPath+image
        logging.info("Resource: {}".format(path))
        return pygame.image.load(path)


    #-----------------------------------------------------------------------------------------------------------------------
    #def _loadSound(self, soundFileName):
    #    pass


    #-----------------------------------------------------------------------------------------------------------------------
    #def _playSound(self, sound):
    #    pass


#-----------------------------------------------------------------------------------------------------------------------
#   Main
#-----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    game = SpaceWarsGame()




