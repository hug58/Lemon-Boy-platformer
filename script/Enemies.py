import pygame
import os
import math
import random
from script import Sprite 

ruta_base =  os.path.abspath("")
ruta_base += "/image/"

class Enemy(Sprite.Sprite):
	def __init__(self,game):
		self.game = game
		Sprite.Sprite.__init__(self)
		self.limite_x = 60
		self.vl = 4

	def patroling(self):
		if self.vl > 0:
			if self.rect.x < self.pos_patrullandox + self.limite_x:
				self.vlx = self.vl
			else:
				self.vl *=-1 
		elif self.vl < 0:
			if self.rect.x > self.pos_patrullandox -self.limite_x:
				self.vlx = self.vl
			else:
				self.vl *=-1

	def follow(self):
		self.distancia = math.sqrt(	(	(self.rect.centerx - self.game.player.rect.centerx )**2 + (self.rect.centery - self.game.player.rect.centery)**2	)	)
		if self.distancia < 200:
			if self.game.player.rect.left < self.rect.left:
				self.vlx = -self.vl
			elif self.game.player.rect.right > self.rect.right:
				self.vlx = self.vl
			
			if self.game.player.rect.left == self.rect.right or self.game.player.rect.right == self.rect.left:
				self.vlx = 0

		else:
			self.vlx = 0

class Enemy_Rect(Enemy):
	def __init__(self,x,y,group):
		Enemy.__init__(self)
		self.image = pygame.Surface((20,20))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.vlx = -3
		self.vly = 0
		self.group = group
		self.pos_patrullandox = self.rect.x
		
	def update(self):
		self.gravity()
		self.patroling()
		self.collided()

class Apple(Enemy):
	def __init__(self,x,y,game,sentido):
		Enemy.__init__(self,game)
		self.frames = [pygame.image.load(ruta_base + "sprites/apple1.png"),
				  pygame.image.load(ruta_base + "sprites/apple2.png"),
				  pygame.image.load(ruta_base + "sprites/apple3.png"),
				  pygame.image.load(ruta_base + "sprites/apple4.png"),]
				
		self.scale_x = 44
		self.scale_y = 34
		self.image = pygame.transform.flip(pygame.transform.scale(self.frames[0],(self.scale_x,self.scale_y)),True,False)
		self.mask = pygame.mask.from_surface(self.image)	
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.animacion = Sprite.animation(self.frames,self.scale_x,self.scale_y)
		self.animacion.limite = 3
		#self.pos_patrullandox = self.rect.x
		self.animacion.limite = 7
		#self.vl = 3 if sentido == "left" else -3
		self.vl = 4
		self.cont = 0
		self.distancia = math.sqrt(	(	(self.rect.centerx - self.game.player.rect.centerx )**2 + (self.rect.centery - self.game.player.rect.centery)**2	)	)
		self.direccionx = 1
	def update(self):

		if self.vlx < 0:
			self.direccionx = 1
			self.image = pygame.transform.flip(self.animacion.update(True),True,False)

		elif self.vlx > 0:
			self.direccionx = -1
			self.image = pygame.transform.flip(self.animacion.update(False),True,False)

		if self.distancia > 200 or self.vlx == 0:
			if self.direccionx > 0:
				self.image = pygame.transform.flip(pygame.transform.scale(self.frames[3],(self.scale_x,self.scale_y)),True,False)
			elif self.direccionx < 0:
				self.image = pygame.transform.scale(self.frames[3],(self.scale_x,self.scale_y))

			
		self.mask = pygame.mask.from_surface(self.image)

		#self.jump()
		#self.patroling()
		self.follow()
		self.gravity()
		
		self.collided()

	def jump(self):
		self.cont +=1
		if self.cont > 30:
			self.vly = -10
			self.cont = 0
