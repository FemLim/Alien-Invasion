import pygame
from pygame.sprite import Sprite
from utils import resource_path

class Alien(Sprite):
	def __init__(self, ai_game):
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings

		self.image = pygame.image.load(resource_path('images/alien.png')).convert_alpha()
		self.rect = self.image.get_rect()

		self.rect.x = self.rect.width
		self.rect.y = self.rect.height

		self.x = float(self.rect.x)

	def dlite(self):
		self.screen.blit(self.image, self.rect)

	def update(self):
		self.x += (self.settings.alien_speed * self.settings.fleet_direction)
		self.rect.x = self.x

	def check_edges(self):
		secreen_rect = self.screen.get_rect()
		if self.rect.right >= secreen_rect.right or self.rect.left <=0:
			return True
