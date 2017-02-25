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

import sys
#from PIL import Image


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

"""
def printImg(data, name):
	w = len(data)
	h = len(data[0])
	img = Image.new('RGB', (w, h) )
	for x in range(w):
		for y in range(h):
			blue = int( 256 * data[x][y] )
			img.putpixel( (x,y), (0,0,blue) )
	img.save(name, 'PNG')
"""

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

"""
def TestTopographyFile(tp_file):
	print('Testing topography %s' % tp_file)
	
	# Data reading
	with open(tp_file, 'rb') as level:
		# Read seed, 8 bytes
		b_seed = level.read(8)
		seed = int.from_bytes(b_seed, sys.byteorder)
		# Read max X sectors, 8 bytes
		b_max_xSec = level.read(8)
		max_xSec = int.from_bytes(b_max_xSec, sys.byteorder)
		# read max Y sectors, 8 bytes
		b_max_ySec = level.read(8)
		max_ySec = int.from_bytes(b_max_ySec, sys.byteorder)
		# read sector width, 8 bytes
		b_sect_width = level.read(8)
		sect_width = int.from_bytes(b_sect_width, sys.byteorder)
		# read sector height, 8 bytes
		b_sect_height = level.read(8)
		sect_height = int.from_bytes(b_sect_height, sys.byteorder)
		
		
		img_width = max_xSec * sect_width
		img_height = max_ySec * sect_height
		img = Image.new('RGB', (img_width, img_height) )
		
		xOff = 0
		for xSec in range(max_xSec):
			yOff = 0
			for ySec in range(max_ySec):
				b_red = level.read(1)
				red = int.from_bytes(b_red, sys.byteorder)
				for x in range(sect_width):
					for y in range(sect_height):
						b_green = level.read(1)
						green = int.from_bytes(b_green, sys.byteorder)
						img.putpixel( (x+xOff,y+yOff), (red, green, 0) )
				yOff += sect_height
			xOff += sect_width
	
	img_name = tp_file.rstrip('dat') + 'png'
	img.save(img_name)
	print('Results written to %s' % img_name)
"""

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

"""
def TestReadSectorTopography(topography, biome, lvl_path, xSect, ySect):
	width = len(topography)
	height = len(topography[0])
	
	img = Image.new('RGB', (width,height) )
	
	for x in range(width):
		for y in range(height):
			img.putpixel((x,y), (0, topography[x][y], 0) )
	
	img.save('%s/sect_%d_%d_topography_b%d.png' % (lvl_path, xSect, ySect, biome) )
"""

























