import pygame
import os.path
from script import Animation
from script import Sprite
ANCHO,ALTO = 1000,700
CANDY = (252,156,238)
RED = pygame.Color("#C65065")
ruta_base =  os.path.abspath("")
ruta_base += "/image/"



class Player(Sprite.Sprite):
	def __init__(self,x,y,group):
		Sprite.Sprite.__init__(self)
		 
		self.hoja_sprites = pygame.image.load(ruta_base +"Hugo_Juego.png")
		self.frame_estatico = pygame.Rect(	(169,45),  (16,29))
		self.pedazo_frame = self.hoja_sprites.subsurface(self.frame_estatico)
		self.list_frame = [(273,153),(310,153),(344,153)]
		self.frame_salto = pygame.Rect(	(234,45), (16,29)	)		
		self.run = Animation.Animation(len(self.list_frame),(16,29),self.hoja_sprites,lados = self.frame_estatico)
		self.image = self.pedazo_frame
		#self.mask = pygame.mask.from_surface(self.image)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y -self.rect.height
		self.vly = 0
		self.vlx = 0
		self.direccionx = 1
		self.direcciony = 0
		self.dead = False
		self.detener = False
		self.fuerza_gravitatoria = 1.6
		self.group = group
		self.cont_jump = 2
		self.keys = {	'KEY_YELLOW': False,'KEY_BLUE': False,
						'KEY_RED': False,
					}
		
		self.lifes = 3
		self.list_lifes = [Sprite.Lifes(column*25,10) for column in range(self.lifes)]

	def update(self):
		
		self.image = self.run.sprites(self.vlx,self.vly,self.direccionx,self.list_frame,self.frame_salto)
		#self.mask = pygame.mask.from_surface(self.image)
		self.move()
		self.life()
			
		if self.vlx >= 7:
			self.vlx = 7
		elif self.vlx <= -7:
			self.vlx = -7	
		if self.detener == True:
			if self.vlx > 0:
				self.vlx -=1
			elif self.vlx < 0:
				self.vlx +=1
			else:
				self.detener = False
						
		self.gravity()
		self.collided()

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

def main():
	pass

if __name__ == '__main__':
	main()
