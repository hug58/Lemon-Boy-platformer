import pygame
import os

ruta_base =  os.path.abspath("")
ruta_base += "/image/"


class Lifes:
	def __init__(self,x,y):
		self.image = pygame.image.load(ruta_base + "heart1.png")
		self.image = pygame.transform.scale(self.image,(15,15))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.cont = 0

class animation():
	def __init__(self,sheet,scale_x,scale_y):
		self.frame_current = 0
		self.step = 0
		self.sheet = sheet
		self.frame = len(self.sheet)
		self.scale_x = scale_x
		self.scale_y = scale_y
		self.limite = 6
		
	def update(self,flip):
		
		if flip == True:
			self.image = self.sheet[self.frame_current] 
			self.image = pygame.transform.flip(self.image,True,False)
		elif flip == False:
			self.image = self.sheet[self.frame_current]				
		self.image = pygame.transform.scale(self.image,(self.scale_x,self.scale_y))

		if self.frame_current < self.frame:
			self.step +=1
			if self.step >= self.limite:
				self.frame_current +=1
				self.step = 0
		if self.frame_current >= self.frame:
			self.frame_current = 0
		return self.image

class Sprite(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.vlx = 0
		self.vly = 0
		self.element = "Sprite"
		self.fuerza_gravitatoria = 1.3
		self.list_lifes = []

	def collided(self):
		self.rect.x += self.vlx
		
		self.colision =  pygame.sprite.spritecollide(self,self.game.plataform,False)
		for block in self.colision:
			if self.vlx > 0:
				#self.cont_jump = 1
				self.rect.right = block.rect.left
			elif self.vlx < 0:
				#self.cont_jump = 1
				self.rect.left = block.rect.right

		self.rect.y +=self.vly
		self.colision =  pygame.sprite.spritecollide(self,self.game.plataform,False) #,pygame.sprite.collide_mask)
		for block in self.colision:
			if self.vly >= 0:
				self.cont_jump = 1
				self.rect.bottom = block.rect.top
				self.direcciony = 1
				self.vly = 0
			elif self.vly < 0:
				self.rect.top = block.rect.bottom

		#for objeto in self.colision:
			#if objeto.element == "block":	
				#if (self.rect.top < objeto.rect.top and self.rect.bottom < objeto.rect.bottom and	self.rect.left < objeto.rect.right 
				#and self.rect.right > objeto.rect.left  and self.vly  >= 0 
				#or self.rect.top < objeto.rect.top and self.rect.bottom < objeto.rect.bottom and self.rect.right > objeto.rect.left 
				#and self.rect.left < objeto.rect.right and self.vly >= 0):	
				#			self.vly = 0			
				#			self.rect.bottom = objeto.rect.top 				
				#			self.cont_jump =2
				#elif self.rect.left < objeto.rect.left:
				#	self.rect.right = objeto.rect.left 		
				#elif self.rect.right > objeto.rect.right:
				#	self.rect.left = objeto.rect.right 
				#elif self.rect.bottom >= objeto.rect.bottom:
				#	self.rect.top = objeto.rect.bottom
				#	self.cont_jump = 0
			#if objeto.element == "pua":
			#	self.vlx = 0
			#	self.vly = 0
			#	self.dead = True
			#	self.rect.bottom = objeto.rect.top +27
			#if objeto.element == "skull" or objeto.element == "enemy":
			#	self.vlx = 0
			#	self.vly = 0
			#	self.dead = True

	def collided_trap(self):
		for sprite in self.game.trap:
			colision = pygame.sprite.collide_mask(self.game.player,sprite)
			if colision != None and sprite.activate_spike == True:
				self.game.player.dead = True
				#return True

		for enemy in self.game.enemies:
			colision = pygame.sprite.collide_mask(self.game.player,enemy)
			if colision != None:
				self.game.player.dead = True



	def gravity(self):
		if self.vly == 0:
			self.vly = 1
		elif self.vly < 8:
			self.vly += self.fuerza_gravitatoria


	def life(self):
		if self.lifes < len(self.list_lifes) and len(self.list_lifes) > 0:
			self.list_lifes.pop()
		elif self.lifes > len(self.list_lifes):
			self.list_lifes.append(Lifes(self.list_lifes[-1].x +20,self.list_lifes[-1].y) )


