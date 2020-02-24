import pygame
from pygame.locals import *


class Controller:
    """Gère les interactions utilisateurs"""
    def __init__(self, game):
        self.game = game
        pygame.key.set_repeat(1,200)    #Permet la répétition de touche, interval de 200 ms

    def tick(self):
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                self.game.quit()
                exit()

            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:

                if event.key == pygame.K_SPACE: 
                    self.game.player.update("strike", event.type == pygame.KEYDOWN)

                elif event.key == pygame.K_q:
                    self.game.player.update("left", event.type == pygame.KEYDOWN)

                elif event.key == pygame.K_d:
                    self.game.player.update("right", event.type == pygame.KEYDOWN)

                elif event.key == pygame.K_z:
                    self.game.player.update("up", event.type == pygame.KEYDOWN)

                elif event.key == pygame.K_s:
                    self.game.player.update("down", event.type == pygame.KEYDOWN)

