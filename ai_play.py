import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
		player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
		self.player_walk = [player_walk_1,player_walk_2]
		self.player_index = 0
		self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

		self.image = self.player_walk[self.player_index]
		self.rect = self.image.get_rect(midbottom = (80,300))
		self.gravity = 0

		self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
		self.jump_sound.set_volume(0.5)

	def player_input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
			self.gravity = -20
			self.jump_sound.play()

	def apply_gravity(self):
		self.gravity += 1
		self.rect.y += self.gravity
		if self.rect.bottom >= 300:
			self.rect.bottom = 300

	def animation_state(self):
		if self.rect.bottom < 300: 
			self.image = self.player_jump
		else:
			self.player_index += 0.1
			if self.player_index >= len(self.player_walk):self.player_index = 0
			self.image = self.player_walk[int(self.player_index)]

	def update(self):
		self.player_input()
		self.apply_gravity()
		self.animation_state()

class Obstacle(pygame.sprite.Sprite):
	def __init__(self,type):
		super().__init__()
		
		if type == 'fly':
			fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
			fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
			self.frames = [fly_1,fly_2]
			y_pos = 210
		else:
			snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
			snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
			self.frames = [snail_1,snail_2]
			y_pos  = 300

		self.animation_index = 0
		self.image = self.frames[self.animation_index]
		self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

	def animation_state(self):
		self.animation_index += 0.1 
		if self.animation_index >= len(self.frames): self.animation_index = 0
		self.image = self.frames[int(self.animation_index)]

	def update(self):
		self.animation_state()
		self.rect.x -= 6
		self.destroy()

	def destroy(self):
		if self.rect.x <= -100: 
			self.kill()

# def display_score():
# 	current_time = int(pygame.time.get_ticks() / 1000) - start_time
# 	score_surf = test_font.render(f'Score: {current_time}',False,(64,64,64))
# 	score_rect = score_surf.get_rect(center = (400,50))
# 	screen.blit(score_surf,score_rect)
# 	return current_time

# def collision_sprite():
# 	if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
# 		obstacle_group.empty()
# 		return False
# 	else: return True

class GameAI:
	def __init__(self):
		self.screen = pygame.display.set_mode((800,400))
		self.clock = pygame.time.Clock()
		self.game_active = True #TODO: Change it
		self.start_time = 0
		self.score = 0
		self.player = pygame.sprite.GroupSingle()
		self.player.add(Player())
		self.obstacle_group = pygame.sprite.Group()
		self.sky_surface = pygame.image.load('graphics/Sky.png').convert()
		self.ground_surface = pygame.image.load('graphics/ground.png').convert()
		self.obstacle_timer = pygame.USEREVENT + 1
		self.test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

		pygame.time.set_timer(self.obstacle_timer,1500)
		
	def display_score(self):
		current_time = int(pygame.time.get_ticks() / 1000) - self.start_time
		score_surf = self.test_font.render(f'Score: {current_time}',False,(64,64,64))
		score_rect = score_surf.get_rect(center = (400,50))
		self.screen.blit(score_surf,score_rect)
		return current_time

	def collision_sprite(self):
		if pygame.sprite.spritecollide(self.player.sprite,self.obstacle_group,False):
			self.obstacle_group.empty()
			return False
		else: return True

	def play(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			if self.game_active:
				if event.type == self.obstacle_timer:
					self.obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail'])))
			else:
				if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
					self.game_active = True
					self.start_time = int(pygame.time.get_ticks() / 1000)
	
			if self.game_active:
				self.screen.blit(self.sky_surface,(0,0))
				self.screen.blit(self.ground_surface,(0,300))
				self.score = self.display_score()
				
				self.player.draw(self.screen)
				self.player.update()

				self.obstacle_group.draw(self.screen)
				self.obstacle_group.update()

				game_active = self.collision_sprite()
				
			else:
				pygame.quit()

			pygame.display.update()
			self.clock.tick(60)
		
		
pygame.init()
pygame.display.set_caption('Runner')
game = GameAI()

while True:
	game.play()