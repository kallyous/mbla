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

import random
from viper.viperconf import *


def WhiteNoise(w, h, s):
	random.seed(s)
	g = []
	for x in range(w):
		g.append([])
		for y in range(h):
			g[x].append(random.random())
	return g


def SmoothNoise(base_noise, octave):
	width = len(base_noise)
	height = len(base_noise[0])
	
	smooth_noise = grid2D(width, height)
	period = pow(2, octave)
	frequency = 1.0/period
	
	for x in range(width):
		sx0 = (float(x) // period) * period
		sx1 = (sx0 + period) % width
		blend_hor = (float(x) - sx0) * frequency
		for y in range(height):
			sy0 = (float(y) // period) * period
			sy1 = (sy0 + period) % height
			blend_ver = (float(y) - sy0) * frequency
			
			x0 = int(sx0)
			x1 = int(sx1)
			y0 = int(sy0)
			y1 = int(sy1)
			
			top = Interpolate(base_noise[x0][y0], base_noise[x1][y0], blend_hor)
			bot = Interpolate(base_noise[x0][y1], base_noise[x1][y1], blend_hor)
			final = Interpolate(top, bot, blend_ver)
			
			smooth_noise[x][y] = final
	
	return smooth_noise


def PerlinNoise(base_noise, octave_count, amplitude=1.0, persistance=0.5):
	width = len(base_noise)
	height = len(base_noise[0])
	
	smooth_noises = []
	for i in range(octave_count):
		smooth_noises.append( SmoothNoise(base_noise, i) )
	
	perlin_noise = grid2D(width, height)
	
	total_amp = 0.0
	
	i = octave_count
	for o in range(octave_count):
		i -= 1
		amplitude *= persistance
		total_amp += amplitude
		
		for x in range(width):
			for y in range(height):
				perlin_noise[x][y] += smooth_noises[i][x][y] * amplitude
	
	for x in range(width):
		for y in range(height):
			perlin_noise[x][y] = perlin_noise[x][y] / total_amp
	
	return perlin_noise



























