import pygame
import os.path
from script import Animation

WHITE2 =  (252,252,238)
LEMON = (249,215,0)
GREEN = (140,196,51)

ruta_base =  os.path.abspath("")
ruta_base += "/image/"

class Block(pygame.sprite.Sprite):
	def __init__(self,x = 0,y= 0):
		pygame.sprite.Sprite.__init__(self)
		self.tierra = pygame.image.load(ruta_base + "cespito.png")	
		self.image = self.tierra.subsurface((0,0),(20,20)).convert()
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.vly = 0
		self.vlx = 0
		self.x = x
		self.y = y
	def scale2x(self):
		self.tierra =pygame.transform.scale2x(pygame.image.load(ruta_base +"cespito.png")).convert()
		self.image = self.tierra.subsurface((0,0),(20*2,20*2)).convert()
		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y

class Llave(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		print()
		self.llave =pygame.transform.scale2x( pygame.image.load(ruta_base + "Hugo_Juego.png"))	
		self.pos_inicial = pygame.Rect(	(342*2,111*2),  (3*2,8*2))		
		self.image = self.llave.subsurface(self.pos_inicial)
		self.llave_posx = x
		self.llave_posy = y
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.vlx = 0
		self.vly = 0
	def update(self):
		self.rect.x += self.vlx
		self.rect.y += self.vly

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
		#self.rect.y = y + self.rect.height +20
		self.rect.y = y +22
		self.vlx = 0
		self.vly = 0
		self.activar_animacion= False
		self.animacion = Animation.Animation(len(self.list_frame),(12*2,9*2),self.trampolin)
	def update(self):
		if self.activar_animacion == True:
			self.animacion.limite = 10
			self.image = self.animacion.basic(self.list_frame)
			if self.animacion.frame_current >= self.animacion.frame -1:
				self.activar_animacion = False
		else:
			self.animacion.cont = 0
			self.animacion.frame_current = 0
				
	def jump(self):
		self.vly = 21
		return -(self.vly)


class Puas(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.puas =pygame.transform.scale2x( pygame.image.load(ruta_base + "Hugo_Juego.png")).convert_alpha()
		self.pos_inicial = pygame.Rect(	(330*2,26*2),  (9*2,5*2))		
		self.image = self.puas.subsurface(self.pos_inicial)
		self.rect = self.image.get_rect()
		self.rect.x = x + 10
		self.rect.y = y + self.rect.height + 20

	def update(self):
		pass

class Puerta(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.puerta =pygame.transform.scale2x( pygame.image.load(ruta_base + "Hugo_Juego.png"))
		self.pos_inicial = pygame.Rect(	(356*2,89*2),  (39*2,42*2))		
		self.image = self.puerta.subsurface(self.pos_inicial)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y -40
		self.list_frame = [(356*2,89*2),(408*2,89*2),(510*2,89*2)]
		self.frame_current = 0
		self.activar_animacion= None
		self.animacion = Animation.Animation(len(self.list_frame),(39*2,42*2),self.puerta)

	def update(self):
		
		if self.activar_animacion == True:
			pass

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