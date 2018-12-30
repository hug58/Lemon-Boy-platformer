import pygame
import os



LEMON = (249,215,0)


class Lemon(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.lemonsito =pygame.transform.scale2x( pygame.image.load(os.path.abspath("sprites") + "/image/Hugo_Juego.png"))		
		self.pos = pygame.Rect(	(370*2,52*2),  (13*2,10*2))	
		self.image = self.lemonsito.subsurface(self.pos)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y


	def update(self):
		pass

	def draw(self,VENTANA):
		VENTANA.blit(self.image,self.rect)



class Barra():
	def __init__(self,lifes):
		self.lifes = lifes
		self.limones = 0
		self.puntaje  = 0
		self.pos1 = (0,0)
		self.group_lemones = pygame.sprite.Group()
		#self.lemones = Lemon(120,10)

	def restablecido(self):
		cont = 120
		if len(self.group_lemones) < self.lifes:
			for lemones in range(self.lifes):
				lemones = Lemon(cont,10)
				self.group_lemones.add(lemones)
				cont +=21


	

	
	def draw(self,VENTANA):
		fuente = pygame.font.Font("Pixel Digivolve.otf",35)
		texto1 = fuente.render("VIDAS:  ",0,LEMON)
		self.group_lemones.draw(VENTANA)
		VENTANA.blit(texto1,self.pos1)


		