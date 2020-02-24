#!/usr/bin/python3
import pygame
import os

TILESIZE = 16
SOLID_BLOCS = ['1', '6', '7', '8', '9', 't', ')']

class Map:
	def __init__(self):
		pass

	def load(self, path):
		try:
			file = open(path, 'r')
		except:
			print("Erreur lors de l'ouverture de " + path)

		map_file = file.read().split('\n')
		file.close()

		self.screen_width, self.screen_height = [int(i) for i in map_file[0].split()]
		self.map_width, self.map_height = [int(i) for i in map_file[1].split()]


		self.map = [i.split(" ") for i in map_file[2:len(map_file) - 1]]


	def collision_map(self, x, y, w, h):

		collision = False

		x = int(x)
		h = int(h)
		w = int(w)

		for map_x in range(x//TILESIZE, (x + w)//TILESIZE + 1):
			for map_y in range(round(y/TILESIZE), (int(y) + h)//TILESIZE + 1):	#Car y se trouve souvent avec des erreurs d'arrondie
				if map_x >= self.map_width or map_x < 0 or map_y < 0 or map_y >= self.map_height:

					collision = collision or False
					continue

				collision = collision or (self.map[int(map_y)][int(map_x)] in SOLID_BLOCS)
				if collision:
					return True
