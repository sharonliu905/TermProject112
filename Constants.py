# Import modules
from os import path
import pygame as pygame
vector = pygame.math.Vector2

''' Global Variable Customizations
Outline inspired by: 
https://github.com/MattR0se/Dungeon-Crusader/blob/master/modules/settings.py '''

#  _____   _____          _____  _____   _____         _____  _____
# |       |     | |\   | |         |    |     | |\   |   |   |
# |       |     | | \  | |_____    |    |_____| | \  |   |   |_____ 
# |       |     | |  \ |       |   |    |     | |  \ |   |         |
# |_____  |_____| |   \|  _____|   |    |     | |   \|   |    _____|

# Keep constant variables global to access through other files
 
# Folder Loads:
gameFolder = path.dirname(__file__)
assetsFolder = path.join(gameFolder, 'Assets')
imageFolder = path.join(gameFolder, 'images')
mapsFolder = path.join(gameFolder, 'maps')
soundsFolder = path.join(assetsFolder, 'sounds')
musicFolder = path.join(assetsFolder, 'music')
scoreFolder = path.join(assetsFolder, 'scores')

'''CITATION: 
-Credits img link:
https://coub.com/view/1ew326
-ObjectiveF2 img link:
https://steamcommunity.com/market/listings/753/325150-Alice%20City%20at%20Night
-ObjectiveF1 img link:
https://anime.desktopnexus.com/get/1888768/?t=9rkbdbeih3293nboo4519ja3j05ccb161c4a121
-ObjectiveImg112 link:
https://www.deviantart.com/pukahuna/art/Jungle-Cave-Background-622040796
'''
# Menus
controlsImage = 'controls.png'
objectiveImageF2 = 'objectiveF2.png'
objectiveImageF1 = 'objectiveF1.png'
objectiveImage112 = 'objective112.png'
minimapF2 = 'floor2_minimap.png'
minimapF1 = 'floor1_minimap.png'
mainMenuImage = 'night.jpg'
creditsScreen = 'credits.png'
exitButton = 'exit.png'

# Color customizations
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
darkred = (200, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
orange = (255, 165, 0) 
yellow = (255, 255, 0)
brown = (106, 55, 5)
lightgray = (120, 120, 120)

# Canvas customizations
startMap = 'floor2_map.tmx'
screenWidth = 800   
screenHeight = 600 
gameName = "Descending Light..."
backgroundColor = black
startScreenImage = 'titleScreen.png'
tileSize = 64
gridScreenWidth = screenWidth / tileSize
gridScreenHeight = screenHeight / tileSize
bestScore = 'bestScore.txt'
currScore = 'score.txt'

# Gun customizations
bulletImage = "bullet.png"
bulletFireImgs = ["gunfire.png", "gunfire2.png", "gunfire3.png"]
bulletOffset = vector(25, 5)
bulletTimeFlash = 45
weapons = {}
weapons['handgun'] = {"bulletSpeed" : 500, 
                     "bulletLifetime" : 1000,
                     "bulletFireRate" : 250,
                     "bulletRecoilRate" : 200,
                     "bulletStray" : 3,
                     "bulletDamage" : 20,
                     "bulletSize" : "handgun",
                     "bulletCount" : 1}
weapons['machinegun'] = {"bulletSpeed" : 600, 
                     "bulletLifetime" : 500,
                     "bulletFireRate" : 500,
                     "bulletRecoilRate" : 300,
                     "bulletStray" : 6,
                     "bulletDamage" : 40,
                     "bulletSize" : "machinegun",
                     "bulletCount" : 2}
weapons['rifle'] = {"bulletSpeed" : 400, 
                     "bulletLifetime" : 800,
                     "bulletFireRate" : 400,
                     "bulletRecoilRate" : 250,
                     "bulletStray" : 5,
                     "bulletDamage" : 50,
                     "bulletSize" : "rifle",
                     "bulletCount" : 4}

# Player customizations
playerSpeed = 200
playerRotationSpeed = 200
playerImage = 'player2.png'
playerImageLeft = 'player.png'
playerCollideRect = pygame.Rect(0, 0, 30, 30)
playerHealth = 100
playerEnergy = 85
playerHealthImage = "heart.png"
playerEnergyImage = "energy.png"
playerEnergyExhaust = 5
playerEnergyExhaustDamage = 3

'''CITATION: Zombie images inspired by:
https://www.pinterest.com/pin/348958671112242858/
https://www.deviantart.com/tdeleeuw/art/Top-down-Characters-pixel-art-424298098'''

# Zombie customizations
zombieImage = 'zombie1.png'
zombieSpeeds = [50, 80, 150, 175, 125, 115]
zombieCollideRect = pygame.Rect(0, 0, 45, 45)
zombieHealth = 100
zombieDamage = 5
zombieKnockback = 10
zombieCoverRadii = 50
zombieDetectPlayerRadii = 400
zombieBloodSplatterImage = "bloodSplatRed.png"

# Zombie Strong customizations
zombieStrongImage = 'zombie2.png'
zombieStrongSpeeds = [100, 120, 140, 160, 180, 200]
zombieStrongCollideRect = pygame.Rect(0, 0, 45, 45)
zombieStrongHealth = 250
zombieStrongDamage = 10
zombieStrongKnockback = 15
zombieStrongCoverRadii = 50
zombieStrongDetectPlayerRadii = 500
zombieStrongBloodSplatterImage = "bloodSplatGreen.png"

# Zombie Random customizations
zombieRandomImage = 'zombie3.png'
zombieRandomCollideRect = pygame.Rect(0, 0, 45, 45)
zombieRandomHealth = 300
zombieRandomDamage = 15
zombieRandomKnockback = 15
zombieRandomDetectPlayerRadii = 200
zombieRandomBloodSplatterImage = "bloodSplatBlue.png"

# Zombie Boss customizations
zombieBossImage = 'bossZombie.png'
zombieBossSpeed = 100
zombieBossCollideRect = pygame.Rect(0, 0, 75, 75)
zombieBossHealth = 3500
zombieBossSpeed = 50
zombieBossDamage = 20
zombieBossKnockback = 20
zombieBossDetectPlayerRadii = 250
zombieBossBloodSplatterImage = "bloodSplatYellow.png"

# Sprite Layers
wallLayer = 4
playerLayer = 2
zombieLayer = 2
bulletLayer = 3
bulletFlashLayer = 4
barLayer = 5

''' CITATION: Images inspired by pixel art @pinterest:
    https://www.pinterest.com/pin/293719206943086140/
-Pizza img: http://rebloggy.com/post/food-pizza-pixel-art-pixel/33858685246'''
# Item images:
allItemImages = {"Food" : "pizza.png", 
                "Drink" : "coffee.png", 
                "Bad food" : "cockroach.png",
                "Machinegun" : "machinegun.png",
                "Rifle" : "rifle.png"}

# Level images:
stairsImage = 'stairs2.png'
stairsLastImage = 'stairs.png'
                      
# Item properties
healthRestoreAmt = 20
badFoodHealthRestoreAmt = 5
energyRestoreAmt = 17
jumpAmt = 8
jumpSpeed = 0.25

'''CITATION: Audio information inside soundSources.txt in sounds folder
             Music sound info in musicSources.txt folder'''
# Sound effects
startingMusic = 'salem.wav'
floor2Music = 'sociopath.wav'
floor1Music = 'hunter.wav'
room112Music = 'Leviathan.mp3'
creditsMusic = 'Low.mp3'
playerOofSounds = ['oof1.wav', 'oof2.wav', 'oof3.wav', 'oof4.wav']
zombieGrowls = ['zombie1.wav','zombie2.wav','zombie3.wav','zombie5.wav',
                    'zombie6.wav']
bossZombieScreams = ['bossScream.wav', 'bossScream2.wav']
bossDeathSounds = ['bossDeath.ogg']
gutsSquishSounds = ['squish1.wav', 'squish2.wav', 'squish3.wav']
weaponSounds = {'handgun' : ['handgun.aiff'],
                'machinegun' : ['machinegun.ogg'],
                'rifle' : ['rifle.wav']}
extraSounds = {'itemPickup': 'itemPickup.wav',
                'gunSelect' : 'gunPickup.wav'}
