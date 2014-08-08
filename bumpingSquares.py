import pygame
import math
import random

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

#Defining the Squares
class Square(pygame.sprite.Sprite):
	#Position
	x = 0
	y = 0


	size = (50, 50)

	def __init__(self, color):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface (self.size)
		self.image.fill (color)
		self.dx = 0
		self.dy = 0
		self.rect = self.image.get_rect()
	def move(self):
		self.rect.x += self.dx
		self.rect.y += self.dy
		if self.rect.right > 700:
			self.dx *= -1
		if self.rect.left < 0:
			self.dx *= -1
		if self.rect.top < 0:
			self.dy *= -1
		if self.rect.bottom > 900:
			self.dy *= -1


pygame.init()
size = (700, 900)
screen = pygame.display.set_mode(size)
pygame.display.set_caption ("Colliding Squares")

#Players
dude  = Square(red)
dude.rect.x = 430
dude.rect.y = 230
dude.dy = 0
dude.dx = 0


dude2  = Square(blue)
dude2.rect.x = 100
dude2.rect.y = 230
dude2.dy = 0
dude2.dx = 0

dude_list = pygame.sprite.Group()
dude_list.add(dude)

other_list = pygame.sprite.Group()
other_list.add(dude2)

done = False

clock = pygame.time.Clock()

#MAIN LOOP
while not(done):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
				done = True
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT:
				dude.dx = 3
			if event.key == pygame.K_LEFT:
				dude.dx = -3
			if event.key == pygame.K_UP:
				dude.dy = -3
			if event.key == pygame.K_DOWN:
				dude.dy = 3
			if event.key == pygame.K_d:
				dude2.dx = 3
			if event.key == pygame.K_a:
				dude2.dx = -3
			if event.key == pygame.K_w:
				dude2.dy = -3
			if event.key == pygame.K_s:
				dude2.dy = 3
				

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_RIGHT:
				dude.dx = 0
			if event.key == pygame.K_LEFT:
				dude.dx = 0
			if event.key == pygame.K_UP:
				dude.dy = 0
			if event.key == pygame.K_DOWN:
				dude.dy = 0
			if event.key == pygame.K_d:
				dude2.dx = 0
			if event.key == pygame.K_a:
				dude2.dx = 0
			if event.key == pygame.K_w:
				dude2.dy = 0
			if event.key == pygame.K_s:
				dude2.dy = 0
	dude.move()
	dude2.move()
	if pygame.sprite.groupcollide(dude_list, other_list, False, False):
		dude.dx *= -1
		dude2.dx *= -1
		dude2.dy *= -1
		dude.dy *= -1

#DRAWING LOGIC
	screen.fill(white)
	dude_list.draw(screen)
	other_list.draw(screen)
	#ALL DRAWING GOES AFTER THE SCREEN FILL AND BEFORE FLIP
	pygame.display.flip()
	clock.tick(60)

pygame.quit()