import pygame
from script import Collided
from script import Player
from script import Elementos

BORDE_X,BORDE_Y = 400,200
"""BIG ISLAND"""	
map1 =	[
			"##--P#--###-------------------------------------------##",
			"##-E###------------B---------####---------------------##",
			"########---B----#######-----##--##--------------------##",
			"######################################--################",]

class Nivel(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.group_inmovil = pygame.sprite.Group()
		#self.group_trampolin = pygame.sprite.Group()
		#self.group_dead = pygame.sprite.Group()
		self.group_lemones = pygame.sprite.Group()
		self.group_enemy = pygame.sprite.Group()
		self.group_sprites = pygame.sprite.Group()
		#self.group_llaves = pygame.sprite.Group()
		#self.group_puerta = pygame.sprite.Group()
		self.collided = Collided.Collided()
		self.collided_e = Collided.Collided()
		self.cont  = 0
		self.maps = [map1]
		self.map = self.maps[0]
	def update(self):
		self.scroll()				
		self.player.update()
		self.group_inmovil.update()
		self.group_enemy.update()
		self.collided.estaticos(self.player,self.group_inmovil)
		for enemy in self.group_enemy:
			enemy.update()
			self.collided_e.estaticos(enemy,self.group_inmovil)
	
	
	def scroll(self):
		if self.player.rect.x >= BORDE_X:
			diff = self.player.rect.x - BORDE_X 
			self.player.rect.x = BORDE_X
			for plataform in self.group_inmovil:
				plataform.rect.x -=diff
			for enemy in self.group_enemy:
				enemy.pos_patrullandox -= diff 
				enemy.rect.x  -= diff

		if self.player.rect.x <= 200:
			diff =  200 - self.player.rect.x
			self.player.rect.x = 200
			for plataform in self.group_inmovil:
				plataform.rect.x +=diff
			for enemy in self.group_enemy:
				enemy.pos_patrullandox += diff
				enemy.rect.x  += diff
				
	def draw(self,screen):
		self.group_inmovil.draw(screen)
		self.group_enemy.draw(screen)
		screen.blit(self.player.image,self.player.rect)

	def generate(self):
		x = 0
		y = 320

		for i in range(len(self.map)):
			for j in range(len(self.map[0])):

				if self.map[i][j] == "E":
					self.player = None
					j = Player.Player(x,y)
					self.player = j
				elif self.map[i][j] == "#":
					j = Elementos.Block(x,y)
					j.scale2x()
					#self.group_general.add(j)
					self.group_inmovil.add(j)
				elif self.map[i][j] == "X":
					j = Elementos.Puas(x,y)
					self.group_general.add(j)
					self.group_dead.add(j)
				elif self.map[i][j] == "S":
					j = Elementos.Puerta(x,y)
					self.group_puerta.add(j)
					self.group_general.add(j)
					
				elif self.map[i][j] == "-":
					pass  
				elif self.map[i][j] == "P":
					j = Elementos.Lemon(x,y)
					self.group_lemones.add(j)
				elif self.map[i][j] == "L":
					j = Elementos.Llave(x,y)
					self.group_general.add(j)
					self.group_llaves.add(j)
				elif self.map[i][j] == "T":
					j = Elementos.Trampolin(x,y)
					self.group_general.add(j)
					self.group_trampolin.add(j)
				elif self.map[i][j] == "B":	
					j = Player.Enemy(x,y)
					self.group_enemy.add(j)
				elif self.map[i][j] == "N":
					j = Player.NPC(x,y)
					self.group_sprites.add(j)
				x +=40

			x = 0
			y +=40



if __name__ == '__main__':
	main()