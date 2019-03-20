import pygame as pg
import math
from script import Sprite 
from script import function_utils as fun

class Enemy(Sprite.Sprite):
	def __init__(self,game):
		self.game = game
		Sprite.Sprite.__init__(self)
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
		Enemy.__init__(self,game)
		self.frames = [pg.image.load(fun.resolve_route("image/sprites/apple1.png")),
				  pg.image.load(fun.resolve_route("image/sprites/apple2.png") ),
				  pg.image.load(fun.resolve_route("image/sprites/apple3.png")),
				  pg.image.load(fun.resolve_route("image/sprites/apple4.png")),]
				
		self.scale_x = 44
		self.scale_y = 34
		self.image = pg.transform.flip(pg.transform.scale(self.frames[3],(self.scale_x,self.scale_y)),True,False)
		self.mask = pg.mask.from_surface(self.image)	
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.animacion = Sprite.animation(self.frames,self.scale_x,self.scale_y)
		self.animacion.limite = 3
		self.animacion.limite = 7
		self.vl = 4
		self.cont = 0
		self.distanciax = math.sqrt((self.rect.centerx - self.game.player.rect.centerx)**2)		
		self.distanciay = math.sqrt((self.rect.centery - self.game.player.rect.centery)**2)
		
		self.direccionx = 1
	def update(self):
		
		if self.vlx < 0:
			self.direccionx = 1
			self.image = pg.transform.flip(self.animacion.update(True),True,False)

		elif self.vlx > 0:
			self.direccionx = -1
			self.image = pg.transform.flip(self.animacion.update(False),True,False)

		if self.distanciax > 200 or self.distanciay > 100 and self.vlx == 0:
			if self.direccionx < 0:
				self.image = pg.transform.flip(pg.transform.scale(self.frames[3],(self.scale_x,self.scale_y)),True,False)
			elif self.direccionx > 0:
				self.image = pg.transform.scale(self.frames[3],(self.scale_x,self.scale_y))
			
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
