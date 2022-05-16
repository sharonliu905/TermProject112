# Import modules
from random import uniform, choice, randint, random
import pytweening as pt
from Constants import *
from TileMap import *
import os
from os import path
vector = pygame.math.Vector2

#  ____   ____   ____    _____  ____  ____
# |      |    | |    | |   |   |     |
# |____  |____| |____| |   |   |____ |____
#      | |      |   \  |   |   |          |
#  ____| |      |    \ |   |   |____  ____|

# Keeps track of all sprites used in game

####    Player   ####
class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.x = x
        self.y = y
        self._layer = playerLayer
        self.groups = game.allSpritesGroup
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.playerImage
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.collideRect = playerCollideRect
        self.collideRect.center = self.rect.center
        self.velocity = vector(0, 0)
        self.position = vector(self.x, self.y)
        self.rotate = -90
        self.health = playerHealth
        self.energy = playerEnergy
        self.currWeapon = "handgun"
        self.lastTimeFired = 0
        self.weaponChange()
        
    '''CITATION: Move function inspired by Lukas Peraza keypressed fn:
    http://blog.lukasperaza.com/getting-started-with-pygame/'''
    def movePlayer(self):
        if self.game.currMap != "room112.tmx":
            self.speed = playerSpeed
        else:
            # Slow player down during boss battle
            self.speed = playerSpeed*(2/3)
        self.velocity = vector(0, 0)
        keys = pygame.key.get_pressed()
        # Move left
        if keys[pygame.K_a]:
            self.velocity = vector(-self.speed, 0)
            self.image = pygame.transform.rotate(self.game.playerImage, 180)
            self.rotate = 180
            if self.energy < (1/3)*playerEnergy:
                self.velocity = vector(-self.speed/2, 0)
        # Move right
        if keys[pygame.K_d]:
            self.velocity = vector(self.speed, 0)
            self.image = pygame.transform.rotate(self.game.playerImage, 0)
            self.rotate = 0
            if self.energy < (1/3)*playerEnergy:
                self.velocity = vector(self.speed/2, 0)
        # Move up
        if keys[pygame.K_w]:
            self.velocity = vector(0, -self.speed)
            self.image = pygame.transform.rotate(self.game.playerImage, 90)
            self.rotate = 90
            if self.energy < (1/3)*playerEnergy:
                self.velocity = vector(0, -self.speed/2)
        # Move down
        if keys[pygame.K_s]:
            self.velocity = vector(0, self.speed)
            self.image = pygame.transform.rotate(self.game.playerImage, -90)
            self.rotate = -90
            if self.energy < (1/3)*playerEnergy:
                self.velocity = vector(0, self.speed/2)
                
        # Rotate counter clockwise
        if keys[pygame.K_q]:
            rotateAmt = 5
            self.rotate += rotateAmt
        
        # Rotate clockwise
        if keys[pygame.K_e]:
            rotateAmt = 5
            self.rotate += -rotateAmt
        
        # Shoot
        if keys[pygame.K_RETURN]:
            self.shoot()
    
    # Create a Bullet sprite
    def shoot(self):
        currentTime = pygame.time.get_ticks()
        if currentTime - self.lastTimeFired > weapons[self.currWeapon]["bulletFireRate"]:
            self.lastTimeFired = currentTime
            dir = vector(1, 0).rotate(-self.rotate)
            position = self.position + bulletOffset.rotate(-self.rotate)
            self.velocity = vector(-weapons[self.currWeapon]["bulletRecoilRate"], 0).rotate(-self.rotate)
            for bullets in range(weapons[self.currWeapon]["bulletCount"]):
                strays = uniform(-weapons[self.currWeapon]["bulletStray"], \
                weapons[self.currWeapon]["bulletStray"])
                Bullet(self.game, position, dir.rotate(strays))
                shotNoise = choice(self.game.currWeaponSounds[self.currWeapon])
                if shotNoise.get_num_channels() > 3:
                    shotNoise.stop()
                shotNoise.play()
            BulletShotFlash(self.game, position)
    
    # Auto-upgrade weapon
    def weaponChange(self):
        if self.game.isFloor1 == True and self.game.isRoom112 == False:
            self.currWeapon = "machinegun"
        if self.game.isRoom112:
            self.currWeapon = "rifle"
            
    def restoreHealth(self, restoreAmt):
        self.health += restoreAmt
        if self.health > playerHealth:
            self.health = playerHealth
            
    def restoreEnergy(self, restoreAmt):
        self.energy += restoreAmt
        if self.energy > playerEnergy:
            self.energy = playerEnergy
            
    def loseEnergy(self):        
        self.energy -= playerEnergyExhaust
        if self.energy < (1/4)*playerEnergy:
            self.energy = (1/4)*playerEnergy
            self.health -= playerEnergyExhaustDamage

    def update(self):
        self.movePlayer()
        self.image = pygame.transform.rotate(self.game.playerImage, self.rotate)
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.position += self.velocity * self.game.sec
        self.collideRect.centerx = self.position.x
        checkWallCollision(self, self.game.walls, 'horizontal')
        self.collideRect.centery = self.position.y
        checkWallCollision(self, self.game.walls, 'vertical')
        checkHolesCollision(self, self.game.holes)
        self.rect.center = self.collideRect.center
    
####    Zombies   ####

# Enemy Type 1: Normal zombie
class Zombie(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = zombieLayer
        self.groups = game.allSpritesGroup, game.zombies
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.zombieImage.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.collideRect = zombieCollideRect.copy()
        self.collideRect.center = self.rect.center
        self.position = vector(x, y)
        self.velocity = vector(0, 0)
        self.acceleration = vector(0, 0)
        self.rect.center = self.position
        self.rotate = 0
        self.health = zombieHealth
        self.speed = choice(zombieSpeeds)
        self.victim = game.player
    
    def zombieGroupDisperse(self):
        for zombie in self.game.zombies:
            if zombie != self:
                dist = self.position - zombie.position
                if 0 < dist.length() < zombieCoverRadii:
                    self.acceleration += dist.normalize()
    
    '''CITATION: Moving enemy towards player idea:
    https://stackoverflow.com/questions/20044791/how-to-make-an-enemy-follow-the-player-in-pygame'''
    def moveToPlayer(self):
        distFromPlayer = self.victim.position - self.position
        if distFromPlayer.length_squared() < zombieDetectPlayerRadii**2:
            if random() < (1/10):
                choice(self.game.zombieSounds).play()
            # Zombies get aggressive when player gets close
            self.rotate = distFromPlayer.angle_to(vector(1, 0))
            self.image = pygame.transform.rotate(self.game.zombieImage, self.rotate)
            self.rect = self.image.get_rect()
            self.rect.center = self.position
            self.acceleration = vector(1, 0).rotate(-self.rotate)
            self.zombieGroupDisperse()
            self.acceleration.scale_to_length(self.speed)
            self.acceleration += -self.velocity
            self.velocity += self.acceleration * self.game.sec
            pos = (self.velocity*self.game.sec) + (0.5*self.acceleration*self.game.sec**2)
            self.position += pos
            self.collideRect.centerx = self.position.x
            checkWallCollision(self, self.game.walls, 'horizontal')
            self.collideRect.centery = self.position.y
            checkWallCollision(self, self.game.walls, 'vertical')
            self.rect.center = self.collideRect.center
            
    def update(self):
        self.moveToPlayer()
        if self.health <= 0:
            choice(self.game.gutsSquishSounds).play()
            self.kill()
            self.game.floorImage.blit(self.game.bloodImage, self.position - vector(32, 32))
            self.game.score += 1
            
    def displayZombieHealth(self):
        if self.health > int(zombieHealth*(2/3)):
            color = green
        elif self.health > int(zombieHealth*(1/3)):
            color = yellow
        else:
            color = red
        width = (self.rect.width * self.health)//zombieHealth
        self.healthBar = pygame.Rect(0, 0, width, 5)
        if self.health < zombieHealth:
            pygame.draw.rect(self.image, color, self.healthBar)

# Enemy Type 2: Stronger and faster zombie for lvl2
class StrongZombie(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = zombieLayer
        self.groups = game.allSpritesGroup, game.zombiesStrong
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.zombieStrongImage.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.collideRect = zombieStrongCollideRect.copy()
        self.collideRect.center = self.rect.center
        self.position = vector(x, y)
        self.velocity = vector(0, 0)
        self.acceleration = vector(0, 0)
        self.rect.center = self.position
        self.rotate = 0
        self.health = zombieStrongHealth
        self.speed = choice(zombieStrongSpeeds)
        self.victim = game.player
        
    def zombieGroupDisperse(self):
        for zombie in self.game.zombiesStrong:
            if zombie != self:
                dist = self.position - zombie.position
                if 0 < dist.length() < zombieStrongCoverRadii:
                    self.acceleration += dist.normalize()
                    
    def moveToPlayer(self):
        distFromPlayer = self.victim.position - self.position
        if distFromPlayer.length_squared() < zombieStrongDetectPlayerRadii**2:
            if random() < 0.01:
                choice(self.game.zombieSounds).play()
            # Zombies get aggressive when player gets close
            self.rotate = distFromPlayer.angle_to(vector(1, 0))
            self.image = pygame.transform.rotate(self.game.zombieStrongImage, self.rotate)
            self.rect = self.image.get_rect()
            self.rect.center = self.position
            self.acceleration = vector(1, 0).rotate(-self.rotate)
            self.zombieGroupDisperse()
            self.acceleration.scale_to_length(self.speed)
            self.acceleration += -self.velocity
            self.velocity += self.acceleration * self.game.sec
            pos = (self.velocity*self.game.sec) + (0.5*self.acceleration*self.game.sec**2)
            self.position += pos
            self.collideRect.centerx = self.position.x
            checkWallCollision(self, self.game.walls, 'horizontal')
            self.collideRect.centery = self.position.y
            checkWallCollision(self, self.game.walls, 'vertical')
            self.rect.center = self.collideRect.center
            
    def update(self):
        self.moveToPlayer()
        if self.health <= 0:
            choice(self.game.gutsSquishSounds).play()
            self.kill()
            self.game.floorImage.blit(self.game.bloodStrImage, self.position - vector(32, 32))
            self.game.score += 5
    
    def displayZombieHealth(self):
        if self.health > int(zombieStrongHealth*(2/3)):
            color = green
        elif self.health > int(zombieStrongHealth*(1/3)):
            color = yellow
        else:
            color = red
        width = (self.rect.width * self.health)//zombieStrongHealth
        self.healthBar = pygame.Rect(0, 0, width, 5)
        if self.health < zombieStrongHealth:
            pygame.draw.rect(self.image, color, self.healthBar)

# Enemy Type 3: Randomly walks up and down to block player
class RandomZombie(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = zombieLayer
        self.groups = game.allSpritesGroup, game.zombiesRandom
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.zombieRandomImage.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.collideRect = zombieCollideRect.copy()
        self.collideRect.center = self.rect.center
        self.endY = y + 200
        self.position = vector(x, y)
        self.velocity = vector(0, 2)
        self.rect.center = self.position
        self.pathY = (y, self.endY)
        self.rotate = 90
        self.health = zombieRandomHealth
        self.speed = choice(zombieSpeeds)
        self.victim = game.player
    
    # Just repeatedly walks up and down a certain dist
    def randomWalkY(self):
        if self.velocity.y > 0:
            if self.position.y + self.velocity.x < self.pathY[1]:
                self.position.y += self.velocity.y
            else:
                self.velocity.y = -self.velocity.y
            self.rotate = -90
        else:
            if self.position.y - self.velocity.x > self.pathY[0]:
                self.position.y += self.velocity.y
            else:
                self.velocity.y = -self.velocity.y
            self.rotate = 90
            
    def update(self):
        distFromPlayer = self.victim.position - self.position
        if distFromPlayer.length_squared() < zombieRandomDetectPlayerRadii**2:
            if random() < 0.01:
                choice(self.game.zombieSounds).play()
        self.image = pygame.transform.rotate(self.game.zombieRandomImage, self.rotate)
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.randomWalkY()
        self.collideRect.centerx = self.position.x
        checkWallCollision(self, self.game.walls, 'horizontal')
        self.collideRect.centery = self.position.y
        checkWallCollision(self, self.game.walls, 'vertical')
        self.rect.center = self.collideRect.center
        if self.health <= 0:
            choice(self.game.gutsSquishSounds).play()
            self.kill()
            self.game.floorImage.blit(self.game.bloodRandImage, self.position - vector(32, 32))
            self.game.score += 2
    
    def displayZombieHealth(self):
        if self.health > int(zombieRandomHealth*(2/3)):
            color = green
        elif self.health > int(zombieRandomHealth*(1/3)):
            color = yellow
        else:
            color = red
        width = (self.rect.width * self.health)//zombieRandomHealth
        self.healthBar = pygame.Rect(0, 0, width, 5)
        if self.health < zombieRandomHealth:
            pygame.draw.rect(self.image, color, self.healthBar)
            
# Enemy Type 4: Boss monster, uses A*pathfinding to find shortest dist to player
class BossZombie(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.x = x
        self.y = y
        self._layer = zombieLayer
        self.groups = game.allSpritesGroup, game.zombieBoss
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.zombieBossImage.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.collideRect = zombieBossCollideRect.copy()
        self.collideRect.center = self.rect.center
        self.position = vector(self.x, self.y)
        self.velocity = vector(0, 0)
        self.acceleration = vector(0, 0)
        self.rect.center = self.position
        self.rotate = 0
        self.health = zombieBossHealth
        self.speed = zombieBossSpeed
        self.victim = game.player
    
    # Use A* path finding to calculate shortest dist to player
    def findPlayer(self, route):
        targetPos = (self.game.player.position.x, self.game.player.position.y)
        bossPos = (self.position.x, self.position.y)
        # If boss hasn't reached player, keep closing in on player
        if bossPos != targetPos:
            direction = route[(self.position.x, self.position.y)]
            # find next in path
            self.position += direction
            self.rotate = direction.angle_to(vector(1, 0))
            self.image = pygame.transform.rotate(self.game.zombieBossImage, \
            self.rotate)
            self.rect = self.image.get_rect()
            self.rect.center = self.position
    
    def moveToPlayer(self):
        distFromPlayer = self.victim.position - self.position
        if distFromPlayer.length_squared() < zombieBossDetectPlayerRadii**2:
            choice(self.game.bossZombieScreams).play()
        self.findPlayer(self.game.route)
        self.collideRect.centerx = self.position.x
        self.collideRect.centery = self.position.y
        self.rect.center = self.collideRect.center
    
    def update(self):
        self.moveToPlayer()
        if self.health <= 0:
            choice(self.game.bossDeathSounds).play()
            self.kill()
            bloodLoc = vector(32, 32)
            self.game.floorImage.blit(self.game.bloodBossImage, \
            self.position-bloodLoc)
            self.game.score += 100
            self.game.lastScreen = True
    
    def displayZombieHealth(self):
        if self.health > int(zombieBossHealth*(2/3)):
            color = green
        elif self.health > int(zombieBossHealth*(1/3)):
            color = yellow
        else:
            color = red
        width = (self.rect.width * self.health)//zombieBossHealth
        self.healthBar = pygame.Rect(0, 0, width, 5)
        if self.health < zombieBossHealth:
            pygame.draw.rect(self.image, color, self.healthBar)

####    Bullet Class   ####
class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, position, dirn):
        self._layer = bulletLayer
        self.groups = game.allSpritesGroup, game.bullets
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bulletImage[weapons[game.player.currWeapon]["bulletSize"]]
        self.rect = self.image.get_rect()
        self.collideRect = self.rect
        self.position = vector(position)
        self.rect.center = position
        self.velocity = dirn * weapons[game.player.currWeapon]["bulletSpeed"]
        self.spawnTime = pygame.time.get_ticks()
        self.rotate = 0
        
    def update(self):
        self.rotate = self.game.player.rotate
        # Diff weapon states
        if weapons[self.game.player.currWeapon]['bulletSize'] == "handgun":
            bulletImg = self.game.bulletImage["handgun"]
            self.image = pygame.transform.rotate(bulletImg, self.rotate)
            self.collideRect = self.image.get_rect()
        if weapons[self.game.player.currWeapon]['bulletSize'] == "machinegun":
            bulletImg = self.game.bulletImage["machinegun"]
            self.image = pygame.transform.rotate(bulletImg, self.rotate)
            self.collideRect = self.image.get_rect()
        if weapons[self.game.player.currWeapon]['bulletSize'] == "rifle":
            bulletImg = self.game.bulletImage["rifle"]
            self.image = pygame.transform.rotate(bulletImg, self.rotate)
            self.collideRect = self.image.get_rect()
        self.position += self.velocity * self.game.sec
        self.rect.center = self.position
        if pygame.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        currTime = pygame.time.get_ticks()
        timeDiff = currTime - self.spawnTime
        if timeDiff > weapons[self.game.player.currWeapon]["bulletLifetime"]:
            self.kill()

class BulletShotFlash(pygame.sprite.Sprite):
    def __init__(self, game, position):
        self._layer = bulletFlashLayer
        self.groups = game.allSpritesGroup
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        size = randint(15, 30)
        self.image = pygame.transform.scale(choice(self.game.bulletFireImgs), \
        (size, size)) 
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.collideRect = self.rect
        self.position = position
        self.rect.center = self.position
        self.timeOfFlash = pygame.time.get_ticks()
        
    def update(self):
        currTime = pygame.time.get_ticks()
        timeFlash = currTime - self.timeOfFlash
        if timeFlash > bulletTimeFlash:
            self.kill()

####    Tiled Wall Objects Class   ####
class BlockObstacles(pygame.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

####    Items Class   ####
class Items(pygame.sprite.Sprite):
    def __init__(self, game, position, itemType):
        self.groups = game.allSpritesGroup, game.items
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.allItemImages[itemType]
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.collideRect = self.rect
        self.itemType = itemType
        self.position = position
        self.rect.center = self.position
        self.pt = pt.linear
        self.dist = 0
        self.dir = 1 
    
    '''CITATION: Pytweening source and instructions: 
    https://github.com/asweigart/pytweening/blob/master/pytweening/__init__.py'''
    def update(self):
        moveDist = jumpAmt * self.pt(0.25)
        self.rect.centery = self.position.y + moveDist * self.dir
        self.dist += jumpSpeed
        if self.dist > jumpAmt:
            self.dist = 0
            self.dir = -self.dir
            self.rect.centerx = self.position.x + moveDist * self.dir
            
####    Stairs Classes   ####
class Stairs(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.allSpritesGroup, game.stairs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.stairsImg
        self.rect = self.image.get_rect()
        self.position = vector(x, y)
        self.rect.center = self.position
        self.collideRect = self.rect
        
class LastStairs(Stairs):
    def __init__(self, game, x, y):
        self.groups = game.allSpritesGroup, game.lastStairs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.stairsLastImg
        self.rect = self.image.get_rect()
        self.position = vector(x, y)
        self.rect.center = self.position
        self.collideRect = self.rect

####    Hole Class   ####
class Hole(pygame.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.holes
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

# Checks for sprite wall/hole/group collisions

''' CITATION: Group collision information inspired by:
https://stackoverflow.com/questions/20658020/various-sprites-collide-using-group-pygame'''

def checkCollisionRect(sprite1, sprite2):
    if sprite1.collideRect.colliderect(sprite2.rect):
        return True
    return False

def checkWallCollision(sprite, spriteGroup, collideAxis):
    if collideAxis == 'horizontal':
        spriteGroupCollide = pygame.sprite.spritecollide(sprite, spriteGroup, \
        False, checkCollisionRect)
        if spriteGroupCollide:
            wallPos = spriteGroupCollide[0]
            if wallPos.rect.centerx > sprite.collideRect.centerx:
                sprite.position.x = wallPos.rect.left - sprite.collideRect.width/2
            if wallPos.rect.centerx < sprite.collideRect.centerx:
                sprite.position.x = wallPos.rect.right + sprite.collideRect.width/2
            sprite.velocity.x = 0
            sprite.collideRect.centerx = sprite.position.x
    if collideAxis == 'vertical':
        spriteGroupCollide = pygame.sprite.spritecollide(sprite, spriteGroup, \
        False, checkCollisionRect)
        if spriteGroupCollide:
            wallPos = spriteGroupCollide[0]
            if wallPos.rect.centery > sprite.collideRect.centery:
                sprite.position.y = wallPos.rect.top - sprite.collideRect.height/2
            if wallPos.rect.centery < sprite.collideRect.centery:
                sprite.position.y = wallPos.rect.bottom + sprite.collideRect.height/2
            sprite.velocity.y = 0
            sprite.collideRect.centery = sprite.position.y

def checkHolesCollision(sprite, spriteGroup):
    spriteGroupCollide = pygame.sprite.spritecollide(sprite, spriteGroup, \
    False, checkCollisionRect)
    if spriteGroupCollide:
        sprite.health -= sprite.health