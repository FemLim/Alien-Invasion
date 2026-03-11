import pygame
import sys
from pygame.sprite import Sprite
from utils import resource_path

class Ship(Sprite):
	"""docstring for GameCharectrer"""
	def __init__(self, ai_game):
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.screen_rect = ai_game.screen.get_rect()


		self.image = pygame.image.load(resource_path('images/ship.png'))
		self.rect = self.image.get_rect()	

		self.moving_right = False
		self.moving_left =  False

		self.rect.midbottom = self.screen_rect.midbottom

	def center_ship(self):
		self.rect.midbottom = self.screen_rect.midbottom
		self.x = float(self.rect.x)

	def update(self):
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.rect.x += self.settings.ship_speed
		if self.moving_left and self.rect.left > 0:
			self.rect.x -= self.settings.ship_speed

	def blitme(self):

		self.screen.blit(self.image, self.rect)		