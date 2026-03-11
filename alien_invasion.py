#Подключение библиотекpygame
import pygame
import sys
import time
#Подключение других файлов
from ship import Ship
from settings import Settings
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button_play import Button
from scoreboard import Scoreboard

#Создание основного класса игры
class AlienInvasion:
	"""docstring for AlienInvasion"""

	#Создание метода инциализациии игры
	def __init__(self):
		# Инициализация библитеки Pygame и mixer
		pygame.init()
		pygame.mixer.init()

		# Объявление переменных и присвоенние им значений
		self.settings = Settings()
		self.stats = GameStats(self)

		self.screen = pygame.display.set_mode((\
		self.settings.screen_width, self.settings.screen_height))
		pygame.display.set_caption("Alien Invasion")

		self.play_button = Button(self, "Начать", y_offset=-30, hover_color=(0, 230, 0))
		self.continue_button = Button(self, "Продолжить", y_offset=-90,\
		 hover_color=(0, 230, 0))
		self.exit_button = Button(self, "Выход", y_offset=30, color=(200, 0, 0),\
		 hover_color=(230, 0, 0))
		self.sb = Scoreboard(self)

		self.explosion_sound = self.settings.explosion_sound
		self.explosion_sound.set_volume(self.settings.explosion_sound_volume)

		self.shoot_sound = self.settings.shoot_sound
		self.shoot_sound.set_volume(self.settings.shoot_sound_volume)

		self.ship = Ship(self)
		self.aliens = pygame.sprite.Group()
		self.bullets = pygame.sprite.Group()

	# Метод работаюший в процессе игры
	def run_game(self):

		# Бесконечный цикл для проверки событий
		while True:
			self._check_events()
			if self.stats.game_active and not self.stats.game_pause:
				self.ship.update()	
				self._update_bullets()		
				self._update_aliens()			
			self._update_screen()

	# Метод для старта и рестарта игры
	def _start_game(self):

		# Фоновая музыка
		self.background_music = self.settings.background_music
		# Установка громкости значением из настроек
		pygame.mixer.music.set_volume(self.settings.background_music_volume)
		# Запуск фоновой музыки (-1) - бесконечный повтор
		pygame.mixer.music.play(-1)

		# Перезапись статистики игры
		self.stats.reset_stats()
		# Перезапись очков
		self.sb.prep_score()
		# Перезапись количества жизней
		self.sb.prep_ships()
		# Обнуление уровня
		self.sb.prep_level()
		# Перезапись настроек сложности
		self.settings.initialize_dynamic_settings()
		# Запуск игры
		self.stats.game_active = True
		# Снятие с паузы
		self.stats.game_pause = False
		# Обнуление врагов 
		self.aliens.empty()
		# Обнуление пуль
		self.bullets.empty()

		# Создание новый армии врагов(флота)
		self._create_fleet()
		# Перемещение коробля в центр
		self.ship.center_ship()

		# Скрытие курсора
		pygame.mouse.set_visible(False)

	# Метод проверки событий 
	def _check_events(self):
		# Цикл для проверки событий
		for event in pygame.event.get():
			# Проверка выхода 
			if event.type == pygame.QUIT:
				sys.exit()
			# Проверка нажатие на кнопки клавитуры
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			# Проверка отпускания кнопок клавиатуры
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)
			# Проверка наатия на кнопки мыши
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_menu_button(mouse_pos)

	#Метод проверки нажатия кнопок
	def _check_keydown_events(self, event):
		# Проверка нажатие стрелки вправо		
		if event.key == pygame.K_RIGHT:
			# Движение коробля вправо
			self.ship.moving_right = True
		# Проверка нажатия стрелки влево
		elif event.key == pygame.K_LEFT:
			# Движение коробля влево
			self.ship.moving_left = True
		# Проверка нажатия на пробел
		elif event.key == pygame.K_SPACE:
			# Проверка активна ли игра
			if not self.stats.game_active:
				# Запуск игры если не активна 
				self._start_game()
			else:
				# Если активна то выстрел
				self._fire_bullet()
		# Проверка нажатия на ENTER при не активной игре
		elif event.key == pygame.K_RETURN and not self.stats.game_active: 
			# Если нажат и игра не активна ативировать игру
			self._start_game()
		# Проверка нажатия на ESC
		elif event.key == pygame.K_ESCAPE:
			# Проверка на паузе ли игра
			if self.stats.game_pause:
				# Если была на паузе запустить с задержской 0.2 сек
				time.sleep(0.2)
				self.stats.game_pause = False
				# Скрытие курсора
				pygame.mouse.set_visible(False)
			else: 
				# Если игра была активна Пауза
				self.stats.game_pause = True
		# Проверка нажатия на R во время игры
		elif event.key == pygame.K_r:
			# Если нажата R быстрый перезапуск
			self._start_game()
		# Проверка нажата ли Q
		elif event.key == pygame.K_q:
			# Быстрый выход из игры
			sys.exit()

    # Метод нажатия на кнопки в гланом меню и меню паузы
	def _check_menu_button(self, mouse_pos):
		# Регистрация нажатия на кнопку Начать
		button_clicked = self.play_button.rect.collidepoint(mouse_pos)
		# Проверка нажата ли кнопа и игра на паузе или не активна
		if button_clicked and (not self.stats.game_active or self.stats.game_pause):
			#Вывоз метода перезапуска игры
			self._start_game()
		# Регистрация нажатия на кнопку Выход
		button_clicked = self.exit_button.rect.collidepoint(mouse_pos)
		# Проверка нажатия на кнопку выходи Состояния игры
		if button_clicked and (not self.stats.game_active or self.stats.game_pause):
			# Выход
			sys.exit()
		# Регистрация нажатия на кнопку Продолжить
		button_clicked = self.continue_button.rect.collidepoint(mouse_pos)
		# Проверка нажатия на кнопку 
		if button_clicked:
			# Задаржка 0.2 сек
			time.sleep(0.2)
			# Снаятие игры с паузы
			self.stats.game_pause = False
			# Скрытие курсора
			pygame.mouse.set_visible(False)	
	
	# Метод отпускания кнопок
	def _check_keyup_events(self, event):
		# Проверка опущена ли стрелка вправо
		if event.key == pygame.K_RIGHT:
			# Отстановка движения кораблся вправо
			self.ship.moving_right = False
		# Проверка отпущена ли стрелка влево
		elif event.key == pygame.K_LEFT:
			# Оставновка движения влево
			self.ship.moving_left = False

	# Метод выстрела 
	def _fire_bullet(self):
		# Активация звука выстрела
		self.shoot_sound.play()
		# Создание пули
		new_bullet = Bullet(self)
		# Добавление пули
		self.bullets.add(new_bullet)

	# Обновление(Движение пуль)
	def _update_bullets(self):

		# Вызов метода обновления пуль из файла 
		self.bullets.update()

		# Цикл проверки если ли пули в Группе
		for bullet in self.bullets.copy():
			# Проверка места нахождения пули
			if bullet.rect.bottom <= 0:
				# Если пули нет на экране удалить её
				self.bullets.remove(bullet)

		# Регистрация попаданий пуль по врагам 
		collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True,)
		# Проверка попадания
		if collisions:
			# Цикл для проверка по какому врагу попали
			for aliens in collisions.values():
				# Начисление очко за попадание
				self.stats.score += self.settings.alien_points * len(aliens)
			# Обновление таблицы очков
			self.sb.prep_score()
			# Проверка не побит ли рекорд
			self._check_high_score()
			# Вызов звук попадания 
			self.explosion_sound.play()

		# Проверка не закончились ли враги
		if not self.aliens:
			# Обнавление экрана
			self._update_screen()
			# Задержска 
			time.sleep(0.2)
			# Удаление оставшихся пуль
			self.bullets.empty()	
			# Вызов модуля усложнения 		
			self.settings.increase_speed()
			# Увеличение уровня
			self.stats.level += 1
			# Обновление уровня на экране
			self.sb.prep_level()
			# создание новой армии противника
			self._create_fleet()

	# Метод проверки рекодра
	def _check_high_score(self):
		# Проверка не побит ли реекорд
		if self.stats.score > self.stats.high_score:
			# Если рекорд побит перезапись рекорда
			self.stats.high_score = self.stats.score
			# Перезапись рекорда на экране
			self.sb.prep_high_score()

 	# Метод создания противника
	def _create_alien(self, alien_number, row_number):
		# Созание противника с указание размеров
		alien = Alien(self)
		alien_width = alien.rect.width
		alien_height = alien.rect.height

		# Позиционировние противника
		alien.x = alien_width + 2 * alien_width * alien_number
		alien.rect.x = alien.x
		alien.rect.y = alien_height + 2 * alien_height * row_number

		#Добавление противника
		self.aliens.add(alien)

	# Создание армии из противников 
	def _create_fleet(self):

		# Создание противника
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size

		# Вычисление свободно места для противников
		available_space_x = self.settings.screen_width - (2 * alien_width)
		number_aliens_x = available_space_x // (2 * alien_width)
		available_space_y = self.settings.screen_height - \
			(3 * alien_height) - self.ship.rect.height 

		# Вычисление количества рядов противниковы
		rows_number = 1 + self.stats.level
		# Вычисление максимально возможного количества рядов 
		max_rows = available_space_y // (2 * alien_height)
		# Проверка не привышается ли максимально количество
		rows_number = min(1 + self.stats.level, max_rows)

		# Цикл для создание рядов и противников
		for row_number in range(rows_number):
			for alien_number in range(number_aliens_x):
				self._create_alien(alien_number, row_number)

	#
	def _check_fleet_edges(self):
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break

	def _change_fleet_direction(self):
		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop_speed
		self.settings.fleet_direction *= -1

	def _ship_hit(self):

		self.stats.ships_left -= 1
		self.sb.prep_ships()
		if self.stats.ships_left > 0:		
			self.aliens.empty()
			self.bullets.empty()

			self._create_fleet()
			self.ship.center_ship()

			time.sleep(0.5)
		else:
			self.stats.game_active = False
			pygame.mixer.music.stop()

	def _update_aliens(self):

		self._check_fleet_edges()
		self.aliens.update()

		if pygame.sprite.spritecollideany(self.ship, self.aliens):
			self._ship_hit()


	def _update_screen(self):


			self.screen.blit(self.settings.bg_image, (0, 0))
			self.ship.blitme()
			self.sb.show_score()

			if self.stats.game_pause:
				pygame.mouse.set_visible(True)	
				self.continue_button.draw_button()
				self.play_button.draw_button()
				self.exit_button.draw_button()

			elif not self.stats.game_active:
				pygame.mouse.set_visible(True)	
				self.play_button.draw_button()
				self.exit_button.draw_button()

			for bullet in self.bullets.sprites():
				bullet.draw_bullet()

			self.aliens.draw(self.screen)


			

			pygame.display.flip()

	
if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()