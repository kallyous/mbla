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

import threading, os, time, socket, queue, viper
from viper.vipercartography import LandLevel
from viper.vipernoise import WhiteNoise, PerlinNoise
from viper.vipermethods import GenerateTopography
if viper.DEBUG == True:
	from viper.viperdebug import printImg, GenerateTopography, TestTopographyFile


class Master(threading.Thread):
	def __init__(self, wid):
		threading.Thread.__init__(self, name='%s Master' % viper.WORLDS[wid]['name'])
		self.wid = wid
		viper.WORLDS[self.wid]['path'] = u'%s/%s' % (viper.CONF['worlds_path'], wid)
		if not os.path.isdir(viper.WORLDS[wid]['path']): os.makedirs(viper.WORLDS[wid]['path'])
		# Each player entry shall be its username
		# A player is a common entity, like any NPC and is treated with the same mechanics.
		# Only difference is when a player take action, the director apply it to the
		# entity with the player's username on the players dictionary.
		viper.WORLDS[self.wid]['players'] = {}
		viper.WORLDS[self.wid]['lock-players'] = False
		viper.WORLDS[self.wid]['lock-objects'] = False
		viper.WORLDS[self.wid]['lock-entities'] = False
		
	
	def run(self):
		self.RaiseLords()
		self.LaunchLords()
		while True:
			# Check for user connection
			time.sleep(5)
	
	def RaiseLords(self):
		viper.WORLDS[self.wid]['lords'] = {}
		viper.WORLDS[self.wid]['lords']['Designer'] = Designer(self.wid)
		viper.WORLDS[self.wid]['lords']['Courier'] = Courier(self.wid)
		viper.WORLDS[self.wid]['lords']['Gaia'] = Gaia(self.wid)
		viper.WORLDS[self.wid]['lords']['Ego'] = Ego(self.wid)
		viper.WORLDS[self.wid]['lords']['Director'] = Director(self.wid)
		viper.WORLDS[self.wid]['lords']['Arbiter'] = Arbiter(self.wid)
		viper.WORLDS[self.wid]['lords']['Artificer'] = Artificer(self.wid)
		viper.WORLDS[self.wid]['lords']['Herald'] = Herald(self.wid)
	
	def LaunchLords(self):
		for lord in viper.WORLDS[self.wid]['lords']:
			viper.WORLDS[self.wid]['lords'][lord].start()
	
	def addPlayer(self, player):
		# Tells that is about to write into players data, so everybody should wait
		viper.WORLDS[self.wid]['lock-players'] = True
		# Waits until anybody reading players data finishes it's reading
		while playerDataInUse(self.wid): time.sleep(1)
		# Writes to players data
		viper.WORLDS[self.wid]['players'][player['name']] = player
		# Unlocks players data
		viper.WORLDS[self.wid]['lock-players'] = False
		# Debug output
		print(u'%s added to [players]:' % self.name)
		print(viper.WORLDS[self.wid]['players'][player['name']])


# Crafts what is to be seem
class Artificer(threading.Thread):
	def __init__(self, wid):
		threading.Thread.__init__(self, name='%s Artificer' % viper.WORLDS[wid]['name'])
		self.wid = wid
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.setblocking(False)
		self.readingFromPlayers = False
		self.readingEntities = False
		self.readingObjects = False
		
	def run(self):
		while True:
			# Check if players data is locked
			if not viper.WORLDS[self.wid]['lock-players']:
				# Lets other sknow that players data is being read
				self.readingFromPlayers = True
				# Copy from players data for processing
				players_data = viper.WORLDS[self.wid]['players']
				# Uses the data
				for player in players_data:
					world = viper.WORLDS[self.wid]['name']
					level = players_data[player]['wlvl']
					x = players_data[player]['x']
					y = players_data[player]['y']
					z = players_data[player]['z']
					addr = players_data[player]['addr']
					port = players_data[player]['graphics-port']
					msg = u'You are in the %s #%d at x:%d y:%d z:%d ' % (world, level, x, y, z)
					try: self.sock.sendto(msg.encode('utf-8'), (addr,port) )
					except: print(u'%s output error.' % self.name)
				# Releases players data for writing after copying it's contents
				self.readingFromPlayers = False
			time.sleep(1)


# Receives players input and stores them on public location
class Courier(threading.Thread):
	def __init__(self, wid):
		threading.Thread.__init__(self, name='%s Courier' % viper.WORLDS[wid]['name'])
		self.wid = wid
		viper.WORLDS[self.wid]['input-pool'] = queue.Queue()
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.setblocking(False)
		self.sock.bind( (viper.SERVER_ADDR, viper.WORLDS[self.wid]['listen-port']) )
		self.readingFromPlayers = False
		self.readingEntities = False
		self.readingObjects = False
		
	def run(self):
		while True:
			try: (data, addr) = self.sock.recvfrom(viper.BUFSIZE)
			except BlockingIOError: pass
			else:
				viper.WORLDS[self.wid]['input-pool'].put(data.decode('utf-8'))
			time.sleep(1)


# Sends the words
class Herald(threading.Thread):
	def __init__(self, wid):
		threading.Thread.__init__(self, name='%s Herald' % viper.WORLDS[wid]['name'])
		self.wid = wid
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.setblocking(True)
		self.readingFromPlayers = False
		self.readingEntities = False
		self.readingObjects = False
	
	def run(self):
		while True:
			# Check if players data is unlocked
			if not viper.WORLDS[self.wid]['lock-players']:
				# Let others know that Heral is reading from it
				self.readingFromPlayers = True
				# Copy players data content
				players_data = viper.WORLDS[self.wid]['players']
				# Releases players data for reading
				self.readingFromPlayers = False
				# Uses data
				for player in players_data:
					addr = players_data[player]['addr']
					port = players_data[player]['data-port']
					msg = u'Hello %s, nice to have you here at the MBLA construction.' % player
					try: self.sock.sendto(msg.encode('utf-8'), (addr,port) )
					except: print(u'%s output error.' % self.name)
				viper.HERALD_BUSY = False
		time.sleep(1)


# Heals, grows, spawns
class Gaia(threading.Thread):
	def __init__(self, wid):
		threading.Thread.__init__(self, name='%s Gaia' % viper.WORLDS[wid]['name'])
		self.wid = wid
		self.readingFromPlayers = False
		self.readingEntities = False
		self.readingObjects = False
	
	def run(self):
		pass


# Thinks
class Ego(threading.Thread):
	def __init__(self, wid):
		threading.Thread.__init__(self, name='%s Ego' % viper.WORLDS[wid]['name'])
		self.wid = wid
		self.readingFromPlayers = False
		self.readingEntities = False
		self.readingObjects = False
	
	def run(self):
		pass


# Directs the action
class Director(threading.Thread):
	def __init__(self, wid):
		threading.Thread.__init__(self, name='%s Director' % viper.WORLDS[wid]['name'])
		self.wid = wid
		self.readingFromPlayers = False
		self.readingEntities = False
		self.readingObjects = False
	
	def run(self):
		while True:
			try: player_action = viper.WORLDS[self.wid]['input-pool'].get()
			except queue.Empty: pass
			else: print(u'%s poped action: %s' % (self.name, player_action) )
			time.sleep(1)


# Makes things fair
class Arbiter(threading.Thread):
	def __init__(self, wid):
		threading.Thread.__init__(self, name='%s Arbiter' % viper.WORLDS[wid]['name'])
		self.wid = wid
		self.readingFromPlayers = False
		self.readingEntities = False
		self.readingObjects = False
	
	def run(self):
		pass


class Designer(threading.Thread):
	def __init__(self, wid):
		threading.Thread.__init__(self, name='%s Designer' % viper.WORLDS[wid]['name'])
		self.wid = wid
		viper.WORLDS[self.wid]['levels'] = []
		self.readingFromPlayers = False
		self.readingEntities = False
		self.readingObjects = False
		
	
	def run(self):
		self.CreateWorld()
		for i in range(viper.WORLDS[self.wid]['level-count']):
			if not viper.WORLDS[self.wid]['levels'][i].loadSector(0,0):
				viper.WORLDS[self.wid]['levels'][i].newSector(0,0)
	
	def CreateWorld(self):
		for level in range(viper.WORLDS[self.wid]['level-count']):
			if self.levelExists(level):
				print('%s loading level %d...' % (self.name, level) )
				self.LoadLevel(level)
			else:
				print('%s creating level %d...' % (self.name, level) )
				self.CreateLevel(level)
	
	def levelExists(self, level):
		lvl_meta = u'%s/%d/level-meta.dat' % (viper.WORLDS[self.wid]['path'], level)
		if os.path.isfile(lvl_meta): return True
		else: return False
	
	def LoadLevel(self, level):
		lvl_path = u'%s/%d' % (viper.WORLDS[self.wid]['path'], level)
		lvl_topography = u'%s/level-meta.dat' % lvl_path
		if os.path.isfile(lvl_topography):
			viper.WORLDS[self.wid]['levels'].append( LandLevel(self.wid, level) )
		else:
			print('CRITICAL: %s does not exists!!!' % lvl_topography)
	
	def CreateLevel(self, level):
		# Name things
		lvl_path = u'%s/%d' % (viper.WORLDS[self.wid]['path'], level)
		lvl_topography = u'%s/level-meta.dat' % lvl_path
		# Stuff already there?
		if not os.path.isdir(lvl_path): os.makedirs(lvl_path)
		if os.path.isfile(lvl_topography):
			print(u'%s #%d already exists, skipping.' % (viper.WORLDS[self.wid]['name'], level) )
			return
		else: print(u'Creating %s #%d...' % (viper.WORLDS[self.wid]['name'], level) )
		# Gather info
		width = viper.CONF['sec_w'] * viper.WORLDS[self.wid]['xSec']
		height = viper.CONF['sec_h'] * viper.WORLDS[self.wid]['ySec']
		seed = viper.WORLDS[self.wid]['noise']['seed'] + level
		octaves = viper.WORLDS[self.wid]['noise']['oct']
		amp = viper.WORLDS[self.wid]['noise']['amp']
		pers = viper.WORLDS[self.wid]['noise']['pers']
		# Generate biomes for all sectors
		bm_wn = WhiteNoise(viper.WORLDS[self.wid]['xSec'], viper.WORLDS[self.wid]['ySec'], seed)
		bm_pn = PerlinNoise(bm_wn, octaves, amplitude=amp, persistance=pers)
		# Generate topogrpahy for all tiles
		tp_wn = WhiteNoise(width, height, seed)
		tp_pn = PerlinNoise(tp_wn, octaves, amplitude=amp, persistance=pers)
		# Generate topography
		lvl_meta = {}
		lvl_meta['seed'] = seed
		lvl_meta['sect_width'] = viper.CONF['sec_w']
		lvl_meta['sect_height'] = viper.CONF['sec_h']
		GenerateTopography(lvl_meta, tp_pn, bm_pn, lvl_topography)
		# Debug
		if viper.DEBUG:
			printImg(tp_pn,'%s/ground.png' % lvl_path )
			printImg(bm_pn,'%s/biomes.png' % lvl_path )
			TestTopographyFile(lvl_topography)
		# Put result in a visible place
		viper.WORLDS[self.wid]['levels'].append( LandLevel( self.wid, level ) )
	
	def GenerateSector(self, level, xSect, ySect):
		viper.WORLDS[self.wid]['levels'][level].newSector(xSect, ySect)


def playerDataInUse(wid):
	for lord in viper.WORLDS[wid]['lords']:
		if viper.WORLDS[wid]['lords'][lord].readingFromPlayers: return True
	return False

def entityDataInUse(wid):
	for lord in viper.WORLDS[wid]['lords']:
		if viper.WORLDS[wid]['lords'][lord].readingEntities: return True
	return False

def objectDataInUse(wid):
	for lord in viper.WORLDS[wid]['lords']:
		if viper.WORLDS[wid]['lords'][lord].readingFromObjects: return True
	return False
















