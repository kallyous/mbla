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

import sys, sqlite3, viper
from pprint import pprint
if viper.DEBUG: from viper.viperdebug import *


def treatData(data):
	try: val = int(data)
	except: pass
	else: return val
	try: val = float(data)
	except: pass
	else: return val
	try: val = data.lower().strip()
	except: pass
	else:
		if val == 'true': return True
		if val == 'false': return False
	return data


def bubbleSort(data, val):
	for i in range(len(data)-1):
		if data[i][val] > data[i+1][val]:
			temp = data[i+1]
			data[i+1] = data[i]
			data[i] = temp
	return data


def grid2D(w, h, d=0.0):
	g = []
	for x in range(w):
		g.append([])
		for y in range(h):
			g[x].append(d)
	return g

def Interpolate(a, b, f):
	return a*(1-f) + f*b


def gridToStr(g):
	w = len(g)
	h = len(g[0])
	data = u''
	for x in range(w):
		for y in range(h): data += u'%s ' % str(g[x][y])
		data = data.rstrip()
		data = data + '\n'
	return data


def GenerateTopography(level_data, base_map, biome_map, out_file):
	b_seed = level_data['seed'].to_bytes(8, sys.byteorder)
	
	world_xSect = len(biome_map)
	world_ySect = len(biome_map[0])
	
	sect_width = level_data['sect_width']
	sect_height = level_data['sect_height']
	
	b_max_lng = world_xSect.to_bytes(8, sys.byteorder)
	b_max_lat = world_ySect.to_bytes(8, sys.byteorder)
	
	b_sect_width = sect_width.to_bytes(8, sys.byteorder)
	b_sect_height = sect_height.to_bytes(8, sys.byteorder)
	
	with open(out_file, 'wb') as file:
		file.write(b_seed)
		file.write(b_max_lng)
		file.write(b_max_lat)
		file.write(b_sect_width)
		file.write(b_sect_height)
		
		xOff = 0
		for lng in range(world_xSect):
			yOff = 0
			for lat in range(world_ySect):
				sector_biome = int(biome_map[lng][lat] * 255)
				file.write( sector_biome.to_bytes(1, sys.byteorder) )
				for x in range(sect_width):
					for y in range(sect_height):
						tile_height = int(base_map[x+xOff][y+yOff] * 255)
						file.write( tile_height.to_bytes(1, sys.byteorder) )
				yOff += sect_height
			xOff += sect_width


def LoadStoredSector(file_path): # TODO: IMPLEMENT
	return {'biome':0, 'owner':'Nature', 'width':32, 'height':32, 'ground':[], 'floor':[], 'walls':[], 'roof':[], 'objects':[], 'entities':[] }


def ReadTopographyAt(file_path, d_xSect, d_ySect):
	# d_ stands for 'desired_'
	with open(file_path, 'rb') as tpf:
		# This is the amount of bytes the topography file currently uses
		base_offset = 40
		# First 8 bytes store the seed
		seed = int.from_bytes(tpf.read(8), sys.byteorder)
		# Next 8 bytes are the maximum X sector
		max_xSect = int.from_bytes(tpf.read(8), sys.byteorder)
		# Next 8 bytes are the maximum Y sector
		max_ySect = int.from_bytes(tpf.read(8), sys.byteorder) 
		# Next 8 bytes are the width of a sector
		sect_width = int.from_bytes(tpf.read(8), sys.byteorder)
		# Next 8 bytes are the height of a sector
		sect_height = int.from_bytes(tpf.read(8), sys.byteorder)
		
		# Prepare grid
		topography = grid2D(sect_width, sect_height, 0)
		
		# Calculates the ammount of bytes in a sector, including the biome byte
		bytes_per_sect = (sect_width*sect_height) + 1
		
		# Now much sectors in the offset
		skip_for_x = (bytes_per_sect*(d_xSect)*max_ySect)
		if skip_for_x < 0: skip_for_x = 0
		skip_for_y = d_ySect*bytes_per_sect
		if skip_for_y < 0: skip_for_y = 0
		sectors_offset = skip_for_x + skip_for_y
		
		# Sums base and sectors offset for the effective offset
		offset = base_offset + sectors_offset
		
		# Get the sector base biome
		tpf.seek(offset)
		biome = int.from_bytes(tpf.read(1), sys.byteorder)
		
		# Read all the sector and map it to the prepared grid
		for x in range(sect_width):
			for y in range(sect_height):
				val = int.from_bytes(tpf.read(1), sys.byteorder)
				topography[x][y] = val
	
	# Return a tuple with the read topography and base biome
	return (topography, biome)


def AuthUser(username, password, email='unknown'):
	db_path = u'%s/data/%s' % (viper.SERVER_HOME, viper.CONF['player-db'])
	print(u'\nOpenning player database on %s\n' % db_path)
	db_conn = sqlite3.connect(db_path)
	cursor = db_conn.cursor()
	query_select = u'SELECT * FROM player WHERE username=?;'
	query_insert = u'INSERT INTO player (username, email, password) VALUES (?, ?, ?)'
	cursor.execute(query_select, (username,))
	result = cursor.fetchall()
	print(u'AuthUser received:\n\tusername = %s\n\tpassword = %s\n\temail = %s' % (username, password, email) )
	if len(result) > 0:
		curr_pass = u'%s' % str(result[0][16]).strip()
		recv_pass = u'%s' % str(password).strip()
		if curr_pass == recv_pass:
			return True, 'Player authenticated', ParsePlayerDataFromDB(result[0])
		else:
			return False, 'Wrong password', {}
	else:
		cursor.execute(query_insert, (username, password, email) )
		db_conn.commit()
		cursor.execute(query_select, (username,))
		result = cursor.fetchall()
		if len(result) > 0:
			return True, 'New player added', ParsePlayerDataFromDB(result[0])
		else:
			return False, 'Unknown error ocurred', None

def LoadPlayerFromDB(player_id):
	pid = treatData(player_id)
	db_conn = sqlite3.connect('%s/data/%s' % (viper.SERVER_HOME, viper.CONF['player-db']) )
	cursor = db_conn.Cursor()
	query_select = u'SELECT * FROM player WHERE id=?";'
	cursor.execute(query_select, (pid,) )
	result = cursor.fetchall()
	if len(result) > 0:
		return ParsePlayerDataFromDB(result[0])
	else:
		return []

def ParsePlayerDataFromDB(db_data):
	player = {}
	player['id'] = db_data[0]
	player['name'] = db_data[1]
	player['lvl'] = db_data[2]
	player['exp'] = db_data[3]
	player['class'] = db_data[4]
	player['world'] = db_data[5]
	player['wlvl'] = db_data[6]
	player['x'] = db_data[7]
	player['y'] = db_data[8]
	player['z'] = db_data[9]
	player['spawn_world'] = db_data[10]
	player['spawn_wlvl'] = db_data[11]
	player['spawn_x'] = db_data[12]
	player['spawn_y'] = db_data[13]
	player['spawn_z'] = db_data[14]
	for n in player:
		player[n] = treatData(player[n])
	return player






















