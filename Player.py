#!/usr/bin/python3

#Constante pour les vittesse maximums
VX = 8
VY = 2
VY_MAX = 40
VY_JUMP = 30

class Player():
	def __init__(self, game, x = 0, y = 0, w = 16, h = 16):
		self.game = game
		self.set_pos(x, y)
		self.w = w
		self.h = h
		self.vx = 0
		self.vy = 0

		self.can_fall = True

		self.is_jumping = True#Car tombe en arrivant, à changer selon la map

		self.state = "player_static"	#Status du joueur, qui corresponds au différents jeu d'animations
		self.look = "right"				#Vers ou regarde le joueur, mis à jour en fonction du dernier déplacement

		self.direction = {"left": False, "right":False, "up":False, "down": False, "strike": False}


	def set_pos(self, x, y):
		self.x = x
		self.y = y


	def update(self, dir, state):
		"""Gère le joueur en fonction des entrées claviers"""

		if dir == "left":
			self.direction[dir] = state
			if state:
				self.direction["right"] = False


		if dir == "right":
			self.direction[dir] = state
			if state:
				self.direction["left"] = False

		if dir == "up":
			self.direction[dir] = state

		if dir == "strike":
			self.direction[dir] = state


	def move(self, dt):
		"""Ajuste la position de joueur en fonction tu temps"""


		if self.direction["right"]:
			self.look = "right"

			for i in range(VX, -1, -1):
				if not self.game.game_map.collision_map(self.x + i, self.y, self.w, self.h):
					self.vx = i
					break

		elif self.direction["left"]:
			self.look = "left"

			for i in range(-VX, 1):
				if not self.game.game_map.collision_map(self.x + i, self.y, self.w, self.h):
					self.vx = i
					break

		else:
			self.vx = 0

		if self.direction["up"] and not self.is_jumping and self.state != "player_bump":
			#Player_bump sert de timer pour relancer un saut. A changer plus tard si besoin
			self.vy = -VY_JUMP
			self.is_jumping = True


		#Quand le joueur va se cogner
		if self.vy < 0:
			for i in range(self.vy, 1):
				if not self.game.game_map.collision_map(self.x + self.vx, self.y + i, self.w, self.h):
					self.vy = i
					break

		if self.direction["strike"]:
			self.state = "player_strike"

		elif self.state != "player_bump" and self.state != "player_strike":
			if self.vx != 0:
				self.state = "player_move"
			else:
				self.state = "player_static"

		self.x += dt/100 * self.vx
		self.y += dt/100 * self.vy

	def gravity(self):

		if self.can_fall:
			if not self.game.game_map.collision_map(self.x, self.y + 1, self.w, self.h):
				self.is_jumping = True	#Pour empécher le joueur de sauter lorqu'il tombe dans le vide

				if self.vy + VY < VY_MAX:
					self.vy += VY
				else:
					self.vy = VY_MAX

				for i in range(self.vy):
					if self.game.game_map.collision_map(self.x, self.y + i, self.w, self.h):
						self.vy = i - 1
						self.is_jumping = False
						self.state = "player_bump"
						break
			else:
				self.is_jumping = False
				self.vy = 0



	def tick(self, dt):
		"""Effectué à chaques tours de boucle, prends en argument dt pour connaitre ou on en est niveau temps"""
		self.move(dt)
		self.gravity()
