import pygame

class Button():

	def __init__(self, ai_game, msg, y_offset=0, color=(0, 200, 0), hover_color=(0, 250, 154)):
		self.screen = ai_game.screen
		self.screen_rect = self.screen.get_rect()

		self.width, self.height = 200, 50
		self.button_color = color
		self.hover_color = hover_color
		self.text_color = (255, 255, 255)
		self.font = pygame.font.SysFont(None, 48)

		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.centerx = self.screen_rect.centerx
		self.rect.centery = self.screen_rect.centery + y_offset

		self._prep_msg(msg)

	def _prep_msg(self, msg):
		self.msg_image = self.font.render(msg, True, self.text_color)
		self.msg_image_rect = self.msg_image.get_rect()
		self.msg_image_rect.center = self.rect.center

	def draw_button(self):
		mouse_pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(mouse_pos):
			current_color = self.hover_color
		else:
			current_color = self.button_color
		self.screen.fill(current_color, self.rect)
		pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 3)
		self.screen.blit(self.msg_image, self.msg_image_rect)