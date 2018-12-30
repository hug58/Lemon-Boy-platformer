import pygame
import os.path
import math
from script import Animation
ANCHO,ALTO = 1000,700
CANDY = (252,156,238)
RED = pygame.Color("#C65065")
ruta_base =  os.path.abspath("")
ruta_base += "/image/"

"""
	LEMON BOY 	"""

"""TANGERINE BOY """

"""GRIPE GIRL
"""


"""
Mi chico agrio es un dolor

"""

"""
Juliet, mi niña epecial

"""


class Player(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.hoja_sprites = pygame.image.load(ruta_base +"Hugo_Juego.png").convert_alpha()
		self.frame_estatico = pygame.Rect(	(169,45),  (16,29))
		self.pedazo_frame = self.hoja_sprites.subsurface(self.frame_estatico).convert_alpha()
		self.list_frame = [(273,153),(310,153),(344,153)]
		self.list_frame_dead = [(184,106),(226,106),(265,106)]
		self.frame_salto = pygame.Rect(	(234,45), (16,29)	)		
		self.run = Animation.Animation(len(self.list_frame),(16,29),self.hoja_sprites,lados = self.frame_estatico)
		self.dead_hug = Animation.Animation(len(self.list_frame_dead),(25,14),self.hoja_sprites)
		self.image = self.pedazo_frame
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y -self.rect.height
		self.vly = 0
		self.vlx = 0
		self.direccionx = 1
		self.direcciony = 0
		self.llave = False
		self.dead = False
		self.reset_automatico = False
		self.initial_x,self.initial_y = x,y
		self.state = 1
		self.detener = False
		self.fuerza_gravitatoria = 2.0
	
	def update(self):
		if self.state == 0:
				self.vlx = 0
				self.image =self.transform.basic(self.list_transform,3)
				if self.transform.cont >= 3:
					self.state = 2
		if self.state == 1:
			if self.dead == False:
				self.image = self.run.sprites(self.vlx,self.vly,self.direccionx,self.list_frame,self.frame_salto)
				self.move()
			else:
				self.image = self.dead_hug.basic(self.list_frame_dead,4)
				if self.dead_hug.cont >= 4:
					self.reset_automatico = True
					self.dead_hug.cont = 0
			
		if self.vlx >= 10:
			self.vlx = 10
		elif self.vlx <= -10:
			self.vlx = -10	
		if self.detener == True:
			if self.vlx > 0:
				self.vlx -=1
			elif self.vlx < 0:
				self.vlx +=1
			else:
				self.detener = False
		self.gravity()
		self.rect.y +=self.vly
		self.rect.x += self.vlx
	
	def move(self):
		pulsar = pygame.key.get_pressed()
		if pulsar[pygame.K_LEFT]:
			self.direccionx = -1
			self.vlx -=1  			
			self.detener = False
		if pulsar[pygame.K_RIGHT]:
			self.direccionx = 1
			self.vlx += 1			
			self.detener = False
		if pulsar[pygame.K_SPACE]:
			self.jump()

	def jump(self):
		if	self.rect.y >= ALTO or self.vly == 0:
			self.vly = -15
		
	def nomove(self):
		self.detener = True	
	
	def gravity(self):
		if self.vly == 0:
			self.vly = 1
		if self.vly < 20:
			self.vly += self.fuerza_gravitatoria
		if self.rect.bottom >= ALTO:
			self.vly = 0
			self.rect.bottom = ALTO
		
				
class Enemy(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.hoja_sprite = pygame.image.load(ruta_base + "enemy.png").convert_alpha()
		self.frame_dinamico = [(8,38),(40,38), (72,38)] 
		self.frame_estatico = pygame.Rect((8,38),(14,24))
		self.list_frame = 	  [(8,6),(40,6),(72,6),(104,6),(136,6),(168,6),(200,6),(232,6)]
		self.frame_salto = pygame.Rect(	(234,45), (16,29)	)
		self.pedazo_frame = self.hoja_sprite.subsurface(self.frame_estatico)
		self.image = self.pedazo_frame		
		self.reposo = Animation.New_Animation(self.frame_dinamico,self.hoja_sprite,(14,24))
		self.run = Animation.New_Animation(self.list_frame,self.hoja_sprite,(14,24))
		self.dead = False
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.vlx = 0
		self.vly = 0
		self.direccionx = 1
		self.direcciony = 0
		self.fuerza_gravitatoria = 2.0
		self.player = None
		self.sentido = True
		self.pos_patrullandox = self.rect.x
		self.limitex = 30
			
	def update(self):
		if self.dead == False:
			self.patrullando()					
		else:
			self.kill()
		if self.vlx == 0:
			if self.direccionx > 0:
				self.image = self.reposo.update(True)
			elif self.direccionx < 0:
				self.image = self.reposo.update(False)
		elif self.vlx > 0:
			self.image = self.run.update(True)
		elif self.vlx < 0:
			self.image = self.run.update(False)
		self.gravity()
		self.rect.x += self.vlx
		self.rect.y += self.vly
	
	def jump(self):
		if	self.rect.bottom >= ALTO or self.vly == 0:
			self.vly = -13
	def seguir(self):
		self.distancia = math.sqrt(	(	(self.rect.x - self.player.rect.x )**2 + (self.rect.y - self.player.rect.y)**2	)	)
		if self.distancia < 200:
			if self.rect.x < self.player.rect.x:
				self.direccionx = 1
				self.vlx =3
			elif self.rect.x > self.player.rect.x:
				self.direccionx = -1
				self.vlx =-3
			else:
				self.vlx = 0
		else:
			self.vlx = 0

	def patrullando(self):
		if self.sentido == True:
			if self.rect.x < self.pos_patrullandox + self.limitex:
				self.vlx = 3
			else:
				self.sentido = False 
		elif self.sentido == False:
			if self.rect.x > self.pos_patrullandox -self.limitex:
				self.vlx = -3
			else:
				self.sentido = True


	def gravity(self):

		if self.vly == 0:
			self.vly = 1

		elif self.vly < 20:
			self.vly += self.fuerza_gravitatoria


class NPC(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.troso = pygame.image.load(ruta_base + "mango_men")
		
		self.image = self.troso.subsurface((10,4),(11,24))
		self.rect = self.image.get_rect()
		self.rect.x = x 
		self.rect.y = y +self.rect.height

	def update(self):
		pass

if __name__ == '__main__':
	main()