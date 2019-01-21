import pygame
import os.path
import random
from script import Animation

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


class Key(pygame.sprite.Sprite):
	def __init__(self,x,y,Object):
		pygame.sprite.Sprite.__init__(self)
		self.image =pygame.transform.scale( pygame.image.load(ruta_base + "key.png"),(8,15))	
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.Object = Object

	def update(self):
		if self.rect.colliderect(self.Object.rect):
			print(self.Object.keys['KEY_YELLOW'])
			self.Object.keys['KEY_YELLOW'] = True
			print(self.Object.keys['KEY_YELLOW'])
			self.kill()

class Trampolin(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.trampolin = pygame.transform.scale2x(pygame.image.load( ruta_base + "Hugo_Juego.png"))
		self.list_frame = [(447*2,39*2),(468*2,39*2),(488*2,39*2),(505*2,39*2),(523*2,39*2),(468*2,59*2),
							(486*2,59*2),(503*2,59*2),(523*2,59*2)]
		self.pos_inicial = pygame.Rect(	self.list_frame[0] ,  (13*2,9*2))
		self.image = self.trampolin.subsurface(self.pos_inicial)
		self.frame_current = 0
		self.rect = self.image.get_rect()
		self.rect.x = x 
		self.rect.y = y +22
		self.vlx = 0
		self.vly = 0
		
		self.activar_animacion= False
		self.frame_current = 0
		self.frame = len(self.list_frame)
		self.step = 0
		#self.animacion = Animation.Animation(len(self.list_frame),(13*2,9*2),self.trampolin)

	def update(self):
		self.image = self.trampolin.subsurface(self.list_frame[self.frame_current],(13*2,9*2))
		if self.activar_animacion == True:
			if self.frame_current < self.frame-1:
				self.step +=5
				if self.step >= 10:				
					self.frame_current +=1
					self.step = 0
			else:		
				self.frame_current = 0
				self.activar_animacion = False
		
		

				
	def jump(self):
		self.vly = 21
		return -(self.vly)


class Door(pygame.sprite.Sprite):
	def __init__(self,x,y,Object,Type):
		pygame.sprite.Sprite.__init__(self)
		self.position = 1
		if Type == "YELLOW":
			self.image = pygame.image.load(ruta_base + "door1.png")
		
		self.image = pygame.transform.scale(self.image,(60,62))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y 
		self.Object = Object
		
		self.open = False
		self.cont = 0
		self.delay = 10

		self.next = None

	def update(self):
		if self.rect.colliderect(self.Object.rect):
			if self.Object.keys['KEY_YELLOW'] == True:
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
	main()
