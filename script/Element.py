import pygame
import os.path
import random


WHITE2 =  (252,252,238)
LEMON = (249,215,0)
GREEN = (140,196,51)

ruta_base =  os.path.abspath("")
ruta_base += "/image/"

class Block(pygame.sprite.Sprite):
	def __init__(self,x,y,scale):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(ruta_base +"pasto.png")	
		self.image = pygame.transform.scale(self.image,(scale[0],scale[0]))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.vly = 0
		self.vlx = 0
		self.x = x
		self.y = y

class Trap(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.trap = pygame.image.load(ruta_base + "spikes.png")
		self.frames = 8
		self.image = self.trap.subsurface((0,0),(32,32))
		self.rect = self.image.get_rect()
		self.rect.x = x 
		self.rect.y = y 
		self.mask = pygame.mask.from_surface(self.image)
		self.position = 0
		self.activate = False
		self.activate_spike = False
		self.cont = 0

	def update(self):
		self.animation()

	def animation(self):
		if self.activate == False:
			self.activate_spike = False
			self.image = self.trap.subsurface((32*self.position,0),(32,32)) 
			self.mask = pygame.mask.from_surface(self.image)			
			self.position +=1
			if self.position == self.frames:
				self.activate = True

		else:
			if self.position != 4 and self.position > 0:
				self.position -=1
				self.cont = 0

			elif self.position == 4:
				self.cont +=1
				if self.cont == 35:
					self.position -=1	
			
			elif self.position == 0:
				self.cont +=1
				self.activate_spike = True
				if self.cont == 35:
					self.activate = False

			self.image = self.trap.subsurface((32*self.position,0),(32,32)) 
			self.mask = pygame.mask.from_surface(self.image)	
			
class Key(pygame.sprite.Sprite):
	def __init__(self,x,y,game):
		pygame.sprite.Sprite.__init__(self)
		self.image =pygame.transform.scale( pygame.image.load(ruta_base + "key.png"),(8,15))	
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.game = game

	def update(self):
		if self.rect.colliderect(self.game.player.rect):
			print(self.game.player.keys['KEY_YELLOW'])
			self.game.player.keys['KEY_YELLOW'] = True
			print(self.game.player.keys['KEY_YELLOW'])
			self.kill()

class Trampoline(pygame.sprite.Sprite):
	def __init__(self,x,y,game):
		pygame.sprite.Sprite.__init__(self)
		self.frames = [(0,0),(21,0),(41,0),(58,0),(76,0),(21,20),(39,20),(56,20),(76,20)]
		
		self.tramp = pygame.image.load( ruta_base + "trampoline.png")
		self.image = self.tramp.subsurface(self.frames[0],(13,9))
		self.image = pygame.transform.scale(self.image,(32,32))

		self.rect = self.image.get_rect()
		self.rect.x = x 
		self.rect.y = y 
		
		self.frame = len(self.frames)
		#self.delay = 5
		#self.cont = 0
		self.position = 0

		self.game = game
		self.activate = False

	def update(self):
		if self.rect.colliderect(self.game.player.rect):
			self.activate = True
			self.game.player.vly = self.jump()

		self.animation()

	def animation(self):
		
		if self.activate == True:
			self.image = self.tramp.subsurface(self.frames[self.position],(13,9)) 			
			self.image = pygame.transform.scale(self.image,(32,32))
			self.position +=1
			
			if self.position >= self.frame:
				self.activate = False
			self.cont = 0
				 
		else:
			
			self.position = 0
			self.image = self.tramp.subsurface(self.frames[self.position],(13,9)) 			
			self.image = pygame.transform.scale(self.image,(32,32))

		return self.image
				
	def jump(self, vl = -12):
		return vl

class Door(pygame.sprite.Sprite):
	def __init__(self,x,y,game,Type):
		pygame.sprite.Sprite.__init__(self)
		self.position = 1
		if Type == "YELLOW":
			self.image = pygame.image.load(ruta_base + "door1.png")
		
		self.image = pygame.transform.scale(self.image,(62,64))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y 
		self.game = game
		
		self.open = False
		self.cont = 0
		self.delay = 10

		self.next = None

	def update(self):
		if self.rect.colliderect(self.game.player.rect):
			if self.game.player.keys['KEY_YELLOW'] == True:
				self.open = True

		if self.open == True: 			
			self.image = self.OpenDoor()

	def OpenDoor(self):
		self.cont += 2.5
		if self.cont > self.delay:
			if self.position < 5:					
				self.image = pygame.image.load(ruta_base + "door{}.png".format(self.position)) 			
				self.image = pygame.transform.scale(self.image,(60,62))
				self.position +=1
			elif self.position >= 4:
				self.next = True
				self.position =1

			self.cont = 0 

		return self.image
		
class Lemon(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.lemonsito =pygame.transform.scale2x( pygame.image.load(ruta_base + "Hugo_Juego.png"))
		self.pos = pygame.Rect(	(370*2,52*2),  (13*2,10*2))		
		self.image = self.lemonsito.subsurface(self.pos)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y + self.rect.height
		self.vlx = 0
		self.vly = 0

	def update(self):
		self.rect.x += self.vlx
		self.rect.y += self.vly

if __name__ == '__main__':
	Main()
