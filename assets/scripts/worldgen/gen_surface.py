""" Copyright 2017 Kallyous Caos Negro
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License. """

from viper.__init__ import CONF
from viper.vipermethods import grid2D

SEA = 0
GRASSLANDS = 1
FOREST = 2
DESERT = 3

EMPTY = 0
DEEP_WATER = 1
SHALLOW_WATER = 2
SAND = 3
DIRT = 4
GRASS = 5
STONE = 6
SNOW = 7
LAVA = 8
OIL = 9
HOLE = 10

WALL_DIRT = 1

def GenerateTerrain(topography, biome):
    sect_width = len(topography)
    sect_height = len(topography[0])
    
    ground_map = grid2D(sect_width, sect_height, 0)
    floor_map = grid2D(sect_width, sect_height, 0)
    wall_map = grid2D(sect_width, sect_height, 0)
    roof_map = grid2D(sect_width, sect_height, 0)
    
    for x in range(sect_width):
        for y in range(sect_height):
            sum = topography[x][y]
    
    avrg = sum / sect_width*sect_height
    
    # Biome Rule: If average height of sector is below 151, the biome is set to 'Sea'
    # Otherwise, get one of 4 different biomes base of stuff
    if avrg < 151: biome = SEA
    else: biome = (biome//64)
    if biome == 4: biome = GRASSLANDS
    
    for x in range(sect_width):
        for y in range(sect_height):
            ground_map[x][y] = groundRule(topography[x][y], biome)
            floor_map[x][y] = floorRule(topography[x][y], biome)
            wall_map[x][y] = wallRule(topography[x][y], biome)
            roof_map[x][y] = roofRule(topography[x][y], biome)
    
    data = {'biome':biome, 'ground':ground_map, 'floor':floor_map, 'walls':wall_map, 'roof':roof_map, 'objects':[], 'entities':[], 'owner':'Nature'}
    
    return data


def groundRule(tile, biome):
    if biome == SEA:
        if tile < 231: return DEEP_WATER
        if tile < 251: return SHALLOW_WATER
        if tile < 256: return SAND
    if biome == GRASSLANDS:
        if tile < 11: return DEEP_WATER
        if tile < 61: return SHALLOW_WATER
        if tile < 231: return GRASS
        if tile < 256: return DIRT
    if biome == FOREST:
        if tile < 21: return DEEP_WATER
        if tile < 81: return SHALLOW_WATER
        if tile < 91: return GRASS # TODO: supposed to be mud, but we do not have graphical assets for that.
        if tile < 200: return GRASS
        if tile < 256: return DIRT
    if biome == DESERT:
        if tile < 6: return SHALLOW_WATER
        if tile < 7: return GRASS # TODO: supposed to be a sandy grass, but we do not have graphical assets for that.
        if tile < 231: return SAND
        if tile < 256: return STONE # TODO: supposed to be sandstone...  


def floorRule(tile, biome):
    return EMPTY


def wallRule(tile, biome):
    if biome == SEA: return EMPTY
    if biome == GRASSLANDS:
        if tile > 230: return WALL_DIRT
    if biome == FOREST:
        if tile > 200: return WALL_DIRT
    if biome == DESERT:
            if tile > 240: return WALL_DIRT # TODO: Suposed to be sandstone wall...
    return EMPTY


def roofRule(tile, biome):
    return EMPTY




 