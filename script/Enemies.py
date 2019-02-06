import pygame
import os
import math
import random
from script import Sprite 

ruta_base =  os.path.abspath("")
ruta_base += "/image/"


class Enemy(Sprite.Sprite):
	def __init__(self):
		Sprite.Sprite.__init__(self)
		self.limite_x = 60
		self.vl = 3
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
		self.distancia = math.sqrt(	(	(self.rect.x - self.game.player.rect.x )**2 + (self.rect.y - self.game.player.rect.y)**2	)	)
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


class Skull(Enemy):
	def __init__(self,x,y,game,sentido = True):
		Enemy.__init__(self)
		self.game = game
		self.position = 1 
		self.position_state = 1
		self.sentido = sentido
		
		if self.sentido == False:
			self.image = pygame.image.load(ruta_base + "skulls{}.png".format(self.position)) 
		
		else:
			self.image = pygame.transform.flip(pygame.image.load(ruta_base + "skulls{}.png".format(self.position)),True,False)	 


		self.image = self.image.subsurface((5,13),(27,27))
		self.image = pygame.transform.scale(self.image,(40,40))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.distancia = None
		self.delay = 20
		self.cont = 0
		self.cont_bullet = 0
		
		
	def update(self):
		#self.seguimiento()
		self.gravity()
		self.rect.x += self.vlx
		self.rect.y += self.vly
		self.seguimiento()
		self.collided()
			
	def seguimiento(self):
		self.distancia = math.sqrt(	(	(self.game.player.x - self.rect.x )**2 + (self.game.player.y - self.rect.y)**2	)	)
		self.cont += 5
		if self.distancia < 250:			
			if self.cont >= self.delay:		
				if self.position <= 4:
					
					if self.sentido == False:
						self.image = pygame.image.load(ruta_base + "skulls{}.png".format(self.position)) 
					elif self.sentido == True:
						self.image = pygame.transform.flip(pygame.image.load(ruta_base + "skulls{}.png".format(self.position)),True,False) 

					self.image = self.image.subsurface((5,13),(27,27))
					self.image = pygame.transform.scale(self.image,(40,40))

					self.position +=1
					self.cont = 0
					self.cont_bullet = 0
				else:
					self.cont_bullet += 0.45
					if self.cont_bullet > 10:	
						#self.bullet.add(Bullet.Bullet(self.rect.x,self.rect.y-2))
						self.cont_bullet = 0
		else:	
			if self.cont >= self.delay:
				if self.position > 1:				
					self.position -=1
					if self.sentido == False:
						self.image = pygame.image.load(ruta_base + "skulls{}.png".format(self.position)) 
					elif self.sentido == True:
						self.image = pygame.transform.flip(pygame.image.load(ruta_base + "skulls{}.png".format(self.position)),True,False) 
					
					self.image = self.image.subsurface((5,13),(27,27))
					self.image = pygame.transform.scale(self.image,(40,40))

					self.cont = 0
				else:
					self.fijo()			
	def fijo(self):
			if self.position_state < 5:		
				
				if self.sentido == False:
					self.image = pygame.image.load(ruta_base + "skulls{}.png".format(self.position)) 
				elif self.sentido == True:
					self.image = pygame.transform.flip(pygame.image.load(ruta_base + "skulls{}.png".format(self.position)),True,False)  
				
				self.image = self.image.subsurface((5,13),(27,27))
				self.image = pygame.transform.scale(self.image,(40,40))

				self.position_state +=1
				self.cont = 0
			elif self.position_state >= 4:
				self.position_state =1 

	def cannon(self):
		#print(len(self.group_bullet))
		for bullet in self.bullet:
			if bullet.rect.x <= 0:
				bullet.kill()

class Lord_of_the_flies(Enemy):
	def __init__(self,x,y,group):
		Enemy.__init__(self)
		self.position = 1 
		self.image = pygame.image.load(ruta_base + "/sprites/belcebu/belcebu{}.png".format(self.position))
		self.image = pygame.transform.scale(self.image,(40,80))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.vlx = 0
		self.vly = 0
		self.group = group
		self.delay = 20
		self.cont = 0

	def update(self):
		self.cont +=10
		if self.cont >= self.delay:
			if self.position < 5:		
				self.image = pygame.image.load(ruta_base + "/sprites/belcebu/belcebu{}.png".format(self.position)) 
				self.image = pygame.transform.scale(self.image,(40,80))
				self.position +=1
			elif self.position >= 4:
				self.position =1 
			
			self.cont = 0
		
		self.gravity()
		self.collided()

class Apple(Enemy):
	def __init__(self,x,y,game,sentido):#player):
		Enemy.__init__(self)
		frames = [pygame.image.load(ruta_base + "sprites/apple1.png"),
				  pygame.image.load(ruta_base + "sprites/apple2.png"),
				  pygame.image.load(ruta_base + "sprites/apple3.png"),
				  pygame.image.load(ruta_base + "sprites/apple4.png"),]
				
		self.scale_x = 32
		self.scale_y = 22
		self.image = pygame.transform.flip(pygame.transform.scale(frames[0],(self.scale_x,self.scale_y)),True,False)
		self.mask = pygame.mask.from_surface(self.image)	
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.animacion = Sprite.animation(frames,self.scale_x,self.scale_y)
		self.animacion.limite = 3
		self.game = game
		self.pos_patrullandox = self.rect.x

		self.vl = 2 if sentido == "left" else -2
		
	def update(self):

		if self.vlx < 0:
			self.animacion.limite = 10
			self.image = pygame.transform.flip(self.animacion.update(True),True,False)
			self.mask = pygame.mask.from_surface(self.image)	

		if self.vlx > 0:
			self.image = pygame.transform.flip(self.animacion.update(False),True,False)
			self.mask = pygame.mask.from_surface(self.image)	
		
		self.patroling()
		#self.follow()
		self.gravity()
		self.collided()

