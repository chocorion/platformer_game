#!/usr/bin/python3
import pygame
from pygame.locals import *
from Game import *

TILESIZE = 16

class Display():
	"""Classe qui gère tout ce qui concerne l'affichage du jeu"""
	def __init__(self, game, width = 40, height = 30):
		self.game = game 	#Besoin pour acceder à tous les éléments du jeu
		self.width = width * TILESIZE
		self.height = height * TILESIZE

		self.tileset = pygame.image.load("tileset.png")

		self.tile_dict = dict()			#Contient les différentes images pour chaque composant visuel du jeu
		self.tile_status = dict() 		#Pour chaque animation -> [current_frame, max_frame, frame_speed]
								 		#Attention avec ce système garde en mémoire ou on en étais dans l'animation, peut reprendre une animation en plein mouvement
								 		#A voir par la suite si c'est génant

		self.screen = pygame.display.set_mode((self.width, self.height))


		self.load_player_sprite()	#A mettre plus tard dans une fonction plus générale de chargement
		self.load_wall_sprite()


	def load_player_sprite(self):
		self.tile_dict["player_static"]   = list()
		self.tile_status["player_static"] = [0, 3, 0.15]

		self.tile_dict["player_move"]   = list()
		self.tile_status["player_move"] = [0, 8, 0.3]

		self.tile_dict["player_bump"]   = list()
		self.tile_status["player_bump"] = [0, 5, 1]

		self.tile_dict["player_strike"] = list()
		self.tile_status["player_strike"] = [0, 4, 0.2]

		#On découpe dans l'image contenant tous les sprites
		for x in range(0, 3 * TILESIZE, TILESIZE):
			self.tile_dict["player_static"].append(self.tileset.subsurface((x, 16 * TILESIZE, TILESIZE, TILESIZE)))

		for x in range(3 * TILESIZE, 8 * TILESIZE, TILESIZE):
			self.tile_dict["player_bump"].append(self.tileset.subsurface((x, 16 * TILESIZE, TILESIZE, TILESIZE)))

		for x in range(0, 8 * TILESIZE, TILESIZE):
			self.tile_dict["player_move"].append(self.tileset.subsurface((x, 17 * TILESIZE, TILESIZE, TILESIZE)))

		for x in range(0, 4 * TILESIZE, TILESIZE):
			self.tile_dict["player_strike"].append(self.tileset.subsurface((x, 19 * TILESIZE, TILESIZE, TILESIZE)))


	def load_wall_sprite(self):
		self.tile_dict["1"] = self.tileset.subsurface((0, TILESIZE, TILESIZE, TILESIZE))
		self.tile_dict["6"] = self.tileset.subsurface((6 * TILESIZE, TILESIZE, TILESIZE, TILESIZE))
		self.tile_dict["7"] = self.tileset.subsurface((7 * TILESIZE, TILESIZE, TILESIZE, TILESIZE))
		self.tile_dict["8"] = self.tileset.subsurface((8 * TILESIZE, TILESIZE, TILESIZE, TILESIZE))
		self.tile_dict["9"] = self.tileset.subsurface((9 * TILESIZE, TILESIZE, TILESIZE, TILESIZE))
		self.tile_dict["t"] = self.tileset.subsurface((10 * TILESIZE, TILESIZE, TILESIZE, TILESIZE))
		self.tile_dict[")"] = self.tileset.subsurface((11 * TILESIZE, TILESIZE, TILESIZE, TILESIZE))
		self.tile_dict["b1"] = self.tileset.subsurface((0, 0, TILESIZE, TILESIZE))
		self.tile_dict["b2"] = self.tileset.subsurface((TILESIZE, 0, TILESIZE, TILESIZE))
		self.tile_dict["b3"] = self.tileset.subsurface((2 * TILESIZE, 0, TILESIZE, TILESIZE))
		self.tile_dict["b4"] = self.tileset.subsurface((3 * TILESIZE, 0, TILESIZE, TILESIZE))

	def show_player(self):
		"""Affiche le joueur à l'écran"""
		state = self.game.player.state	#Jeu d'animation à choisir, mis à jour par le joueur

		image = self.tile_dict[state][int(self.tile_status[state][0])]

		#Rotation en fonction de la direction
		if self.game.player.look == "left":
			image = pygame.transform.flip(image, True, False)



		#Mise à jour de l'animation en cours
		old_frame = self.tile_status[state][0]
		self.tile_status[state][0] = (self.tile_status[state][0] + self.tile_status[state][2]) % self.tile_status[state][1]

		#Permet de garder l'animation bump jusqu'à la fin sans interruption par d'autres jeux d'animation
		#A changer plus tard, par exemple strike peut etre prioritaire sur l'animation bump
		if state == "player_bump" and old_frame + self.tile_status[state][2] >= self.tile_status[state][1]:
			if self.game.player.vx != 0:
				self.game.player.state = "player_move"
			else:
				self.game.player.state = "player_static"

		if state == "player_strike" and old_frame + self.tile_status[state][2] >= self.tile_status[state][1]:
			if self.game.player.vx != 0:
				self.game.player.state = "player_move"
			else:
				self.game.player.state = "player_static"

		image = self.tile_dict[state][int(self.tile_status[state][0])]

		#Rotation en fonction de la direction
		if self.game.player.look == "left":
			image = pygame.transform.flip(image, True, False)

		self.screen.blit(image, (self.game.player.x, self.game.player.y))

	def show_map(self):
		m = self.game.game_map.map
		for y in range(len(m)):
			for x in range(len(m[0])):
				if m[y][x] == '0':
					continue
				else:
					self.screen.blit(self.tile_dict[m[y][x]], (x * TILESIZE, y * TILESIZE))



	def tick(self):
		"""Effectué à chaque tour de boucle"""
		self.screen.fill((0, 0, 0))
		self.show_map()
		self.show_player()
		pygame.display.flip()
