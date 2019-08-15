
import sys
import pygame


# 简单按钮
class EasyButton(pygame.sprite.Sprite):
	def __init__(self, position=(320, 100)):
		pygame.sprite.Sprite.__init__(self)
		self.img_1 = pygame.Surface((285, 100))
		self.img_1_front = pygame.Surface((281, 96))
		self.img_1.fill((255, 255, 255))
		self.img_1_front.fill((0, 0, 0))
		self.img_1.blit(self.img_1_front, (2, 2))
		self.img_2 = pygame.Surface((285, 100))
		self.img_2_front = pygame.Surface((281, 96))
		self.img_2.fill((255, 255, 255))
		self.img_2_front.fill((24, 196, 40))
		self.img_2.blit(self.img_2_front, (2, 2))
		self.text = 'easy'
		self.font = pygame.font.Font('./resource/fonts/m04.ttf', 42)
		self.textRender = self.font.render(self.text, 1, (255, 255, 255))
		self.img_1.blit(self.textRender, (60, 29))
		self.img_2.blit(self.textRender, (60, 29))
		self.image = self.img_1
		self.rect = self.image.get_rect()
		self.rect.center = position
		self.type=2
	def update(self):
		mouse_pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(mouse_pos):
			self.image = self.img_2
		else:
			self.image = self.img_1


# 中等难度按钮
class MediumButton(pygame.sprite.Sprite):
	def __init__(self, position=(320, 250)):
		pygame.sprite.Sprite.__init__(self)
		self.img_1 = pygame.Surface((285, 100))
		self.img_1_front = pygame.Surface((281, 96))
		self.img_1.fill((255, 255, 255))
		self.img_1_front.fill((0, 0, 0))
		self.img_1.blit(self.img_1_front, (2, 2))
		self.img_2 = pygame.Surface((285, 100))
		self.img_2_front = pygame.Surface((281, 96))
		self.img_2.fill((255, 255, 255))
		self.img_2_front.fill((24, 30, 196))
		self.img_2.blit(self.img_2_front, (2, 2))
		self.text = 'medium'
		self.font = pygame.font.Font('./resource/fonts/m04.ttf', 42)
		self.textRender = self.font.render(self.text, 1, (255, 255, 255))
		self.img_1.blit(self.textRender, (15, 29))
		self.img_2.blit(self.textRender, (15, 29))
		self.image = self.img_1
		self.rect = self.image.get_rect()
		self.rect.center = position
		self.type=5
	def update(self):
		mouse_pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(mouse_pos):
			self.image = self.img_2
		else:
			self.image = self.img_1


# 困难难度按钮
class HardButton(pygame.sprite.Sprite):
	def __init__(self, position=(320, 400)):
		pygame.sprite.Sprite.__init__(self)
		self.img_1 = pygame.Surface((285, 100))
		self.img_1_front = pygame.Surface((281, 96))
		self.img_1.fill((255, 255, 255))
		self.img_1_front.fill((0, 0, 0))
		self.img_1.blit(self.img_1_front, (2, 2))
		self.img_2 = pygame.Surface((285, 100))
		self.img_2_front = pygame.Surface((281, 96))
		self.img_2.fill((255, 255, 255))
		self.img_2_front.fill((196, 24, 24))
		self.img_2.blit(self.img_2_front, (2, 2))
		self.text = 'hard'
		self.font = pygame.font.Font('./resource/fonts/m04.ttf', 42)
		self.textRender = self.font.render(self.text, 1, (255, 255, 255))
		self.img_1.blit(self.textRender, (60, 29))
		self.img_2.blit(self.textRender, (60, 29))
		self.image = self.img_1
		self.rect = self.image.get_rect()
		self.rect.center = position
		self.type=8
	def update(self):
		mouse_pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(mouse_pos):
			self.image = self.img_2
		else:
			self.image = self.img_1


# 游戏模式选择界面
class CHOICE():
	def __init__(self, WIDTH, HEIGHT):

		
		
		self.EB = EasyButton()
		self.MB = MediumButton()
		self.HB = HardButton()
	# 外部调用
	def update(self, screen):
		clock = pygame.time.Clock()
		
		self.Bs = pygame.sprite.Group(self.EB, self.MB, self.HB)
		difficulty_choice=None
		difficulty_type=1
		while True:
			clock.tick(60)
			screen.fill((0, 0, 0))
			self.Bs.update()
			self.Bs.draw(screen)
			pygame.display.flip()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit(0)
					pygame.quit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						mouse_pos = pygame.mouse.get_pos()
						idx = 0
						for b in self.Bs:
							idx += 1
							if b.rect.collidepoint(mouse_pos):
								difficulty_choice = b.text
								difficulty_type = b.type
								print (difficulty_type)
			if difficulty_choice:
				break
		return difficulty_type