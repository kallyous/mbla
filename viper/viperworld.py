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

from viper.__init__ import WORLDS, CONF
import threading, os, gzip
from viper.vipermethods import printImg, grid2D, gridToStr
from viper.vipernoise import WhiteNoise, PerlinNoise

WATER_DEEP = 1
WATER_SHALLOW = 2
DIRT = 3
GRASS = 4
DIRT_WALL = 5

class World(threading.Thread):
    def __init__(self, data):
        threading.Thread.__init__(self, name=data['name'])
        self.data = data
    
    def run(self):
        wn = WhiteNoise(32, 32, self.data['id'])
        pn = PerlinNoise(wn, 4)
        self.world_path = u'%s/%s' % (CONF['worlds-path'], self.name)
        if not os.path.isdir(self.world_path): os.makedirs(self.world_path)
        printImg(pn, u'%s/%s.png' % (self.world_path, self.name) ) # debug
        self.CreateTerrain(pn)
        
    
    def CreateTerrain(self, pn):
        w = len(pn)
        h = len(pn[0])
        ground_data = grid2D(w, h, 0)
        wall_data = grid2D(w, h, 0)
        empty_data = grid2D(w, h, 0)
        
        for x in range(w):
            for y in range(h):
                tile_h = pn[x][y]
                if tile_h >= 0.9:
                    tile = DIRT
                    wall_data[x][y] = DIRT_WALL
                if tile_h < 0.9 and tile_h >= 0.5: tile = GRASS
                if tile_h < 0.5 and tile_h >= 0.4: tile = DIRT
                if tile_h < 0.4 and tile_h >= 0.2: tile = WATER_SHALLOW
                if tile_h < 0.2: tile = WATER_DEEP
                ground_data[x][y] = tile
        
        lvl_str = 'Alpha Biome\nNature\n0 0\n'
        
        lvl_str += 'data_map ground\n'
        lvl_str += gridToStr(ground_data)
        
        lvl_str += 'data_map floor\n'
        lvl_str += gridToStr(empty_data)
        
        lvl_str += 'data_map walls\n'
        lvl_str += gridToStr(wall_data)
        
        lvl_str += 'data_map roof\n'
        lvl_str += gridToStr(empty_data)
        
        lvl_str += 'obj_list 0\n'
        lvl_str += 'entity_list 0\n'
        lvl_str += 'effect_list 0'
        
        file_path = u'%s/sector-alpha.dat.gz' % self.world_path
        with gzip.open(file_path, 'wb') as sector_file:
            sector_file.write(lvl_str.encode('utf-8'))