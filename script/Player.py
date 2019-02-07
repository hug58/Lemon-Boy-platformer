import pygame
import os.path
from script import Sprite

ruta_base =  os.path.abspath("")
ruta_base += "/image/"

ruta_sound = os.path.abspath("")
ruta_sound += "/sound/"

class Player(Sprite.Sprite):
	def __init__(self,x,y,game):
		Sprite.Sprite.__init__(self)
		self.state = [	pygame.image.load(ruta_base + "sprites/hug/hug0.png"),
						pygame.image.load(ruta_base + "sprites/hug/hug1.png"),
																			]
		
		self.walk = [	
						pygame.image.load(ruta_base + "sprites/hug/hug2.png"),
						pygame.image.load(ruta_base + "sprites/hug/hug3.png"),													
						pygame.image.load(ruta_base + "sprites/hug/hug4.png"),
						pygame.image.load(ruta_base + "sprites/hug/hug5.png"),												
																				]

		self.jump = [	pygame.image.load(ruta_base + "sprites/hug/hug6.png"),
																				]


		self.activate_jump = False

		self.animation_state = Sprite.animation(self.state,32,52)
		self.animation_walk = Sprite.animation(self.walk,32,52)


		self.image = self.state[0]
		self.mask = pygame.mask.from_surface(self.image)
		self.rect = pygame.Rect((x,y),(25,52))
		#self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y 
		self.vly = 0
		self.vlx = 0
		
		self.direccionx = 1
		self.direcciony = 0
		self.dead = None
		self.detener = False
		self.fuerza_gravitatoria = 0.65
		self.game = game
		self.cont_jump = 2
		self.keys = {	'KEY_YELLOW': False,'KEY_BLUE': False,
						'KEY_RED': False,
					}
		
		self.lifes = 3
		self.list_lifes = [Sprite.Lifes(column*25,10) for column in range(self.lifes)]
		self.sound_jump = pygame.mixer.Sound(ruta_sound + "Jump.wav")

	def update(self):
		#print(self.vly)
		if self.vlx == 0:
			self.animation_state.limite = 10
			if self.direccionx > 0:
				self.image = self.animation_state.update(False)
			if self.direccionx < 0:
				self.image = self.animation_state.update(True)
		
		elif self.vlx > 0:
			self.image = self.animation_walk.update(False) 

		elif self.vlx < 0:
			self.image = self.animation_walk.update(True)

		if self.direcciony < 0:	
			if self.direccionx > 0:
				self.image = self.jump[0]
		
			else:
				self.image = pygame.transform.flip(self.jump[0],1,0)

		self.mask = pygame.mask.from_surface(self.image)


		self.move()
		self.life()
			
		if self.vlx >= 5:
			self.vlx = 5
		elif self.vlx <= -5:
			self.vlx = -5	
		if self.detener == True:
			if self.vlx > 0:
				self.vlx -=1
			elif self.vlx < 0:
				self.vlx +=1
			else:
				self.detener = False

		self.gravity()
		self.collided()
		self.collided_trap()

	def move(self):
		pulsar = pygame.key.get_pressed()
		if pulsar[pygame.K_LEFT]:
			self.direccionx = -1
			self.vlx +=-1  			
			self.detener = False
		if pulsar[pygame.K_RIGHT]:
			self.direccionx = 1
			self.vlx += 1			
			self.detener = False			

	#def func_jump(self):
	#	
	#	if self.cont_jump > 0:		
	#		self.vly -=4
	#		
	#		if self.vly >= -4:
	#			self.sound_jump.play()
	#		if self.vly <= -8:
	#			self.cont_jump -=1
	#	else:
	#		self.activate_jump = False
	#	self.direcciony = -1

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

