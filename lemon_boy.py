import pygame as pg
import os, pytmx, sys,math,os.path
import pytweening as tween


pg.display.init()
pg.mixer.init()
pg.joystick.init()
pg.font.init()

WIDTH = 620
HEIGHT = 480

WHITE2 =  (252,252,238)
LEMON = (249,215,0)
GREEN = (140,196,51)


SCREEN = pg.display.set_mode((WIDTH,HEIGHT))


def resolve_route(route_relative):
	#if hasattr(sys,"_MEIPASS"):
	#	return os.path.join(sys._MEIPASS,route_relative)
	return os.path.join(os.path.abspath("."),route_relative)

pg.display.set_caption("Project Hugo")

pg.display.set_icon(pg.image.load(resolve_route("lemon.ico") ))
 

image = {
	"background": pg.image.load(resolve_route("image/background.png")),
	"lemon": pg.image.load(resolve_route("image/lemon.png")),
	"hugo": pg.image.load(resolve_route("image/hug.png")),
	"paty": pg.image.load(resolve_route("image/paty.png")),
	"plataform_movil": pg.image.load(resolve_route("image/plataform.png")),
	"spikes": pg.image.load(resolve_route("image/spikes.png")),
	"key": pg.image.load(resolve_route("image/key.png")),
	"trampoline": pg.image.load( resolve_route("image/trampoline.png")),
	"door": pg.image.load(resolve_route("image/door.png")),
	"fireball": pg.image.load(resolve_route("image/fireball.png")),
	"apple": pg.image.load(resolve_route("image/apple.png")),
	"dead": pg.image.load(resolve_route("image/dead.png")),
	"arrow": pg.image.load(resolve_route("image/arrow.png")),

 }


sound = {	
	
	"jump": pg.mixer.Sound(resolve_route("sound/Jumpa.wav")),
	"arrow": pg.mixer.Sound(resolve_route("sound/arrow_sound.wav")),


	"objs": pg.mixer.Sound(resolve_route("sound/Pickup_Coin.wav")),
	"blip":pg.mixer.Sound(resolve_route("sound/blip.wav")),
	"dead": pg.mixer.Sound(resolve_route("sound/dead.wav")),
}



class plataform_m(pg.sprite.Sprite):
	def __init__(self,x,y,vl):
		pg.sprite.Sprite.__init__(self)
		self.image = image["plataform_movil"]	
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.step = 0
		self.vlx = int(vl)

	def update(self):
		
		self.step += 1
		self.rect.x += self.vlx
		if self.step > 80:
			self.vlx *=-1
			self.step = 0 

class Trap(pg.sprite.Sprite):
	def __init__(self,x,y,game,sentido = "top"):
		pg.sprite.Sprite.__init__(self)
		self.trap = image["spikes"]
		self.frames = 8
		self.sentido  = sentido

		self.image = self.trap.subsurface((0,0),(32,32))
		
		self.activate = False
		self.activate_spike = False
		self.cont = 0
		self.position = 0

		if self.sentido == "right": self.image = pg.transform.rotate(self.image,-90)
		elif self.sentido == "left": self.image = pg.transform.rotate(self.image,90)
		elif self.sentido == "bottom": self.image = pg.transform.rotate(self.image,180)

		self.rect = self.image.get_rect()
		self.rect.x = x 
		self.rect.y = y 
		self.mask = pg.mask.from_surface(self.image)
		self.game = game

	def update(self):
		self.animation()

		colision = pg.sprite.collide_mask(self.game.player,self)
		if colision != None and self.activate_spike == True:
			self.game.player.dead = True
		colision = pg.sprite.collide_mask(self.game.player,self)
		if colision != None and self.activate_spike == True:
			self.game.player.dead = True
		for enemy in self.game.enemies:
			colision_enemies = pg.sprite.collide_mask(enemy,self)
			if colision_enemies != None and self.activate_spike == True:
				enemy.kill()


	def animation(self):
		if self.activate == False:
			self.activate_spike = False
			self.image = self.trap.subsurface((32*self.position,0),(32,32)) 
			if self.sentido == "right": self.image = pg.transform.rotate(self.image,-90)	
			self.mask = pg.mask.from_surface(self.image)			
			self.position +=1
			if self.position == self.frames: self.activate = True

		else:
			if self.position != 6 and self.position > 0:
				self.position -=1
				self.step = 0

			elif self.position == 6:
				self.step +=1
				if self.step == 55: self.position -=1	
			
			elif self.position == 0:
				self.step +=1
				self.activate_spike = True
				if self.step == 55: self.activate = False
		
			self.image = self.trap.subsurface((32*self.position,0),(32,32)) 
			if self.sentido == "right": self.image = pg.transform.rotate(self.image,-90)	
			elif self.sentido == "left": self.image = pg.transform.rotate(self.image,90)
			elif self.sentido == "bottom": self.image = pg.transform.rotate(self.image,-180)
			self.mask = pg.mask.from_surface(self.image)	
			
class Key(pg.sprite.Sprite):
	def __init__(self,x,y,game):
		pg.sprite.Sprite.__init__(self)
		self.image =pg.transform.scale( image["key"],(8,15)) 	
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.game = game
		self.tween = tween.easeInOutSine
		self.bob_range = 20
		self.bob_speed = 0.6
		self.step = 0
		self.dir = 1
		self.posy = y
		
	def update(self):
		if self.rect.colliderect(self.game.player.rect):
			self.game.player.keys['KEY_YELLOW'] = True
			self.game.sound["objs"].play()
			self.kill()

		offset = self.bob_range *  (self.tween(self.step / self.bob_range) - 0.5)
		self.rect.centery = self.posy + offset * self.dir
		self.step += self.bob_speed
		
		if self.step > self.bob_range:
			self.step = 0
			self.dir *=-1

class Trampoline(pg.sprite.Sprite):
	def __init__(self,x,y,game):
		pg.sprite.Sprite.__init__(self)
		self.frames = [(0,0),(21,0),(41,0),(58,0),(76,0),(21,20),(39,20),(56,20),(76,20)]
		
		self.tramp = image["trampoline"]
		self.image = self.tramp.subsurface(self.frames[0],(13,9))
		self.image = pg.transform.scale(self.image,(32,32))

		self.rect = self.image.get_rect()
		self.rect.x = x 
		self.rect.y = y 
		
		self.frame = len(self.frames)
		self.position = 0

		self.game = game
		self.activate = False

	def update(self):
		if self.rect.colliderect(self.game.player.rect):
			if self.game.player.rect.top < self.rect.top:
				self.game.sound["jump"].stop()
				self.game.sound["jump"].play()

				self.activate = True
				self.jump()

		self.animation()

	def animation(self):
		
		if self.activate == True:
			self.image = self.tramp.subsurface(self.frames[self.position],(13,9)) 			
			self.image = pg.transform.scale(self.image,(32,32))
			self.position +=1
			if self.position >= self.frame: self.activate = False
			
		else:
			self.position = 0
			self.image = self.tramp.subsurface(self.frames[self.position],(13,9)) 			
			self.image = pg.transform.scale(self.image,(32,32))
				
	def jump(self, vl = -15):
		self.game.player.cont_jump = 0
		self.game.player.direcciony = -1
		self.game.player.vly = vl

class Door(pg.sprite.Sprite):
	def __init__(self,x,y,game,Type):
		pg.sprite.Sprite.__init__(self)
		self.position = 0
		self.frames = {0:(0,0),1:(0,42),2:(0,84),3:(0,126)}

		if Type == "YELLOW":
			self.image_a =  image["door"]
		self.image = self.image_a.subsurface(self.frames[0],(39,42))
		self.image = pg.transform.scale(self.image,(62,64))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y 
		self.game = game
		
		self.open = False
		self.step = 0
		self.delay = 10

		self.next = None

	def update(self):
		if self.rect.colliderect(self.game.player.rect):
			if self.game.player.keys['KEY_YELLOW'] == True:
				self.open = True

		if self.open == True: 			
			self.OpenDoor()

	def OpenDoor(self):
		self.step += 2.5
		if self.step > self.delay:
			if self.position < 4:	
				print(self.frames[self.position])				
				self.image = self.image_a.subsurface(self.frames[self.position],(39,42)) 			
				self.image = pg.transform.scale(self.image,(62,64))
				self.position +=1

			elif self.position >= 4:
				self.next = True
				self.position =0

			self.step = 0 
		
class Lemon(pg.sprite.Sprite):
	def __init__(self,x,y,game):
		pg.sprite.Sprite.__init__(self)
		self.image =pg.transform.scale2x( image["lemon"] )
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y 
		self.game = game
		self.tween = tween.easeInOutSine
		self.bob_range = 20
		self.bob_speed = 0.5
		self.step = 0
		self.dir = 1
		self.posy = y

	def update(self):
		if self.rect.colliderect(self.game.player.rect):
				self.game.sound["objs"].play()
				self.kill()

		offset = self.bob_range *  (self.tween(self.step / self.bob_range) - 0.5)
		self.rect.centery = self.posy + offset * self.dir
		self.step += self.bob_speed
		
		if self.step > self.bob_range:
			self.step = 0
			self.dir *=-1

class Fire_Cannon(pg.sprite.Sprite):
	def __init__(self,x,y,game,sentido):
		pg.sprite.Sprite.__init__(self)
		self.fireball = []
		self.limite = 1
		self.game = game
		self.rect = pg.Rect(x,y,20,20)
		self.sentido = sentido
		self.step = 0
	def update(self):
		if len(self.fireball) < self.limite:
			self.step +=1
			if self.step == 20:
				self.fireball.append(Fireball(self.rect.centerx,self.rect.centery,self.sentido))
				self.step = 0

		for fireball in self.fireball:
			colision = pg.sprite.collide_mask(self.game.player,fireball)
			if colision != None:
				self.game.player.dead = True

			colision_pared = pg.sprite.spritecollide(fireball,self.game.plataform,False)
			
			if len(colision_pared) > 0:
				
				self.fireball.remove(fireball)
				
			fireball.update()

class Fireball(pg.sprite.Sprite):

	def __init__(self,x,y,sentido):
		pg.sprite.Sprite.__init__(self)
		self.frames = { 0:(0,0), 1:(0,12), 2:(0,24), }
		self.image_a = image["fireball"]
		self.image = self.image_a.subsurface(self.frames[0],(12,12))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.mask = pg.mask.from_surface(self.image)
		
		if sentido == "right": self.vlx = 3
		elif sentido == "left": self.vlx  = -3
		else: self.vlx = 0		
		
		if sentido == "bottom": self.vly = 3
		elif sentido == "top": self.vly  = -3
		else: self.vly = 0
		
		self.position = 0
		self.step = 0
		self.delay = 10

	def update(self):

		self.rect.x += self.vlx
		self.rect.y += self.vly
		self.animation()

	def animation(self):
		
		self.step += 2.5
		
		if self.step > self.delay:
			if self.position < 3:	
				self.image = self.image_a.subsurface(self.frames[self.position],(12,12)) 			
				self.position +=1
				
			elif self.position >= 3:
				self.position =0

			self.step = 0 

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
				
class Player(Sprite):
	def __init__(self,x,y,game):
		

		self.walk = { 	0:(0,0), 1:(32,0), 2:(64,0), 3:(0,52),}
		self.state = { 0:(32,52), 1:(64,52),}
		self.archers = { 0:(0,104), 1:(32,104),2:(64,104),}
		self.jump= {0:(0,156),}
		self.image_a = image["hugo"]
		self.size = (32,52)
		self.game = game

		self.image = self.image_a.subsurface(self.state[0],(32,52))
		Sprite.__init__(self)


		self.activate_jump = False
		self.mask = pg.mask.from_surface(self.image)
		self.rect = pg.Rect((x,y),(25,52))
		self.rect.centerx = self.rect.x
		self.rect.y = y 


		self.vly = 0
		self.vlx = 0


		self.direccionx = 1
		self.direcciony = 0
		self.stop = False

		self.cont_jump = 2
		self.keys = {	'KEY_YELLOW': False,'KEY_BLUE': False,
						'KEY_RED': False,
					}
		
		self.cont_shot  = 0

		self.dead = None
		self.cont_dead = 0

	def update(self):
		
		if self.vlx == 0:
		
			self.frames = self.state

			if self.direccionx > 0: self.animation(0,self.state)
			if self.direccionx < 0: self.animation(1,self.state)
		
		elif self.vlx != 0:
		
			self.frames = self.walk
		
			if self.vlx > 0:  self.animation(0,self.walk) 
			elif self.vlx < 0:  self.animation(1,self.walk)
		
		if self.direcciony < 0:	
			
			self.image = self.image_a.subsurface(self.jump[0],(32,52))
			
			if self.direccionx < 0: self.image = pg.transform.flip(self.image,1,0)
			elif self.direccionx > 0: pass

		self.mask = pg.mask.from_surface(self.image)
		self.move()	

		if self.vlx >= 7: self.vlx = 7
		elif self.vlx <= -7: self.vlx = -7	

		if self.stop == True:
			
			if self.vlx > 0: self.vlx -=1
			elif self.vlx < 0: self.vlx +=1
			else: self.stop = False
		
		self.gravity()
		self.Fundead()
		self.collided()

		if len(self.colision_plataform) == 0 and self.cont_jump == 2:
			self.direcciony = -1
			self.cont_jump = 1

	def move(self):
		move = pg.key.get_pressed()
		
		if move[pg.K_LEFT]:
			self.direccionx = -1
			self.vlx +=-1  			
			self.stop = False
		if move[pg.K_RIGHT]:
			self.direccionx = 1
			self.vlx += 1		
			self.stop = False	
		if move[pg.K_c]:
		    if self.vlx == 0:
			    self.cont_shot += 0.55
			    if self.cont_shot>= 10: self.archer(1)
			    elif self.cont_shot >= 5: self.archer(0)

	def archer(self,pos):
		
		self.image = self.image_a.subsurface(self.archers[pos],(32,52))
		
		if self.direccionx < 0: self.image = pg.transform.flip(self.archers[pos],1,0)
		elif self.direccionx > 0: pass  			

	def shot(self):

		self.game.sound["arrow"].play()
		
		if self.direccionx > 0: self.game.arrow.add(Arrow(self.rect.right +5,self.rect.centery,1,self.game))
		elif self.direccionx < 0: self.game.arrow.add(Arrow(self.rect.left -5,self.rect.centery,-1,self.game))

	def Fundead(self):
		
		if self.dead == True:
			self.fuerza_gravitatoria = 0
			self.vlx = 0
			self.vly = 0

			if self.cont_dead == 10: sound["dead"].play()
			elif self.cont_dead == 20: self.game.effect.add(Dead(self.rect.centerx,self.rect.centery))
			elif self.cont_dead >= 100: self.game.load()

			self.cont_dead +=1

class Arrow(pg.sprite.Sprite):
	def __init__(self,x,y,direccion,game):
		pg.sprite.Sprite.__init__(self)
		self.direccion = direccion

		if self.direccion > 0: self.image = image["arrow"]
		elif self.direccion < 0: self.image = pg.transform.flip(pg.image.load(resolve_route("image/sprites/hug/arrow.png") ),1,0)

		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y  = y
		self.game = game
		self.vl = 11 if self.direccion > 0 else -11

	def update(self):
		self.colision =  pg.sprite.spritecollide(self,self.game.plataform,False)
		if len(self.colision) > 0:
			self.vl = 0
			self.vly = 0
		self.colision_enemy = pg.sprite.spritecollide(self,self.game.enemies,True)
		if len(self.colision_enemy) > 0: self.kill()

		self.rect.x += self.vl
	
class Dead(pg.sprite.Sprite):
	def __init__(self,x,y):
		pg.sprite.Sprite.__init__(self)
		self.image = image["dead"]
		self.image = pg.transform.scale(self.image,(32,32))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.tween = tween.easeInOutSine
		self.bob_range = 20
		self.bob_speed = 0.7
		self.step = 0
		self.dir = 1
		self.posy = y
		self.posx = x

	def update(self):
		offset = self.bob_range *  (self.tween(self.step / self.bob_range) - 0.5)
		self.rect.centery -=1 
		self.rect.centerx = self.posx + offset * self.dir
		self.step += self.bob_speed
		
		if self.step > self.bob_range:
			self.step = 0
			self.dir *=-1

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

class TileMap:
	def __init__(self,filename):
		tm = pytmx.load_pygame(filename,pixelaplha = True)
		self.width = tm.width * tm.tilewidth
		self.height = tm.height * tm.tileheight
		self.tmxdata = tm

	def render(self,surface):
		ti = self.tmxdata.get_tile_image_by_gid
		for layer in self.tmxdata.visible_layers:
			if isinstance(layer,pytmx.TiledTileLayer):
				for x,y,gid in layer:
					tile = ti(gid)
					if tile: surface.blit(tile,(x* self.tmxdata.tilewidth,y* self.tmxdata.tileheight))
						
	def make_map(self):

		temp_surface = pg.Surface((self.width,self.height)) #pg.SRCALPHA
		temp_surface.set_colorkey((0,0,0))	
		self.render(temp_surface)
		#temp_surface.convert_alpha()
		
		return temp_surface

class Camera:
	def __init__(self,width,height):
		self.camera = pg.Rect((0,0),(width,height))
		self.width = width
		self.height = height
	
	def apply(self,entity):
		return entity.rect.move(self.camera.topleft)
	def apply_rect(self,rect):
		#mueve la posición de la surface a la pos de la camara en topleft (arriba/izquierda)
		return rect.move(self.camera.topleft)
	
	def update(self,target):
		#Targe en negativo para que en caso de llegar al extremo left (positivo) , el movimiento sea 0
		x =-target.rect.x + int(WIDTH/2)
		y = -target.rect.y + int(HEIGHT/2)
		#print(x)
		#limit scrolling to map size
		x = min(0,x) #left
		y = min(0,y) #top
		#print(self.width)
		#lógica inversa
		#Si -(self.width - WIDTH) es menor que X, X seguira avanzando, en caso contrario X se mantendrá fijo
		x = max(-(self.width - WIDTH),x)#right
		y = max(-(self.height-HEIGHT),y)
		self.camera = pg.Rect(x,y,self.width,self.height)

class Plataform(pg.sprite.Sprite):
	def __init__(self,x,y,w,h):
		pg.sprite.Sprite.__init__(self)
		self.rect = pg.Rect((x,y),(w,h))
		self.rect.x = x
		self.rect.y = y
		self.vlx = 0

class Spikes(pg.sprite.Sprite):
	def __init__(self,x,y,w,h,game):
		pg.sprite.Sprite.__init__(self)
		self.rect = pg.Rect((x,y),(w,h))
		self.rect.x = x
		self.rect.y = y
		self.game = game

	def update(self):
		if self.rect.colliderect(self.game.player.rect):
			self.game.player.dead = True

		for enemy in self.game.enemies:
			if self.rect.colliderect(enemy.rect):
				enemy.kill()

class Menu:
	def __init__(self,maps):
		self.maps = maps
		self.surface_text = lambda text,color: pg.font.Font("Pixel Digivolve.otf",30).render(text,2,color)

		self.clock = pg.time.Clock()
		
		self.lemon =  pg.transform.scale(image["lemon"],(30,30))
		self.hugo =  pg.transform.flip(image["hugo"],1,0)
		self.hugo = self.hugo.subsurface((32,52),(32,52))
		self.paty = pg.transform.scale(image["paty"],(32,52))
 
		self.exit = False
		self.color_selection = pg.Color("#DBAE09")
		self.color_base = pg.Color("#C4C4C4")
		self.position = 1
		self.changes_maps = False	

		self.game_active = False
		self.exit_game = False
	
	def update(self):

		lemon_pos = {1:(0,0),2:(0,40), 3:(0,80),4:(0,120)}
		text_continue = self.surface_text("Continue",self.color_selection)
		text_partida = self.surface_text("Start Game",self.color_base)
		text_about = self.surface_text("About",self.color_base)
		text_exit = self.surface_text("Exit",self.color_base)
		text_twitter = self.surface_text("@hug588",pg.Color("#1CA4F4"))
		
		if self.game_active == False:
			texto = (text_partida,text_about,text_exit,text_twitter)
			position = 2

		else:
			texto = (text_continue,text_partida,text_about,text_exit,text_twitter)			
			position = 1
		
		
		limite = len(texto) 

		if self.exit_game != True:
			surface = pg.Surface((620,480))
			surface = self.apply(surface,texto)
			surface.blit(self.hugo,(400,400))
			surface.blit(self.paty,(440,400))
		
		while self.exit != True:
			self.clock.tick(30)
			for event in pg.event.get():
				if event.type == pg.QUIT:
					self.exit_game = True
					self.exit = True

				elif event.type == pg.KEYDOWN:
					if event.key == pg.K_RETURN:

						if position == 1:
							self.exit = True

						elif position == 2:
							self.exit = True
							self.changes()
							self.game_active = True

						elif position == 3:							
							self.about()

							sound["blip"].stop()							
							sound["blip"].play()							

						elif position == 4:
							self.exit_game = True
							self.exit = True

					elif event.key == pg.K_DOWN:
						
						if position < limite:
							position +=1

							sound["blip"].stop()							
							sound["blip"].play()							


					elif event.key == pg.K_UP:
						if self.game_active == False:
							if position > 2:								
								position -=1
						else:
							if position > 1:
								position -=1

							sound["blip"].stop()							
							sound["blip"].play()							


			SCREEN.blit(surface,(0,0))
			SCREEN.blit(self.lemon,lemon_pos[position-1]) if self.game_active == False else SCREEN.blit(self.lemon,lemon_pos[position]) 
			pg.display.flip()

	def apply(self,surface,args,x= 30,y = 0,space_line = 0,sign = 1):
		surface.fill(pg.Color("#0C040C"))
		cont = 0
		value = 40 * sign
		for text in args:
			surface.blit(text,(x,y))
			cont +=1
			if space_line > 0 and cont == space_line:
				y +=80
				cont = 0
			else:
				y += value
		return surface

	def about(self,exit = False):
		text_hug = self.surface_text("Developer/programmer: Hugo  ",self.color_base)
		text_twitter_hug = self.surface_text("@hug588",pg.Color("#1CA4F4"))

		text_paty = self.surface_text("Artist: Patricia",self.color_base)
		text_facebook_paty = self.surface_text("The pash team",pg.Color("#3C5C9C"))

		text_return = self.surface_text("Return [K]",self.color_base)
		texto = (text_hug,text_twitter_hug,text_paty,text_facebook_paty)

		surface = pg.Surface((620,480))
		surface = self.apply(surface,texto,space_line= 2)
		surface.blit(text_return,(40,440))
		surface.blit(self.lemon,(0,440))
		surface.blit(self.hugo,(400,400))
		surface.blit(self.paty,(440,400))
		
		while exit != True:
			self.clock.tick(30)
			for event in pg.event.get():
				if event.type == pg.QUIT:
					self.exit_game = True
					self.exit = True
					exit = True

				if event.type == pg.KEYDOWN:
					if event.key == pg.K_k:
						exit = True
						sound["blip"].stop()							
						sound["blip"].play()							

								

			SCREEN.blit(surface,(0,0))
			pg.display.flip()

	def changes(self,exit = False):
		surface = pg.Surface((620,480))
		surface_selection = pg.Surface((200,40))

		texto = [self.surface_text( "Map {}".format(i+1),self.color_base) for i in range(len(self.maps))]
		position = 1
		y_move = 0
		surface_selection = self.apply(surface_selection,texto,y = y_move,sign= -1)
		text_return = self.surface_text("Return [K]",self.color_base)

		surface.fill(pg.Color("#0C040C"))
		surface.blit(text_return,(40,440))
		SCREEN.blit(surface,(0,0))
		SCREEN.blit(self.lemon,(0,440))
		
		while exit != True:

			self.clock.tick(30)
	
			for event in pg.event.get():
				if event.type == pg.QUIT:
					self.exit_game = True
					self.exit = True
					exit = True
				if event.type == pg.KEYDOWN:
					if event.key == pg.K_RETURN:
						self.position = position -1
						self.changes_maps = True
						exit = True
					if event.key == pg.K_k:
						self.exit = False
						exit = True
					elif event.key == pg.K_UP:
						if position < len(self.maps):
							y_move +=40
							surface_selection = self.apply(surface_selection,texto,y = y_move,sign =-1 )
							position +=1
					elif event.key == pg.K_DOWN:
						if position > 1:
							y_move -=40
							surface_selection = self.apply(surface_selection,texto,y = y_move, sign= -1)	
							position -=1


			SCREEN.blit(surface_selection,(240,100))	
			pg.display.flip()

class Game:
	
	def __init__(self,maps):
		self.maps = maps
		self.sound = sound
		self.map_cont = 0
		self.map = TileMap(self.maps[self.map_cont])
		self.Mapimage = self.map.make_map()
		self.Maprect = self.Mapimage.get_rect()
		self.camera = Camera(self.map.width,self.map.height)
		self.changes_maps = False

		#Es más rápido crear otra Surface que dibujarlo directamente en la pantalla
								
	def load(self):

		self.effect = pg.sprite.Group()	
		self.arrow = pg.sprite.Group()
		self.plataform = pg.sprite.Group()
		self.plataform_m = pg.sprite.Group()
		self.enemies = pg.sprite.Group()
		self.objs = pg.sprite.Group()
		self.spike = pg.sprite.Group()
		self.trap = pg.sprite.Group()
		self.fire_cannon = pg.sprite.Group()

		for sprite in self.map.tmxdata.objectgroups:
			for tile_object in sprite:
				if tile_object.name == "Player": self.player = Player(tile_object.x,tile_object.y,self)

		for tile_object in self.map.tmxdata.objects:
			if tile_object.name == "plataform": self.plataform.add(Plataform(tile_object.x,tile_object.y,tile_object.width,tile_object.height))
			elif tile_object.name == "Door": self.objs.add(Door(tile_object.x,tile_object.y,self,"YELLOW"))
			elif tile_object.name == "Apple": self.enemies.add(Apple(tile_object.x,tile_object.y,self,tile_object.type))
			elif tile_object.name == "Key": self.objs.add(Key(tile_object.x,tile_object.y,self))
			elif tile_object.name == "Lemon": self.objs.add(Lemon(tile_object.x,tile_object.y,self))
			elif tile_object.name == "Spike_trap": self.trap.add(Trap(tile_object.x,tile_object.y,self,tile_object.type))
			elif tile_object.name == "plataform_m": self.plataform_m.add(plataform_m(tile_object.x,tile_object.y,tile_object.type))	
			elif tile_object.name == "Spike": self.spike.add(Spikes(tile_object.x,tile_object.y,tile_object.width,tile_object.height,self))
			elif tile_object.name == "Fire_cannon": self.fire_cannon.add(Fire_Cannon(tile_object.x,tile_object.y,self, tile_object.type))				
			elif tile_object.name == "jump": self.objs.add(Trampoline(tile_object.x,tile_object.y,self))
		
	def update(self):
		
		self.camera.update(self.player)
		self.spike.update()
		self.trap.update()
		self.fire_cannon.update()
		self.arrow.update()
		self.enemies.update()
		self.plataform_m.update()
		self.effect.update()
		
		for objs in self.objs:	
			objs.update()

			try:
				if objs.next == True:
					
					if self.map_cont < len(self.maps) -1: self.map_cont +=1
					else: self.map_cont = 0

					self.map =  TileMap(self.maps[self.map_cont])
					self.Mapimage = self.map.make_map()
					self.Maprect = self.Mapimage.get_rect()
					self.camera = Camera(self.map.width,self.map.height)
					self.load()
					
			except  Exception  as e: pass

		if self.changes_maps == True:
		
			self.map =  TileMap(self.maps[self.map_cont])
			self.Mapimage = self.map.make_map()
			self.Maprect = self.Mapimage.get_rect()
			self.camera = Camera(self.map.width,self.map.height)
			self.load()
			self.changes_maps = False			

		self.player.update()

	def draw(self):


		for arrow in self.arrow:
			SCREEN.blit(arrow.image,self.camera.apply(arrow))
		
		SCREEN.blit(self.Mapimage,self.camera.apply_rect(self.Maprect))
		
		for plataform_m in self.plataform_m: 
			SCREEN.blit(plataform_m.image,self.camera.apply(plataform_m))	 
		
		for cannon in self.fire_cannon:
			for fireball in cannon.fireball:
				SCREEN.blit(fireball.image,self.camera.apply(fireball))
		
		for enemies in self.enemies: 
			SCREEN.blit(enemies.image,self.camera.apply(enemies))	
		
		for objs in self.objs: 
			SCREEN.blit(objs.image,self.camera.apply(objs))
		
		SCREEN.blit(self.player.image,self.camera.apply(self.player))
		
		for trap in self.trap:
			SCREEN.blit(trap.image,self.camera.apply(trap))


		for effect in self.effect:
			SCREEN.blit(effect.image,self.camera.apply(effect))


def main():

	exit = False
	clock = pg.time.Clock()
	maps= ["map/map1.tmx","map/map2.tmx","map/map3.tmx","map/map4.tmx","map/map5.tmx","map/map6.tmx","map/map7.tmx"]
	menu = Menu(maps)
	game = Game(menu.maps)
	game.load()
	

	#Creando un objeto joystick e iniciando

	joystick =  pg.joystick.Joystick(0)  if pg.joystick.get_count() > 0 else None
	joystick.init() if joystick != None else None


	background = pg.Surface((WIDTH,HEIGHT)).convert()
	background.blit(pg.transform.scale(image["background"],(WIDTH,HEIGHT)),(0,0))
	draw_background = lambda background: SCREEN.blit(background,(0,0))
		

	while exit != True and menu.exit_game != True:
		clock.tick(60)
		
		for event in pg.event.get():
			if event.type == pg.QUIT: exit = True
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_x:
					if game.player.cont_jump > 0:
						game.player.diffx = 0

						game.sound["jump"].stop()
						game.sound["jump"].play()

						game.player.vly = -8
						game.player.cont_jump -=1
						game.player.direcciony = -1

				if event.key == pg.K_RETURN: menu.exit = False

			if event.type == pg.KEYUP:
				if event.key == pg.K_RIGHT or event.key == pg.K_LEFT: game.player.stop = True
				if event.key == pg.K_c:
					if game.player.cont_shot >= 13:
						game.player.shot()
						game.player.cont_shot = 0
					else: game.player.cont_shot = 0
			
		if menu.changes_maps == True:
			game.map_cont = menu.position
			game.changes_maps = True
			menu.changes_maps = False
		
		if menu.exit != True: menu.update()
		
		draw_background(background)

		#Cerrar el videojuego completamente sin pasar por dibujar el nivel actual(lvl1 por defecto)
		if menu.exit_game != True: game.draw()


		game.update()
		pg.display.flip()

if __name__ == "__main__":
	main()
