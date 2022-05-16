# Import modules
import pygame
import math
from Constants import *
import pytmx
from collections import deque
import heapq
vector = pygame.math.Vector2

# _____          _____
#   |   | |     |
#   |   | |     |___
#   |   | |     |
#   |   | |____ |_____

# Classes that deal with the map layout

'''CITATION: sprite sheets/map layout adapted and inspired from: 
            https://www.kenney.nl/assets/topdown-shooter
            Pixel style inspired by:
            https://itch.io/game-assets'''

# All possible travel directions on map
adjacentDirections = [vector(1, 0), 
                      vector(-1, 0), 
                      vector(0, 1), 
                      vector(0, -1),
                      vector(1, 1), 
                      vector(-1, 1), 
                      vector(1, -1), 
                      vector(-1, -1)]

# Side scrolling
class ScreenScroll:
    def __init__(self, screenWidth, screenHeight):
        self.screenScroll = pygame.Rect(0, 0, screenWidth, screenHeight)
        self.windowWidth = screenWidth
        self.windowHeight = screenHeight

    def moveWindow(self, player):
        return player.rect.move(self.screenScroll.topleft)
        
    def moveWindowRect(self, rect):
        return rect.move(self.screenScroll.topleft)

    def update(self, player):
        x = -player.rect.centerx + int(screenWidth / 2)
        y = -player.rect.centery + int(screenHeight / 2)

        # Limit scrolling to map size
        x = min(0, x)  # left stop
        x = max(-(self.windowWidth - screenWidth), x)  # right stop
        y = min(0, y)  # top stop
        y = max(-(self.windowHeight - screenHeight), y)  # bottom stop
        self.screenScroll = pygame.Rect(x, y, self.windowWidth, self.windowHeight)

class DefaultGrid:
    def __init__(self):
        self.tilescreenWidth = screenWidth
        self.tilescreenHeight = screenHeight
        self.screenWidth = self.tilescreenWidth * tileSize
        self.screenHeight = self.tilescreenHeight * tileSize

'''CITATION: Tile Instructions and Layout inspiration taken from 
https://qq.readthedocs.io/en/latest/tiles.html'''
class TileMap:
    def __init__(self, filename):
        self.filename = filename
        loadTileMap = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = loadTileMap.width * loadTileMap.tilewidth
        self.height = loadTileMap.height * loadTileMap.tileheight
        self.TileMapData = loadTileMap
        self.costScale = 10
        self.weights = {}
        self.walls = []
        self.getRoomWallCoords()
    
    # Make sure route is not a wall
    def checkCollisionState(self, tile):
        if 0 <= tile.x < self.width and \
        0 <= tile.y < self.height and \
        tile not in self.walls:
            return True
        return False
    
    # Fine shortest adjacent tile dist
    def tileToTileDist(self, targetObj, currObj):
        currObjPos = vector(currObj)
        targetObjPos = vector(targetObj)
        # Get magnitude of moving vertical/horizontal
        if (currObjPos - targetObjPos).length_squared() == 1:
            adjacentCost = 1
            return self.weights.get(currObj, 0) + adjacentCost * self.costScale
        # Get magnitude of moving diagonally
        else:
            diagonalCost = math.sqrt(2)
            return self.weights.get(currObj, 0) + int(diagonalCost * self.costScale)
    
    # Fill walls lst with wall coordinates
    def getRoomWallCoords(self):
        if self.filename == "room112.tmx":
            for obj in self.TileMapData.objects:
                if obj.name == "Wall":
                    self.walls.append(vector(obj.x, obj.y))
    
    # Get all feasible routeDicts 
    def checkAdjacentTile(self, tile):
        adjTile = [tile + direction for direction in adjacentDirections]
        adjTile = filter(self.checkCollisionState, adjTile)
        return adjTile
    
    # Draw the tile layers on the surface
    def render(self, canvas):
        #Get the tile map global Ids
        tileIDs = self.TileMapData.get_tile_image_by_gid
        for layer in self.TileMapData.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tileSurf = tileIDs(gid)
                    if tileSurf:
                        canvas.blit(tileSurf, (x * self.TileMapData.tilewidth,
                                    y * self.TileMapData.tileheight)) 
    
    def generateTileMap(self):
        mapLayout = pygame.Surface((self.width, self.height))
        self.render(mapLayout)
        return mapLayout
    
# Use heap queue to get best route to coordinate position
class HeapQueue:
    def __init__(self):
        self.tiles = []

    # Use heap queue to analyze price of traveling tile distance
    def orderHeapQ(self, tile, tileToTileDist):
        # Find the least distance tile 
        heapLst = self.tiles
        # Insert best tile into go-to tiles lst
        heapq.heappush(self.tiles, (tileToTileDist, tile))
    
    def currentTile(self):
        tile = heapq.heappop(self.tiles)
        return tile[1]

# Estimate distance from current to target position
def heuristics(current, target):
    costScale = 10
    xDist = abs(current.x - target.x)
    yDist = abs(current.y - target.y)
    manhattanDistance = (xDist + yDist) * costScale
    return manhattanDistance
    
''' CITATION: Pathfinding algorithm Modified and Inspired by: 
    (i) https://github.com/Mekire/find-a-way-astar-pathfinding/blob/master/solver.py
    (ii) https://github.com/kidscancode/pygame_tutorials/blob/master/examples/pathfinding/part5.py'''
# Finds the shortest and fastest route to target from current coordinates
def AStarSearchAlgorithm(TileMap, targetObj, currObj):
    endPos = currObj
    openLst = HeapQueue()
    targetObjCoords = (int(targetObj.x), int(targetObj.y))
    openLst.orderHeapQ(targetObjCoords, 0)
    routeDict = {}
    priorityTravelDict = {}
    routeDict[targetObjCoords] = None
    priorityTravelDict[targetObjCoords] = 0
    
    # While the map has not been explored and player not found
    while len(openLst.tiles) != 0:
        currPos = openLst.currentTile()
        if currPos != endPos:
            # Check the next position in map
            for nextPos in TileMap.checkAdjacentTile(vector(currPos)):
                nextPos = (int(nextPos.x), int(nextPos.y))
                nextPosTile = priorityTravelDict[currPos] + TileMap.tileToTileDist(currPos, nextPos)
                # Check if next position exists and traveling to it is still valid
                if nextPos not in priorityTravelDict or nextPosTile < priorityTravelDict[nextPos]:
                    priorityTravelDict[nextPos] = nextPosTile
                    # Prioritize shortest estimated distance
                    prioritySearch = nextPosTile + heuristics(currObj, vector(nextPos))
                    openLst.orderHeapQ(nextPos, prioritySearch)
                    routeDict[nextPos] = vector(currPos) - vector(nextPos)
        else:
            break
    route = (routeDict, priorityTravelDict)
    return route

# Returns the dictionary of the route from current pos to target pos
def AStarRoute(TileMap, targetObj, currObj):
    route = AStarSearchAlgorithm(TileMap, targetObj, currObj)
    return route[0]
