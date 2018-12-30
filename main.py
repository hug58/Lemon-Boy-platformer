import pygame
from script import Nivel

import os

EARTH = 1
BRICK = 2

pygame.display.init()


TILESIZE = 40

MAPWIDTH = 15
MAPHEIGHT = 12
		
screen = pygame.display.set_mode((MAPWIDTH*TILESIZE,MAPHEIGHT*TILESIZE))

class Tierra(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale2x(pygame.image.load("image/cespito.png")).convert()
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		 

def main():
	exit = False
	clock = pygame.time.Clock()
	#tierra = [[Elementos.Block(w*TILESIZE,h*TILESIZE) for w in range(MAPWIDTH)] for h in range(MAPHEIGHT)]
	#for i in tierra:
	#	for j in i:
	#		j.scale2x()
	
	nivel = Nivel.Nivel()
	nivel.generate()

	while exit == False:
		clock.tick(40)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit = True

			if event.type == pygame.KEYUP:
				nivel.player.nomove()

		screen.fill(pygame.Color("#06095A"))
		nivel.update()
		nivel.draw(screen)

		pygame.display.flip()

	pygame.quit()

if __name__ == "__main__": 
	main()