#################################################################
# Your Name: Sharon Liu
# Your Andrew ID: sharonli
# Term Project: Descending Light
#################################################################

# Import modules
import pygame
import sys
import time
from os import path
from Screens import *
from Constants import *
from AllSprites import *
from TileMap import *

#  ____         ____   ____   __ __   ____  
# |    | \   / |      |    | |  |  | |    
# |____|  \_/  |  __  |____| |  |  | |___  
# |        |   |    | |    | |     | |
# |        |   |____| |    | |     | |____ 

# Run game using this file

'''CITATION: Game class inspired by Lukas Peraza's framework:
   http://blog.lukasperaza.com/getting-started-with-pygame/'''
class PygameGame:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 4, 3000)
        pygame.init()
        self.screen = pygame.display.set_mode((screenWidth, screenHeight))
        pygame.display.set_caption(gameName)
        self.clock = pygame.time.Clock()
        self.loadExternalFiles()
        self.timeElapsed = 0
        self.fps = 60
        self.sec = self.clock.tick(self.fps)/1000.0
        self.showStairs = False
        self.isFloor1 = False
        self.isRoom112 = False
        self.mainMenu = True
        self.firstMainMenu = True
        self.score = 0 
    
    #Load files from different directories
    def loadExternalFiles(self):
        # Screen files
        self.startScreenImage = pygame.image.load(path.join(imageFolder, \
        startScreenImage)).convert_alpha()
        self.controlsImage = pygame.image.load(path.join(imageFolder, \
        controlsImage)).convert_alpha()
        self.objectiveF2 = pygame.image.load(path.join(imageFolder, \
        objectiveImageF2)).convert_alpha()
        self.objectiveF1 = pygame.image.load(path.join(imageFolder, \
        objectiveImageF1)).convert_alpha()
        self.objective112 = pygame.image.load(path.join(imageFolder, \
        objectiveImage112)).convert_alpha()
        self.mainMenuImage = pygame.image.load(path.join(imageFolder, \
        mainMenuImage)).convert_alpha()
        self.minimapF2 = pygame.image.load(path.join(imageFolder, \
        minimapF2)).convert_alpha()
        self.minimapF1 = pygame.image.load(path.join(imageFolder, \
        minimapF1)).convert_alpha()
        self.exitButton = pygame.image.load(path.join(imageFolder, \
        exitButton)).convert_alpha()
        self.creditsScreen = pygame.image.load(path.join(imageFolder, \
        creditsScreen)).convert_alpha()
        
        # Sprite images
        self.playerImage = pygame.image.load(path.join(imageFolder, \
        playerImage)).convert_alpha()
        self.bulletImage = {}
        self.bulletImage["handgun"] = pygame.image.load(path.join(imageFolder, \
        bulletImage)).convert_alpha()
        scaleMGBullet = (20, 10)
        self.bulletImage["machinegun"] = pygame.transform.scale(\
        self.bulletImage["handgun"], scaleMGBullet)
        scaleRBullet = (25, 10)
        self.bulletImage["rifle"] = pygame.transform.scale(\
        self.bulletImage["handgun"], scaleRBullet)
        self.zombieImage = pygame.image.load(path.join(imageFolder, \
        zombieImage)).convert_alpha()
        self.zombieStrongImage = pygame.image.load(path.join(imageFolder, \
        zombieStrongImage)).convert_alpha()
        self.zombieRandomImage = pygame.image.load(path.join(imageFolder, \
        zombieRandomImage)).convert_alpha()
        self.zombieBossImage = pygame.image.load(path.join(imageFolder, \
        zombieBossImage)).convert_alpha()
        self.healthImage = pygame.image.load(path.join(imageFolder, \
        playerHealthImage)).convert_alpha()
        self.healthImgRect = self.healthImage.get_rect()
        self.energyImage = pygame.image.load(path.join(imageFolder, \
        playerEnergyImage)).convert_alpha()
        self.energyImgRect = self.energyImage.get_rect()
        self.stairsImg = pygame.image.load(path.join(imageFolder, \
        stairsImage)).convert_alpha()
        self.stairsImg = pygame.transform.rotate(self.stairsImg, 90)
        self.stairsImgRect = self.stairsImg.get_rect()
        self.stairsLastImg = pygame.image.load(path.join(imageFolder, \
        stairsLastImage)).convert_alpha()
        self.stairsLastImgRect = self.stairsLastImg.get_rect()
        self.bloodImage = pygame.image.load(path.join(imageFolder, \
        zombieBloodSplatterImage)).convert_alpha()
        self.bloodStrImage = pygame.image.load(path.join(imageFolder, \
        zombieStrongBloodSplatterImage)).convert_alpha()
        self.bloodRandImage = pygame.image.load(path.join(imageFolder, \
        zombieRandomBloodSplatterImage)).convert_alpha()
        self.bloodBossImage = pygame.image.load(path.join(imageFolder, \
        zombieBossBloodSplatterImage)).convert_alpha()
        scaleX, scaleY = 256, 256
        self.bloodBossImage = pygame.transform.scale(self.bloodBossImage, \
        (scaleX, scaleY))
        
        # Item images
        self.bulletFireImgs = []
        self.allItemImages = {}
        for fires in bulletFireImgs:
            self.bulletFireImgs.append(pygame.image.load(path.join(imageFolder,\
            fires)).convert_alpha())
        for item in allItemImages:
            self.allItemImages[item] = pygame.image.load(path.join(imageFolder,\
            allItemImages[item])).convert_alpha()
            
        # All sound files
        self.soundEffects = {}
        for sounds in extraSounds:
            self.soundEffects[sounds] = pygame.mixer.Sound(path.join( \
            soundsFolder, extraSounds[sounds]))
        self.currWeaponSounds = {}
        for weapon in weaponSounds:
            self.currWeaponSounds[weapon] = []
            for sounds in weaponSounds[weapon]:
                sd = pygame.mixer.Sound(path.join(soundsFolder, sounds))
                sd.set_volume(0.15)
                self.currWeaponSounds[weapon].append(sd)
        self.zombieSounds = []
        for sounds in zombieGrowls:
            sound = pygame.mixer.Sound(path.join(soundsFolder, sounds))
            sound.set_volume(0.15)
            self.zombieSounds.append(sound)
        self.bossZombieScreams = []
        for sounds in bossZombieScreams:
            sound = pygame.mixer.Sound(path.join(soundsFolder, sounds))
            sound.set_volume(0.6)
            self.bossZombieScreams.append(sound)
        self.bossDeathSounds = []
        for sounds in bossDeathSounds:
            sound = pygame.mixer.Sound(path.join(soundsFolder, sounds))
            self.bossDeathSounds.append(sound)
        self.playerOofSounds = []
        for sounds in playerOofSounds:
            self.playerOofSounds.append(pygame.mixer.Sound(path.join(\
            soundsFolder, sounds)))
        self.gutsSquishSounds = []
        for sounds in gutsSquishSounds:
            self.gutsSquishSounds.append(pygame.mixer.Sound(path.join(\
            soundsFolder, sounds)))
            
        # Screen texts
        '''CITATION: 
        -Main font: https://www.dafont.com/cold-night-for-alligators.font
        -Score font: https://www.dafont.com/diediedie.font'''
        self.mainFont = path.join(imageFolder, "cnfa.ttf")
        self.scoreFont = path.join(imageFolder, "ddd.ttf")
        self.transpScreen = pygame.Surface(self.screen.get_size()).convert_alpha()
        self.transpScreen.fill((0, 0, 0, 170))
        self.saveScore()
        
    # Keep track of player score throughout the levels
    def saveScore(self):
        with open(path.join(scoreFolder, bestScore), 'r+') as file:
            try:
                self.bestScore = int(file.read())
            except:
                self.bestScore = 0
    
    # Re-initialize sprites and positions everytime game is rerun
    def reloadGame(self):
        # Init sprite groups
        self.allSpritesGroup = pygame.sprite.LayeredUpdates()
        self.walls = pygame.sprite.Group()
        self.holes = pygame.sprite.Group()
        self.stairs = pygame.sprite.Group()
        self.lastStairs = self.stairs.copy()
        self.zombies = pygame.sprite.Group()
        self.zombiesStrong = pygame.sprite.Group()
        self.zombiesRandom = pygame.sprite.Group()
        self.zombieBoss = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.notes = pygame.sprite.Group()
        self.showCollisionRects = False
        # Splash screens
        self.pause = False
        self.controls = False
        self.minimap = False
        self.objective = False
        self.lastScreen = False
        self.credits = False
        
        # Change floor maps on appropriate level
        if not self.isFloor1:
            self.changeFloorMaps()
            self.currentFloor()
        elif self.isFloor1 and not self.isRoom112:
            self.changeFloorMaps()
            self.currentFloor()
        elif self.isRoom112:
            self.changeFloorMaps()
            self.currentFloor()
    
    # Floor map levels changing
    def changeFloorMaps(self):
        if self.isFloor1 == False and self.isRoom112 == False:
            self.currMap = startMap
        elif self.isFloor1 == True and self.isRoom112 == False:
            self.mainMenu = False
            self.currMap = 'floor1_map.tmx'
        elif self.isFloor1 == False and self.isRoom112 == True:
            self.mainMenu = False
            self.minimap = False
            self.currMap = 'room112.tmx'
    
    # Instantiate all non-moving objects in the current Floor
    def currentFloor(self):
        #Every time game loads: init all sprite groups
        self.floor = TileMap(path.join(mapsFolder, self.currMap))
        self.floorImage = self.floor.generateTileMap()
        self.floorRect = self.floorImage.get_rect()
        for obj in self.floor.TileMapData.objects:
            xCenter = obj.x + obj.width//2
            yCenter = obj.y + obj.height//2
            objCenter = vector(xCenter, yCenter)
            if obj.name == "Player":
                self.player = Player(self, objCenter.x, objCenter.y)
            if obj.name == "Wall":
                BlockObstacles(self, obj.x, obj.y, obj.width, obj.height)
            if obj.name == "Hole":
                Hole(self, obj.x, obj.y, obj.width, obj.height)
            if obj.name == "Stairs":
                stairs = Stairs(self, objCenter.x, objCenter.y)
                stairs.image = pygame.transform.rotate(stairs.image, -90)
            if obj.name == "Last Stairs":
                stairs = LastStairs(self, objCenter.x, objCenter.y)
        self.spawnRecurring()
        self.screenScroll = ScreenScroll(self.floor.width, self.floor.height)
    
    # Instantiate all moving objects 
    def spawnRecurring(self):
        for obj in self.floor.TileMapData.objects:
            xCenter = obj.x + obj.width//2
            yCenter = obj.y + obj.height//2
            objCenter = vector(xCenter, yCenter)
            if obj.name == "Zombie":
                Zombie(self, objCenter.x, objCenter.y)
            if obj.name == "StrongZombie":
                StrongZombie(self, objCenter.x, objCenter.y)
            if obj.name == "RandomZombie":
                RandomZombie(self, objCenter.x, objCenter.y)
            if obj.name == "BossZombie":
                self.boss = BossZombie(self, objCenter.x, objCenter.y)
            for itemType in allItemImages:
                if obj.name == itemType:
                    Items(self, objCenter, obj.name)
    
    # Update sprite motion and movement frames
    def update(self):
        self.allSpritesGroup.update()
        self.screenScroll.update(self.player)
        # Track all different sprite collisions
        self.playerCollisions()
        self.enemyAndWeaponHits(self.zombies, zombieKnockback)
        self.enemyAndWeaponHits(self.zombiesStrong, zombieStrongKnockback)
        self.enemyAndWeaponHits(self.zombiesRandom, zombieRandomKnockback)
        self.enemyAndWeaponHits(self.zombieBoss, zombieBossKnockback)
    
    # All sprite to sprite collisions
    def playerCollisions(self):
        # Powerups:
        itemGetHit = pygame.sprite.spritecollide(self.player, self.items, False)
        for item in itemGetHit:
            if item.itemType == "Food" and self.player.health < playerHealth:
                item.kill()
                self.soundEffects["itemPickup"].play()
                self.player.restoreHealth(healthRestoreAmt)
            if item.itemType == "Bad food" and self.player.health < playerHealth:
                item.kill()
                self.soundEffects["itemPickup"].play()
                self.player.restoreHealth(badFoodHealthRestoreAmt)
            if item.itemType == "Drink" and self.player.energy < playerEnergy:
                item.kill()
                self.soundEffects["itemPickup"].play()
                self.player.restoreEnergy(energyRestoreAmt)
            if item.itemType == "Machinegun":
                item.kill()
                self.soundEffects["gunSelect"].play()
                self.player.currWeapon = "machinegun"
            if item.itemType == "Rifle":
                item.kill()
                self.soundEffects["gunSelect"].play()
                self.player.currWeapon = "rifle"
                
        # Stairs to Flr 1:
        stairsGetHit = pygame.sprite.spritecollide(self.player, \
        self.stairs, False)
        for hits in stairsGetHit:
            if stairsGetHit:
                self.isFloor1 = not self.isFloor1
                self.playing = False
                
        # Stairs to Room 112:
        stairsGetHit = pygame.sprite.spritecollide(self.player, \
        self.lastStairs, False)
        for hits in stairsGetHit:
            if stairsGetHit:
                self.isFloor1 = not self.isFloor1
                self.isRoom112 = True
                self.playing = False        
    
    def showScore(self):
        with open(path.join(scoreFolder, bestScore), 'r+') as file:
            file.write(str(self.bestScore))
    
    # Keep track of enemy collisions and weapon collisions
    def enemyAndWeaponHits(self, zombieType, knockBack):
        playerGetHit = pygame.sprite.spritecollide(self.player, zombieType, \
        False, checkCollisionRect)
        # Non-boss zombies and player collisions
        if zombieType != self.zombieBoss:
            for attacks in playerGetHit:
                if random() < 0.5:
                    choice(self.playerOofSounds).play()
                self.player.health -= zombieDamage
                attacks.velocity = vector(0, 0)
                if self.player.health <= 0:
                    self.playing = False
            if playerGetHit:
                posChange = vector(knockBack, 0).rotate(-playerGetHit[0].rotate)
                self.player.position += posChange
        else:
            # Boss and player sprite collision
            playerGetHit = pygame.sprite.spritecollide(self.player, \
            zombieType, False)
            for attacks in playerGetHit:
                if random() < 0.7:
                    choice(self.playerOofSounds).play()
                self.player.health -= zombieDamage
                attacks.velocity = vector(0, 0)
                if self.player.health <= 0:
                    self.playing = False
            if playerGetHit:
                posChange = vector(knockBack, 0).rotate(-playerGetHit[0].rotate)
                self.player.position += posChange
                
        #Bullets hurt Zombies
        zombieGetHit = pygame.sprite.groupcollide(zombieType, self.bullets, \
        False, True)
        for zombs in zombieGetHit:
            zombs.health -= weapons[self.player.currWeapon]["bulletDamage"]
            if zombieType != self.zombiesRandom:
                zombs.velocity = vector(3, 3)
    
    # Main screen text-maker
    def createText(self, text, fontName, txtSize, color, left, right, anchor):
        font = pygame.font.Font(fontName, txtSize)
        txtcanvas = font.render(text, True, color)
        txtRect = txtcanvas.get_rect()
        txtanchor = (left, right)
        if anchor == "nw":
            txtRect.topleft = txtanchor
        elif anchor == "ne":
            txtRect.topright = txtanchor
        elif anchor == "sw":
            txtRect.bottomleft = txtanchor
        elif anchor == "se":
            txtRect.bottomright = txtanchor
        elif anchor == "ct":
            txtRect.center = txtanchor
        self.screen.blit(txtcanvas, txtRect)
    
    # Draw player health and energy bars
    def drawPlayerHealthBar(self, x, y, fractionHealth):
        barLength = 200
        barHeight = 15
        health = fractionHealth * barLength
        outLine = pygame.Rect(x, y, barLength, barHeight)
        healthRect = pygame.Rect(x, y, health, barHeight)
        if fractionHealth < 0:
            fractionHealth = 0
        if fractionHealth > (3/5):
            color = green
        elif fractionHealth > (3/10):
            color = yellow
        else:
            color = red
        barFill = pygame.draw.rect(self.screen, color, healthRect)
        barOutline = pygame.draw.rect(self.screen, white, outLine, 1)
        
    def drawPlayerEnergyBar(self, x, y, fractionEnergy):
        barLength = 200
        barHeight = 15
        energy = fractionEnergy * barLength
        outLine = pygame.Rect(x, y, barLength, barHeight)
        energyRect = pygame.Rect(x, y, energy, barHeight)
        if fractionEnergy < 0:
            fractionEnergy = 0
        if fractionEnergy > (3/5):
            color = yellow
        elif fractionEnergy > (3/10):
            color = orange
        else:
            color = red
        barFill = pygame.draw.rect(self.screen, color, energyRect)
        barOutline = pygame.draw.rect(self.screen, white, outLine, 1)
    
    # Continue updating sprites
    def redrawAll(self):
        self.screen.blit(self.floorImage, self.screenScroll.moveWindowRect(self.floorRect))
        for sprite in self.allSpritesGroup:
            if isinstance(sprite, Zombie):
                sprite.displayZombieHealth() 
            if isinstance(sprite, StrongZombie):
                sprite.displayZombieHealth() 
            if isinstance(sprite, RandomZombie):
                sprite.displayZombieHealth() 
            if isinstance(sprite, BossZombie):
                sprite.displayZombieHealth() 
            self.screen.blit(sprite.image, self.screenScroll.moveWindow(sprite))
            if self.showCollisionRects:
                pygame.draw.rect(self.screen, white, \
                self.screenScroll.moveWindowRect(sprite.collideRect), 1)
        if self.showCollisionRects:
            for wall in self.walls:
                pygame.draw.rect(self.screen, white, \
                self.screenScroll.moveWindowRect(wall.rect), 1)
            for hole in self.holes:
                pygame.draw.rect(self.screen, white, \
                self.screenScroll.moveWindowRect(hole.rect), 1)
                
        # Plater attributes on top of screen
        self.createText("SCORE: " + str(self.score), self.scoreFont, 30, 
                        white, 4, 2, anchor="nw") 
        barLen = 200
        margin = 10
        xLoc = screenWidth - barLen - margin
        yLocH = 10
        yLocE = 40
        self.drawPlayerHealthBar(xLoc, yLocH, self.player.health/playerHealth)
        self.healthImgRect.center = (580, 5)
        self.screen.blit(self.healthImage, self.healthImgRect.center)
        self.drawPlayerEnergyBar(xLoc, yLocE, self.player.energy/playerEnergy)
        self.energyImgRect.center = (580, 35)
        self.screen.blit(self.energyImage, self.energyImgRect.center)
        
        #Splash screens
        if self.pause:
            self.screen.blit(self.transpScreen, (0, 0))
            self.createText("Paused", self.mainFont, 180, darkred, 
                            screenWidth//2, screenHeight//2, anchor="ct")
        if self.controls:
            self.displayControlsScreen()
        if self.minimap:
            if not self.isFloor1:
                self.displayMiniMap(self.minimapF2)
            elif self.isFloor1:
                self.displayMiniMap(self.minimapF1)
            else:
                self.minimap = False
        if self.objective:
            if not self.isFloor1 and not self.isRoom112:
                self.displayObjectiveScreenFlr2()
            elif self.isFloor1 and not self.isRoom112:
                self.displayObjectiveScreenFlr1()
            elif self.isRoom112 and not self.isFloor1:
                self.displayObjectiveScreenRoom112()
        if self.mainMenu:
            self.displayMainMenu()
        if self.lastScreen:
            self.displayLastScreen()
        if self.credits:
            self.displayCreditsScreen()
        pygame.display.flip()
    
    '''' CITATION: keyPressed function adapted from Lukas Peraza framework:
            http://blog.lukasperaza.com/getting-started-with-pygame/'''
    def keyPressed(self):
        # keyPressed below
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                if not self.firstMainMenu:
                    if event.key == pygame.K_ESCAPE:
                        self.objective = False
                        self.minimap = False
                        self.controls = False
                        self.lastScreen = False
                        self.mainMenu = not self.mainMenu
                    if not self.mainMenu or self.lastScreen:
                        if event.key == pygame.K_p:
                            self.pause = not self.pause
                            self.objective = False
                            self.minimap = False
                            self.controls = False
                        if event.key == pygame.K_m:
                            if not self.pause:
                                self.minimap = not self.minimap
                                self.objective = False
                                self.controls = False
                        if event.key == pygame.K_o:
                            if not self.pause:
                                self.objective = not self.objective
                                self.minimap = False
                                self.controls = False
        
    # Display all Splash screens
    def displayObjectiveScreenFlr1(self):
        self.screen.blit(self.objectiveF1, (0, 0))
        pygame.display.flip()
        
    def displayObjectiveScreenFlr2(self):
        self.screen.blit(self.objectiveF2, (0, 0))
        pygame.display.flip()
    
    def displayObjectiveScreenRoom112(self):
        self.screen.blit(self.objective112, (0, 0))
        pygame.display.flip()
    
    def displayLastScreen(self):
        self.screen.blit(self.transpScreen, (0,0))
        self.createText("You won! Your total score is " + str(self.score), 
                            self.scoreFont, 50, white, \
                            screenWidth//2, screenHeight//2, anchor = "ct")
        pygame.display.flip()
    
    def displayCreditsScreen(self):
        buttonSize = 28
        buttonX, buttonY = screenWidth - 38, 10
        self.screen.blit(self.creditsScreen, (0, 0))
        self.screen.blit(self.exitButton, (buttonX, buttonY))
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        # Check in bounds of exit button
        if buttonX < mouse[0] < buttonX + buttonSize and \
        buttonY < mouse[1] < buttonY + buttonSize:
            if click[0] == 1:
                self.mainMenu = True
                self.credits = False
        pygame.display.flip()
    
    def displayMainMenu(self):
        margin = 5
        startX = 50
        shiftAmt = 60
        buttonWidth, buttonHeight = 200, 30
        self.screen.blit(self.mainMenuImage, (0, 0))
        self.createText("DESCENDING LIGHT \n MAIN MENU", self.mainFont, 60, \
        red, screenWidth//2, screenHeight//5, anchor="ct")
        newRect = (startX, screenHeight//2 - shiftAmt, buttonWidth, buttonHeight)
        saveRect = (startX, screenHeight//2, buttonWidth, buttonHeight)
        loadRect = (startX, screenHeight//2 + shiftAmt, buttonWidth, buttonHeight)
        exitRect = (startX, screenHeight//2 + 2*shiftAmt, buttonWidth, buttonHeight)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        # Check in bounds of new game button
        if startX < mouse[0] < startX + buttonWidth and \
        screenHeight//2 - shiftAmt < mouse[1] < screenHeight//2 - buttonHeight:
            pygame.draw.rect(self.screen, lightgray, (newRect))
            if click[0] == 1:
                self.firstMainMenu = False
                self.mainMenu = False
                self.reloadGame()
                self.fadeScreen()
                self.objective = True
                self.score = 0
        # Check in bounds of controls button
        if startX < mouse[0] < startX + buttonWidth and \
        screenHeight//2 < mouse[1] < screenHeight//2 + buttonHeight:
            pygame.draw.rect(self.screen, lightgray, (saveRect))
            if click[0] == 1:
                self.mainMenu = False
                self.controls = True
                self.minimap = False
                self.objective = False
        # Check in bounds of credits button 
        if startX < mouse[0] < startX + buttonWidth and \
        screenHeight//2 + shiftAmt < mouse[1] < screenHeight//2 + buttonHeight*3:
            pygame.draw.rect(self.screen, lightgray, (loadRect))
            if click[0] == 1:
                self.mainMenu = False
                self.minimap = False
                self.objective = False
                self.credits = True
        # Check in bounds of exit button
        if startX < mouse[0] < startX + buttonWidth and \
        screenHeight//2 + 2*shiftAmt < mouse[1] < screenHeight//2 + buttonHeight*5:
            pygame.draw.rect(self.screen, lightgray, (exitRect))
            if click[0] == 1:
                self.quit()
        pygame.draw.rect(self.screen, white, (newRect), 3)
        self.createText("NEW GAME", self.mainFont, 30, red, 95, \
        screenHeight//2-shiftAmt+margin, anchor="nw")
        pygame.draw.rect(self.screen, white, (saveRect), 3)
        self.createText("CONTROLS", self.mainFont, 30, red, 95, \
        screenHeight//2+margin, anchor="nw")
        pygame.draw.rect(self.screen, white, (loadRect), 3)
        self.createText("CREDITS", self.mainFont, 30, red, 95, \
        screenHeight//2+shiftAmt+margin, anchor="nw")
        pygame.draw.rect(self.screen, white, (exitRect), 3)
        self.createText("EXIT GAME", self.mainFont, 30, red, 95, \
        screenHeight//2+120+margin, anchor="nw")
        self.createText("Press 'esc' to return to game", self.mainFont, \
        25, white, screenWidth//3, screenHeight*(6/7), anchor="nw")
        pygame.display.flip()
    
    def displayControlsScreen(self):
        buttonSize = 28
        buttonX, buttonY = screenWidth - 38, 10
        self.screen.blit(self.controlsImage, (0, 0))
        self.screen.blit(self.exitButton, (buttonX, buttonY))
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        # Check in bounds of exit button
        if buttonX < mouse[0] < buttonX + buttonSize and \
        buttonY < mouse[1] < buttonY + buttonSize:
            if click[0] == 1:
                self.controls = False
                self.mainMenu = True
        pygame.display.flip()
    
    def displayMiniMap(self, currFloor):
        marginX = 5
        marginY = 45
        self.screen.blit(currFloor, (marginX, marginY))
        pygame.display.flip()
    
    def displayCurrentScene(self):
        self.changeFloorMaps()
        self.currentFloor()
    
    def displayStartScreen(self):
        pygame.mixer.music.load(path.join(musicFolder, startingMusic))
        pygame.mixer.music.play(loops=-1)
        self.screen.blit(self.startScreenImage, (0, 0))
        pygame.display.flip()
        self.detectKeyPress()
    
    def displayGameOverScreen(self):
        self.screen.blit(self.transpScreen, (0,0))
        self.createText("YOU DIED", self.mainFont, 180, darkred, \
        screenWidth//2, screenHeight//3, anchor="ct")
        self.createText("Press a key to restart", self.mainFont, 50, \
        white, screenWidth//2, screenHeight*(2/3), anchor="ct")
        pygame.display.flip()
        self.detectKeyPress()
    
    def detectKeyPress(self):
        pygame.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pygame.KEYUP:
                    waiting = False
    
    # Fade effect for screen
    def fadeScreen(self): 
        screen = pygame.Surface((screenWidth, screenHeight))
        screen.fill(black)
        for color in range(0, 255):
            screen.set_alpha(color)
            self.fillColor()
            self.screen.blit(screen, (0,0))
            pygame.display.update()
            pygame.time.delay(5)
            
    def fillColor(self):
        self.screen.fill(lightgray)
    
    def quit(self):
        pygame.quit()
        sys.exit()
        
    '''CITATION: Run function influenced by @Lukas Peraza starter code:
        http://blog.lukasperaza.com/getting-started-with-pygame/'''    
    def run(self):
        self.playing = True
        # Play appropriate music for floor levels
        if self.isFloor1 == False and self.isRoom112 == False:
            self.displayMainMenu()
            pygame.mixer.music.load(path.join(musicFolder, floor2Music))
        elif self.isFloor1 == True and self.isRoom112 == False:
            self.objective = True
            pygame.mixer.music.load(path.join(musicFolder, floor1Music))
            pygame.mixer.music.set_volume(0.75)
        else:
            time.sleep(3)
            self.objective = True
            pygame.mixer.music.load(path.join(musicFolder, room112Music))
            pygame.mixer.music.set_volume(0.2)
            playerCoords = self.player.position
            bossCoords = vector(self.boss.x, self.boss.y)
            # Calculate route to player from boss
            self.route = AStarRoute(self.floor, playerCoords, bossCoords)
        
        # As game is running
        pygame.mixer.music.play(-1)
        while self.playing:
            self.sec = self.clock.tick(self.fps)/1000
            self.keyPressed()
            if not self.pause and not self.mainMenu and \
            not self.controls and not self.credits:
                self.timeElapsed += self.sec
                if self.timeElapsed > 10:
                    self.player.loseEnergy()
                    self.timeElapsed = 0
                if self.player.health <= 0:
                    self.playing = False
                if self.currMap == "room112.tmx":
                    self.minimap = False
                    playerCoords = self.player.position
                    bossCoords = self.boss.position
                    # Recalculate route to player from boss
                    self.route = AStarRoute(self.floor, playerCoords, bossCoords)
                self.update()
            self.redrawAll()

#Run and create an instance of PygameGame
running = True
g = PygameGame()
g.displayStartScreen()
while running:
    g.reloadGame()
    g.run()
    if g.player.health <= 0:
        g.displayGameOverScreen() 
        g.score = 0
    g.fadeScreen()
