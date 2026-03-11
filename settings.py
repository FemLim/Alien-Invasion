import pygame
from utils import resource_path

class Settings():
	
	def __init__(self):
		self.screen_width = 1280
		self.screen_height = 820
		self.full_bg_image = pygame.image.load(resource_path('images/bg.png'))
		self.bg_image = pygame.transform.scale(self.full_bg_image,\
    		(self.screen_width, self.screen_height))
		self.shoot_sound = pygame.mixer.Sound(resource_path('sounds/laser.wav'))
		self.shoot_sound_volume = 0.1
		self.explosion_sound = pygame.mixer.Sound(resource_path('sounds/explosion.wav'))
		self.explosion_sound_volume = 0.1
		self.background_music = pygame.mixer.music.load\
			(resource_path('sounds/background_music.mp3'))
		self.background_music_volume = 0.3
		self.ship_limit = 3
		self.bullet_color = (0, 255, 255)
		self.bullet_width = 3
		self.bullet_height = 15

		self.speedup_scale = 1.1
		self.score_scale = 1.2
		self.initialize_dynamic_settings()
		

	def initialize_dynamic_settings(self):
		self.ship_speed = 1
		self.bullet_speed = 2
		self.alien_speed = 0.4
		self.fleet_drop_speed = 10
		self.fleet_direction = 1
		self.alien_points = 50

	def increase_speed(self):
		self.ship_speed *= self.speedup_scale
		self.bullet_speed *= self.speedup_scale
		self.alien_speed *= self.speedup_scale
		self.alien_points = int(self.alien_points * self.score_scale)