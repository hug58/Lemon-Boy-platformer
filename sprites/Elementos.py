import pygame
import os
from sprites import Animation

WHITE2 =  (252,252,238)
LEMON = (249,215,0)
GREEN = (140,196,51)

class Block(pygame.sprite.Sprite):
	#Pos = Tupla x e y
	#trozo = tamaño
	def __init__(self,posx,posy,trozo,pos):
		pygame.sprite.Sprite.__init__(self)
		self.tierra = pygame.image.load(os.path.abspath("sprites") + "/image/tierra2.0.png")
		#self.color = WHITE2
		self.trozo = trozo
		self.image = self.tierra.subsurface(pos,self.trozo)
		self.rect = self.image.get_rect()
		#self.add(group)
		self.rect.x = posx
		self.rect.y = posy
		self.vly = 0
		self.vlx = 0
		self.pos = pos	
		self.x = posx
		self.y = posy
		self.arrastrar = False
		
		
	def update(self):
		pass
	
	def scale2x(self):
		self.tierra =pygame.transform.scale2x(pygame.image.load(os.path.abspath("sprites") + "/image/tierra2.0.png"))
		self.image = self.tierra.subsurface(self.pos,self.trozo)
		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y
		

	"""ALFHA DESTRUIR

		CREAR UNA CLASE DESTRUIR-COSTRUIR(?)

						"""
	def destruir(self,parar,group,group2,group_temporal):
		
		if parar == False:
			self.cont_destruccion +=1
			if self.cont_destruccion ==4:
				self.destruido = True
				self.group = group
				self.add(group_temporal)
				self.group2 = group
				self.remove(group,group2)
				self.cont_destruccion = 0	

class Block_big(Block):
	def __init__(self,group,posx,posy,width,vert = None,hor = None,vl = 3):
		Block.__init__(self,posx,posy,width)
		self.image = pygame.Surface((60,20))
		self.image.fill(GREEN)
		self.add(group)
		self.vly = 0
		self.vlx = 0
		self.vl = vl
		self.vert = vert
		self.hor = hor

		self.limitey = 140
		self.limitex = 100
		self.pos_inicio_y = posy
		self.pos_inicio_x = posx

		self.activar = False

	def update(self):
		self.rect.y += self.vly
		self.rect.x += self.vlx

		if self.activar == True:
			self.vertical()
			self.horizontal()


	def vertical(self):

		if self.vert:
			if self.rect.y <= self.pos_inicio_y-self.limitey:
				self.vly =self.vl
			elif self.rect.y >= self.pos_inicio_y:
				self.vly = -self.vl

		elif self.vert == False:
			if self.rect.y >= self.pos_inicio_y + self.limitey:
				self.vly = -self.vl
			elif self.rect.y <= self.pos_inicio_y:
				self.vly = self.vl 
		else:
			pass

	def horizontal(self):
		if self.hor:
			if self.rect.x <= self.pos_inicio_x-self.limitex:
				self.vlx = self.vl
			elif self.rect.x >= self.pos_inicio_x:
				self.vlx =  -self.vl
		elif self.hor == False:
			if self.rect.x >= self.pos_inicio_x + self.limitex:
				self.vlx = -self.vl
			elif self.rect.x <= self.pos_inicio_x:
				self.vlx = self.vl 
		else:
			pass

class Llave(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		print()
		self.llave =pygame.transform.scale2x( pygame.image.load(os.path.abspath("sprites") + "/image/Hugo_Juego.png"))
		
		
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
	def sound(self):
		pass

class Trampolin(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.trampolin = pygame.image.load(os.path.abspath("sprites") + "/image/Hugo_Juego.png")
		self.list_frame = [(447,39),(468,39),(488,39),(505,39),(523,39),(468,59),(486,59),(503,59),(523,59)]
		self.pos_inicial = pygame.Rect(	self.list_frame[0] ,  (13,9))
		self.image = self.trampolin.subsurface(self.pos_inicial)
		self.frame_current = 0
		self.rect = self.image.get_rect()
		self.rect.x = x + 10
		self.rect.y = y + self.rect.height + 20
		self.vlx = 0
		self.vly = 0
		self.activar_animacion= False
		self.animacion = Animation.Animation(len(self.list_frame),(12,9),self.trampolin)
	
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
		self.puas =pygame.transform.scale2x( pygame.image.load(os.path.abspath("sprites") + "/image/Hugo_Juego.png"))
		self.pos_inicial = pygame.Rect(	(330*2,26*2),  (9*2,5*2))		
		self.image = self.puas.subsurface(self.pos_inicial)
		self.rect = self.image.get_rect()
		self.rect.x = x + 10
		self.rect.y = y + self.rect.height + 20

	def update(self):
		pass
		#self.image.fill((255,255,255))

class Puerta(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.puerta =pygame.transform.scale2x( pygame.image.load(os.path.abspath("sprites") + "/image/Hugo_Juego.png"))
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
			self.image = self.animacion.basic(self.list_frame,0)
			if self.animacion.cont >= 3:
				self.image = self.puerta.subsurface(self.pos_inicial)		
				self.activar_animacion = False

"""
Si los enemigos lo agarran:
	esprimir lemon
					"""

class Lemon(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.lemonsito =pygame.transform.scale2x( pygame.image.load(os.path.abspath("sprites") + "/image/Hugo_Juego.png"))
		self.pos = pygame.Rect(	(370*2,52*2),  (13*2,10*2))		
		self.image = self.lemonsito.subsurface(self.pos)
		
		self.rect = self.image.get_rect()
		self.rect.x = x

		#un cuadro de tierra mide de largo 40px, el lemon 20px, si le sumo 20px a la pos y (empieza desde el top del objeto), en total da igual
		self.rect.y = y + self.rect.height

		#self.list_frame = []
		#self.frame_current = 0
		#self.step = 0

		#self.add(group)

		self.vlx = 0
		self.vly = 0

	def update(self):

		self.rect.x += self.vlx
		self.rect.y += self.vly


	def animacion(self):
		pass


	def activate(self):
		pass
		
#def polygono(VENTANA):
#	poly = pygame.draw.polygon(VENTANA,LEMON,[(200,100),(210,90),(230,90),(240,100),(230,110),(210,110)])
#def ellipse(VENTANA,posx,posy):
#	pygame.draw.ellipse(VENTANA,LEMON,(posx,posy,10,10))
