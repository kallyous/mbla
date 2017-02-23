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

import builtins, threading, gzip, os, time
from viper.viperconf import *
from viper.vipernoise import *

WATER_DEEP = 1
WATER_SHALLOW = 2
DIRT = 3
GRASS = 4
DIRT_WALL = 5


class Master(threading.Thread):
	def __init__(self, wid):
		threading.Thread.__init__(self, name='%s Master' % builtins.WORLDS[wid]['name'])
		self.wid = wid
		builtins.WORLDS[wid]['path'] = u'%s/%s' % (builtins.CONF['worlds_path'], wid)
		if not os.path.isdir(builtins.WORLDS[wid]['path']): os.makedirs(builtins.WORLDS[wid]['path'])
	
	def run(self):
		last_time = time.time()
		self.RaiseLords()
		self.LaunchLords()
		while True:
			if (time.time() - last_time) > 30: self.SaveLands()
			time.sleep(1)
			last_time = time.time()
	
	def RaiseLords(self):
		self.Lords = {}
		self.Lords['Designer'] = Designer(self.wid)
		self.Lords['Gaia'] = Gaia(self.wid)
		self.Lords['Ego'] = Ego(self.wid)
		self.Lords['Director'] = Director(self.wid)
		self.Lords['Arbiter'] = Arbiter(self.wid)
		self.Lords['Artificer'] = Artificer(self.wid)
		self.Lords['Herald'] = Herald(self.wid)
	
	def LaunchLords(self):
		for lord in self.Lords:
			self.Lords[lord].start()
	
	def SaveLands(self):
		for level in builtins.WORLDS[self.wid]['levels']:
				for sector in level:
					self.saveSector(level, sector)
	
	def saveSector(self, level, sector):
		print('Save sector called.')


class Designer(threading.Thread):
	def __init__(self, wid):
		threading.Thread.__init__(self, name='%s Designer' % builtins.WORLDS[wid]['name'])
		self.wid = wid
	
	# Builds world data and meta for first run
	def CreateWorld(self):
		for level in range(builtins.WORLDS[self.wid]['levels']):
			lvl_path = u'%s/%d' % (builtins.WORLDS[self.wid]['path'], level)
			if not os.path.isdir(lvl_path): os.makedirs(lvl_path)
			self.CreateLevel(level)
	
	def CreateLevel(self, level):
		# Name stuff
		lvl_path = u'%s/%d' % (builtins.WORLDS[self.wid]['path'], level)
		lvl_topography = u'%s/topography.dat' % lvl_path
		
		# Stuff already there?
		if not os.path.isdir(lvl_path): os.makedirs(lvl_path)
		if os.path.isfile(lvl_topography):
			print(u'%s #%d already exists, skipping.' % (builtins.WORLDS[self.wid]['name'], level) )
			return
		else: print(u'Creating %s #%d...' % (builtins.WORLDS[self.wid]['name'], level) )
		
		# Gather info
		width = builtins.CONF['sector_width'] * builtins.WORLDS[self.wid]['xSec']
		height = builtins.CONF['sector_height'] * builtins.WORLDS[self.wid]['ySec']
		seed = builtins.WORLDS[self.wid]['noise']['seed'] + level
		octaves = builtins.WORLDS[self.wid]['noise']['oct']
		amp = builtins.WORLDS[self.wid]['noise']['amp']
		pers = builtins.WORLDS[self.wid]['noise']['pers']
		
		# Generate biomes for all sectors
		bm_wn = WhiteNoise(builtins.WORLDS[self.wid]['xSec'], builtins.WORLDS[self.wid]['ySec'], seed)
		bm_pn = PerlinNoise(bm_wn, octaves, amplitude=amp, persistance=pers)
		
		# Generate topogrpahy for all tiles
		tp_wn = WhiteNoise(width, height, seed)
		tp_pn = PerlinNoise(tp_wn, octaves, amplitude=amp, persistance=pers)
		
		# debug
		printImg(tp_pn,'%s/ground.png' % lvl_path )
		printImg(bm_pn,'%s/biomes.png' % lvl_path )
		
		# Test topography generation
		lvl_meta = {}
		lvl_meta['seed'] = seed
		lvl_meta['sect_width'] = builtins.CONF['sector_width']
		lvl_meta['sect_height'] = builtins.CONF['sector_height']
		GenerateTopography(lvl_meta, tp_pn, bm_pn, lvl_topography)
		TestTopographyFile(lvl_topography)
	
	def run(self):
		self.CreateWorld()
	
	def GenerateSector(self):
		pass


class Gaia(threading.Thread):
	def __init__(self, wid):
		threading.Thread.__init__(self, name='%s Gaia' % builtins.WORLDS[wid]['name'])
		self.wid = wid
	def run(self):
		pass


class Ego(threading.Thread):
	def __init__(self, wid):
		threading.Thread.__init__(self, name='%s Ego' % builtins.WORLDS[wid]['name'])
		self.wid = wid
	def run(self):
		pass


class Director(threading.Thread):
	def __init__(self, wid):
		threading.Thread.__init__(self, name='%s Director' % builtins.WORLDS[wid]['name'])
		self.wid = wid
	def run(self):
		pass


class Arbiter(threading.Thread):
	def __init__(self, wid):
		threading.Thread.__init__(self, name='%s Arbiter' % builtins.WORLDS[wid]['name'])
		self.wid = wid
	def run(self):
		pass


class Artificer(threading.Thread):
	def __init__(self, wid):
		threading.Thread.__init__(self, name='%s Artificer' % builtins.WORLDS[wid]['name'])
		self.wid = wid
	def run(self):
		pass


class Herald(threading.Thread):
	def __init__(self, wid):
		threading.Thread.__init__(self, name='%s Herald' % builtins.WORLDS[wid]['name'])
		self.wid = wid
	def run(self):
		pass


class World(threading.Thread):
	def __init__(self, data):
		threading.Thread.__init__(self, name=data['name'])
		self.data = data
	
	def run(self):
		wn = WhiteNoise(32, 32, self.data['id'])
		pn = PerlinNoise(wn, 4)
		self.world_path = u'%s/%s' % (builtins.CONF['worlds-path'], self.name)
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


















