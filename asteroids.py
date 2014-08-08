import pygame
import math
import random
import time

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.imageMaster = pygame.image.load('images/ship1.png').convert()
		self.image = self.imageMaster
		self.rect = self.image.get_rect()
		self.image.set_colorkey(white)
		self.direction = 0
		self.angle = 0
		self.dx = 0
		self.dy = 0
		self.speed = 5
		self.deg = 0
		self.d_deg = 0
		self.accel = 0
		self.moveforward = False

	def update(self):
		self.deg += self.d_deg
		#self.speed += self.accel
		self.angle = math.radians(self.deg)
		oldcenter = self.rect.center
		self.rotate()
		self.rect = self.image.get_rect()
		self.rect.center = oldcenter
		if self.moveforward == True:
			self.move()
		self.wrap()

	def wrap(self):
		if self.rect.x > WIDTH:
			self.rect.x = 0
		if self.rect.x < 0:
			self.rect.x = WIDTH
		if self.rect.y < 0:
			self.rect.y = HEIGHT
		if self.rect.y > HEIGHT:
			self.rect.y = 0
	def move(self):
		self.rect.x += math.cos(self.angle) * self.speed
		self.rect.y += math.sin(self.angle) * self.speed

	def rotate(self):
		self.image = pygame.transform.rotate(self.imageMaster, -math.degrees(self.angle)-90)
		#angle = 0

class Enemy(pygame.sprite.Sprite):
	def __init__(self, width, height):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([width, height])
		self.image.fill(red)
		self.rect = self.image.get_rect()
		self.speed  = 2
	def wrap(self):
		if self.rect.y < 0:
			self.rect.y = HEIGHT
		if self.rect.y > HEIGHT:
			self.rect.y = 0
	def update(self):
		self.move()
	def move(self):
		self.rect.y += self.speed


class Bullet(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([4,10])
		self.image.fill(white)
		self.rect = self.image.get_rect()
		self.angle = 0
		self.speed = 5

	def update(self):
		self.move()

	def move(self):
		self.rect.x += math.cos(self.angle) * self.speed
		self.rect.y += math.sin(self.angle) * self.speed

WIDTH = 640
HEIGHT = 480

pygame.init()
pygame.font.init()

font = pygame.font.Font(None, 36)

size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)

enemies = pygame.sprite.Group()
sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()

for i in range(30):
	enemy = Enemy(20, 20)
	enemy.rect.x = random.randrange(640)
	enemy.rect.y = random.randrange(480)
	enemies.add(enemy)
	sprites.add(enemy)

player = Player()
player.rect.x = 300
player.rect.y = 200
sprites.add(player)

done = False
clock = pygame.time.Clock()
score = 0

while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT:
				player.d_deg = 5
			if event.key == pygame.K_LEFT:
				player.d_deg = -5
			if event.key == pygame.K_UP:
				player.moveforward = True
			if event.key == pygame.K_SPACE:
				bullet = Bullet()
				bullet.rect.center = player.rect.center
				bullet.angle = player.angle
				sprites.add(bullet)
				bullets.add(bullet)
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_RIGHT:
				player.d_deg = 0
			if event.key == pygame.K_LEFT:
				player.d_deg = 0
			if event.key == pygame.K_UP:
				player.moveforward = False

	for bullet in bullets:
		bullet.update()
		hit_list = pygame.sprite.spritecollide(bullet, enemies, True)

		for entity in hit_list:
			bullets.remove(bullet)
			sprites.remove(bullet)
			score += 1

		if bullet.rect.x > 650 or bullet.rect.x < -10 or bullet.rect.y > 490 or bullet.rect.y < -10:
			bullets.remove(bullet)
			sprites.remove(bullet)

	player.update()

	enemy.update()

	hit_list = pygame.sprite.spritecollide(player, enemies, True)
	for entity in hit_list:
		score += 1

	screen.fill(black)
	sprites.draw(screen)

	text = font.render("Score: "+str(score), True, green)
	textpos = [10, 10]
	screen.blit(text, textpos)

	timer = font.render("Score: "+str(pygame.time.get_ticks()), True, green)
	timerpos = [480, 10]
	screen.blit(timer, timerpos)


	clock.tick(60)
	pygame.display.flip()

	if score == 30:
		pygame.time.wait(3000)
		pygame.quit()
pygame.quit()