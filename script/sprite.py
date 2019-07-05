from script import *

class Sprite(pg.sprite.Sprite):
	def __init__(self):
		pg.sprite.Sprite.__init__(self)
		self.vlx = 0
		self.vly = 0
		self.element = "Sprite"
		self.fuerza_gravitatoria = 0.65
		self.list_lifes = []
		self.diffx = 0

		self.frame_current = 0
		self.step = 0
		self.limit = 7

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

	def animation(self,flip,frames):

		if self.frame_current >= len(frames): self.frame_current = 0


		if flip == True:
			self.image = self.image_a.subsurface(frames[self.frame_current],self.size)
			self.image = pg.transform.flip(self.image,True,False)
		
		elif flip == False: 
			self.image = self.image_a.subsurface(frames[self.frame_current],self.size)				
		
		if self.frame_current < len(frames):
			self.step +=1
			if self.step >= self.limit:
				self.frame_current +=1
				self.step = 0