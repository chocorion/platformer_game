#!/usr/bin/python3
import pygame
from pygame.locals import *

from Player import Player
from Map import Map
from Display import Display
from Controller import Controller


class Game():
	"""
		Classe qui gère le jeu. C'est en quelque sorte le "modèle".
		Il récupère les informations du controleurs, met à jour les données.
	"""

	def __init__(self, map_path="map_00.map"):
		
		pygame.init()

		self.game_map = Map()
		self.game_map.load(map_path)

		self.display = Display(self, self.game_map.screen_width, self.game_map.screen_height)
		self.controller = Controller(self)

		self.player = Player(self)

		#gestion des FPS
		self.fps = 30
		self.clock = pygame.time.Clock()

	def tick(self):
		"""Fonction appellée à chaque tout de boucle"""
		dt = self.clock.tick(self.fps)	#On évite d'aller trop vite

		self.controller.tick()

		self.player.tick(dt)
		self.display.tick()
		

	def quit(self):
		pygame.quit()
