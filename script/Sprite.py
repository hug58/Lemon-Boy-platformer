import pygame as pg
#import script.function_utils as fun
from script import function_utils as fun


class Lifes:
	def __init__(self,x,y):
		self.image = pg.image.load(fun.resolve_route("image/heart1.png"))
		self.image = pg.transform.scale(self.image,(15,15))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.cont = 0

class animation:
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
			self.image = pg.transform.flip(self.image,True,False)
		elif flip == False:
			self.image = self.sheet[self.frame_current]				
		self.image = pg.transform.scale(self.image,(self.scale_x,self.scale_y))

		if self.frame_current < self.frame:
			self.step +=1
			if self.step >= self.limite:
				self.frame_current +=1
				self.step = 0
		if self.frame_current >= self.frame:
			self.frame_current = 0

			
		return self.image

class Sprite(pg.sprite.Sprite):
	def __init__(self):
		pg.sprite.Sprite.__init__(self)
		self.vlx = 0
		self.vly = 0
		self.element = "Sprite"
		self.fuerza_gravitatoria = 0.65
		self.list_lifes = []
		self.diffx = 0

	def collided(self):
		self.rect.x += self.vlx
		self.rect.x += self.diffx
		self.colision_plataform =  pg.sprite.spritecollide(self,self.game.plataform,False)
		self.colision_plataform_m = pg.sprite.spritecollide(self,self.game.plataform_m,False)
		
		if len(self.colision_plataform_m) > 0:
			self.colision_plataform = self.colision_plataform_m
			
		for block in self.colision_plataform:
			if self.vlx > 0:
				#self.cont_jump = 1
				self.rect.right = block.rect.left
			elif self.vlx < 0:
				#self.cont_jump = 1
				self.rect.left = block.rect.right

		self.rect.y +=self.vly
		self.colision_plataform =  pg.sprite.spritecollide(self,self.game.plataform,False) #,pg.sprite.collide_mask)
		self.colision_plataform_m = pg.sprite.spritecollide(self,self.game.plataform_m,False)
		if len(self.colision_plataform_m) > 0:
			self.colision_plataform = self.colision_plataform_m
		
		
		for block in self.colision_plataform:
			if self.vly >= 0:
				self.cont_jump = 2
				self.rect.bottom = block.rect.top
				self.diffx= block.vlx					
				self.direcciony = 1
				self.vly = 0
			elif self.vly < 0:
				self.rect.top = block.rect.bottom

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
