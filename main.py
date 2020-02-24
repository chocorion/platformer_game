#!/usr/bin/python3
from Game import Game

game = Game()


#Boucle principale du jeu
while True:
	game.tick()

game.quit()
