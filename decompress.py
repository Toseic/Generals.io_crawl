import urllib.request
import json
import traceback
import xml.etree.ElementTree as ET
import lzstring
import urllib.request

id = "S5v8wi0l9"
# id = "S9IuRURPK"

class NeutralTile:
    def __init__(self, position, strength):
        self.pos = position
        self.strength = strength

class City:
    def __init__(self, position, strength):
        self.pos = position
        self.strength = strength

class ChatMessage:
    def __init__(self, arr):
        self.text = arr[0]
        self.prefix = arr[1]
        self.playerIndex = arr[2]
        self.turn = arr[3]

class AFKEvent:
    def __init__(self, arr):
        self.playerIndex = arr[0]
        self.turn = arr[1]

class Position:
    def __init__(self, idx, width):
        self.row = idx // width
        self.col = idx % width

class Move:
    def __init__(self, arr, width):
        self.playerIndex = arr[0]
        self.start = Position(arr[1], width)
        self.end = Position(arr[2], width)
        self.isSplit = (arr[3] == 1)
        self.turn = arr[4]

class Map:
    def __init__(self, width, height, cities, cityArmies, generals, mountains, neutralArmyPositions, neutralArmyStrengths, swamps, lightBlocks):
        self.width = width
        self.height = height
        self.cities = [City(Position(cities[i], width), cityArmies[i]) for i in range(len(cities))]
        self.generals = [Position(x, width) for x in generals]
        self.mountains = [Position(x, width) for x in mountains]
        if neutralArmyPositions != None:
            self.neutralTiles = [NeutralTile(Position(neutralArmyPositions[i], width), neutralArmyStrengths[i]) for i in range(len(neutralArmyPositions))]
        if swamps != None:
            self.swamps = [Position(x, width) for x in swamps]
        if lightBlocks != None:
            self.lightBlocks = [Position(x, width) for x in lightBlocks]

    def inbounds(self, pos):
        return pos.row < self.height and pos.col < self.width and pos.row >= 0 and pos.col >= 0

urllib.request.urlretrieve(f"https://generalsio-replays-na.s3.amazonaws.com/{id}.gior", f"{id}.gior")
lz = lzstring.LZString()
with open(f"./{id}.gior", mode="rb") as compressed_rep:
    compressed_arr = compressed_rep.read()
    compressed_str = ""
    for i in range(int(len(compressed_arr) / 2)):
        compressed_str += chr(compressed_arr[2 * i] * 256 + compressed_arr[2 * i + 1])
    rep = json.loads(lz.decompress(compressed_str))
    print(rep)
    version = rep[0]
    id = rep[1]
    mapWidth = rep[2]
    mapHeight = rep[3]
    usernames = rep[4]
    stars = rep[5]
    cities = rep[6]
    cityArmies = rep[7]
    generals = rep[8]
    mountains = rep[9]
    moves = rep[10]
    afks = rep[11]
    teams = rep[12] if len(rep) > 12 else None
    map_title = rep[13] if len(rep) > 13 else None
    neutralArmyPositions = rep[14] if len(rep) > 14 else None
    neutralArmyStrengths = rep[15] if len(rep) > 15 else None
    swamps = rep[16] if len(rep) > 16 else None
    chat = rep[17] if len(rep) > 17 else None
    playerColors = rep[18] if len(rep) > 18 else None
    lightBlocks = rep[19] if len(rep) > 19 else None
    gameSettings = rep[20] if len(rep) > 20 else None
    cur_map = Map(mapWidth, mapHeight, cities, cityArmies, generals, mountains, neutralArmyPositions, neutralArmyStrengths, swamps, lightBlocks)
    move_list = [Move(x, mapWidth) for x in moves]
    chat_list = [ChatMessage(x) for x in chat] if chat != None else None
    afk_events = [AFKEvent(x) for x in afks]