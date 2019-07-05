import math
from script import *
from script.sprite import Sprite

class Enemy(Sprite):
	def __init__(self,game):
		self.game = game
		Sprite.__init__(self)
		self.limite_x = 60
		self.vl = 4
		
	def follow(self):
		
		self.distanciax = math.sqrt((self.rect.centerx - self.game.player.rect.centerx)**2)
		self.distanciay = math.sqrt((self.rect.centery - self.game.player.rect.centery)**2)
		if self.distanciax < 200 and self.distanciay <= 100:
			if self.game.player.rect.left < self.rect.left:
				self.vlx = -self.vl
			elif self.game.player.rect.right > self.rect.right:
				self.vlx = self.vl
	
		else:
			self.vlx = 0

	def collided_player(self):
		colision = pg.sprite.collide_mask(self.game.player,self)
		if colision != None:
			self.game.player.dead = True

class Apple(Enemy):
	def __init__(self,x,y,game,sentido):
		self.frames = { 0:(0,0), 1:(0,12), 2:(0,24), 3:(0,36), }
		self.size = (12,12)

		self.image_a = image["apple"]
		self.image = self.image_a.subsurface(self.frames[3],(12,12))
		self.image = pg.transform.flip(pg.transform.scale(self.image,(34,34)),1,0)

		Enemy.__init__(self,game)


		self.mask = pg.mask.from_surface(self.image)	
		self.rect = pg.Rect((x,y),self.image.get_size())

		self.vl = 4
		self.cont = 0

		self.distanciax = math.sqrt((self.rect.centerx - self.game.player.rect.centerx)**2)		
		self.distanciay = math.sqrt((self.rect.centery - self.game.player.rect.centery)**2)
		
		self.direccionx = 1

	def rotate(self):
		
		if self.vlx < 0:
			self.direccionx = 1
			self.animation(False,self.frames)

		elif self.vlx > 0:
			self.direccionx = -1
			self.animation(True,self.frames)
			
		self.image = pg.transform.scale(self.image,(34,34))

	def update(self):

		self.rotate()

		if self.distanciax > 200 or self.distanciay > 100 and self.vlx == 0:
			if self.direccionx < 0:
				self.image = pg.transform.flip(pg.transform.scale(self.image_a.subsurface(self.frames[3],(12,12)),(34,34)),1,0)
			elif self.direccionx > 0:
				self.image = pg.transform.scale(self.image_a.subsurface(self.frames[3],(12,12)),(34,34))
			
		self.mask = pg.mask.from_surface(self.image)

		self.follow()
		self.gravity()
		self.collided()
		self.collided_player()

	def jump(self):
		self.cont +=1
		if self.cont > 30:
			self.vly = -10
			self.cont = 0