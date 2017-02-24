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

import threading, os, time
from viper.__init__ import WORLDS, CONF
from viper.vipercartography import LandLevel
from viper.vipernoise import WhiteNoise, PerlinNoise
from viper.vipermethods import printImg, GenerateTopography, TestTopographyFile

LEVELS = []

class Master(threading.Thread):
	def __init__(self, wid):
		threading.Thread.__init__(self, name='%s Master' % WORLDS[wid]['name'])
		self.wid = wid
		WORLDS[wid]['path'] = u'%s/%s' % (CONF['worlds_path'], wid)
		if not os.path.isdir(WORLDS[wid]['path']): os.makedirs(WORLDS[wid]['path'])
	
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
		for level in WORLDS[self.wid]['levels']:
				for sector in level:
					self.saveSector(level, sector)
	
	def saveSector(self, level, sector):
		print('Save sector called.')


class Designer(threading.Thread):
	def __init__(self, wid):
		threading.Thread.__init__(self, name='%s Designer' % WORLDS[wid]['name'])
		self.wid = wid
	
	def run(self):
		self.CreateWorld()
		
	
	def CreateWorld(self):
		for level in range(WORLDS[self.wid]['levels']):
			lvl_path = u'%s/%d' % (WORLDS[self.wid]['path'], level)
			if not os.path.isdir(lvl_path): os.makedirs(lvl_path)
			if not self.levelExists(lvl_path): self.CreateLevel(level)
	
	def levelExists(self, lvl_path):
		if not os.path.isdir(lvl_path): return False
		if not os.path.isfile('%s/level-meta.dat' % lvl_path): return False
		if not os.path.isfile('%s/level-0-0.gz' % lvl_path): return False
		return True
	
	def CreateLevel(self, level):
		# Name things
		lvl_path = u'%s/%d' % (WORLDS[self.wid]['path'], level)
		lvl_topography = u'%s/level-meta.dat' % lvl_path
		# Stuff already there?
		if not os.path.isdir(lvl_path): os.makedirs(lvl_path)
		if os.path.isfile(lvl_topography):
			print(u'%s #%d already exists, skipping.' % (WORLDS[self.wid]['name'], level) )
			return
		else: print(u'Creating %s #%d...' % (WORLDS[self.wid]['name'], level) )
		# Gather info
		width = CONF['sec_w'] * WORLDS[self.wid]['xSec']
		height = CONF['sec_h'] * WORLDS[self.wid]['ySec']
		seed = WORLDS[self.wid]['noise']['seed'] + level
		octaves = WORLDS[self.wid]['noise']['oct']
		amp = WORLDS[self.wid]['noise']['amp']
		pers = WORLDS[self.wid]['noise']['pers']
		# Generate biomes for all sectors
		bm_wn = WhiteNoise(WORLDS[self.wid]['xSec'], WORLDS[self.wid]['ySec'], seed)
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
		lvl_meta['sect_width'] = CONF['sec_w']
		lvl_meta['sect_height'] = CONF['sec_h']
		GenerateTopography(lvl_meta, tp_pn, bm_pn, lvl_topography)
		TestTopographyFile(lvl_topography)
		# Put result in a visible place
		LEVELS.append( LandLevel( self.wid, level ) )
		# Generate the sector 0 0
		self.GenerateSector(level, 0, 0)
	
	def GenerateSector(self, level, xSect, ySect):
		LEVELS[level].newSector(xSect, ySect)
		


class Gaia(threading.Thread):
	def __init__(self, wid):
		threading.Thread.__init__(self, name='%s Gaia' % WORLDS[wid]['name'])
		self.wid = wid
	def run(self):
		pass


class Ego(threading.Thread):
	def __init__(self, wid):
		threading.Thread.__init__(self, name='%s Ego' % WORLDS[wid]['name'])
		self.wid = wid
	def run(self):
		pass


class Director(threading.Thread):
	def __init__(self, wid):
		threading.Thread.__init__(self, name='%s Director' % WORLDS[wid]['name'])
		self.wid = wid
	def run(self):
		pass


class Arbiter(threading.Thread):
	def __init__(self, wid):
		threading.Thread.__init__(self, name='%s Arbiter' % WORLDS[wid]['name'])
		self.wid = wid
	def run(self):
		pass


class Artificer(threading.Thread):
	def __init__(self, wid):
		threading.Thread.__init__(self, name='%s Artificer' % WORLDS[wid]['name'])
		self.wid = wid
	def run(self):
		pass


class Herald(threading.Thread):
	def __init__(self, wid):
		threading.Thread.__init__(self, name='%s Herald' % WORLDS[wid]['name'])
		self.wid = wid
	def run(self):
		pass





















