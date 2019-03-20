import pygame as pg
import os, pytmx, sys

#Prueba
import threading as th

from script import Player
from script import Enemies
from script import Element
from script import function_utils as fun

pg.display.init()
pg.mixer.init()
pg.joystick.init()
pg.font.init()

WIDTH = 620
HEIGHT = 480

SCREEN = pg.display.set_mode((WIDTH,HEIGHT))
pg.display.set_caption("Project Hugo")



pg.display.set_icon(pg.image.load(fun.resolve_route("lemon.ico") ))
 

image = {
	"background":pg.image.load(fun.resolve_route("image/background.png")),
	"lemon":pg.image.load(fun.resolve_route("image/lemon.png")),
	"hugo":pg.image.load(fun.resolve_route("image/sprites/hug/hug0.png")),
	"paty":pg.image.load(fun.resolve_route("image/sprites/paty.png")),
 }


sound = {	
	
	"jump": pg.mixer.Sound(fun.resolve_route("sound/Jumpa.wav")),
	"arrow": pg.mixer.Sound(fun.resolve_route("sound/arrow_sound.wav")),
	"objs": pg.mixer.Sound(fun.resolve_route("sound/Pickup_Coin.wav")),
	"blip":pg.mixer.Sound(fun.resolve_route("sound/blip.wav")),
	"dead": pg.mixer.Sound(fun.resolve_route("sound/dead.wav")),
}


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
					if tile:
						
						surface.blit(tile,(x* self.tmxdata.tilewidth,y* self.tmxdata.tileheight))
						
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
		self.font = pg.font.Font("Pixel Digivolve.otf",30)
		self.clock = pg.time.Clock()
		
		self.lemon =  pg.transform.scale(image["lemon"],(30,30))
		self.hugo =  pg.transform.flip(image["hugo"],1,0)
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
		text_continue = self.font.render("Continue",2,self.color_selection)
		text_partida = self.font.render("Start Game ",2,self.color_base)
		text_about = self.font.render("About",2,self.color_base)
		text_exit = self.font.render("Exit",2,self.color_base)
		text_twitter = self.font.render("@hug588",2,pg.Color("#1CA4F4"))
		
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
		text_hug = self.font.render("Developer/programmer: Hugo  ",2,self.color_base)
		text_twitter_hug = self.font.render("@hug588",2,pg.Color("#1CA4F4"))

		text_paty = self.font.render("Artist: Patricia",2,self.color_base)
		text_facebook_paty = self.font.render("The pash team",2,pg.Color("#3C5C9C"))

		text_return = self.font.render("Return [K]",2,self.color_base)
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

		texto = [self.font.render( "Map {}".format(i+1),2,self.color_base) for i in range(len(self.maps))]
		position = 1
		y_move = 0
		surface_selection = self.apply(surface_selection,texto,y = y_move,sign= -1)
		text_return = self.font.render("Return [K]",2,self.color_base)

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
		self.rampas = []
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
				if tile_object.name == "Player":
					self.player = Player.Player(tile_object.x,tile_object.y,self)

		for tile_object in self.map.tmxdata.objects:
			if tile_object.name == "Door":
				if tile_object.type == "YELLOW":
					self.objs.add(Element.Door(tile_object.x,tile_object.y,self,"YELLOW"))
			elif tile_object.name == "Apple":				
					self.enemies.add(Enemies.Apple(tile_object.x,tile_object.y,self,tile_object.type))
			elif tile_object.name == "Key":
				self.objs.add(Element.Key(tile_object.x,tile_object.y,self))
			elif tile_object.name == "Lemon":
				self.objs.add(Element.Lemon(tile_object.x,tile_object.y,self))
			elif tile_object.name == "Spike_trap":
				self.trap.add(Element.Trap(tile_object.x,tile_object.y,self,tile_object.type))
			elif tile_object.name == "plataform":
				self.plataform.add(Plataform(tile_object.x,tile_object.y,tile_object.width,tile_object.height))
			elif tile_object.name == "plataform_m":
				self.plataform_m.add(Element.plataform_m(tile_object.x,tile_object.y,tile_object.type))	
			elif tile_object.name == "Spike":
				self.spike.add(Spikes(tile_object.x,tile_object.y,tile_object.width,tile_object.height,self))
			elif tile_object.name == "Fire_cannon":
					self.fire_cannon.add(Element.Fire_Cannon(tile_object.x,tile_object.y,self, tile_object.type))				
			elif tile_object.name == "jump":
				self.objs.add(Element.Trampoline(tile_object.x,tile_object.y,self))
		
	def update(self):
		
		self.camera.update(self.player)
		self.spike.update()
		self.trap.update()
		self.fire_cannon.update()
		self.arrow.update()
		self.enemies.update()
		self.plataform_m.update()

		for objs in self.objs:	
			objs.update()

			try:
				if objs.next == True:
					if self.map_cont < len(self.maps) -1:
						self.map_cont +=1
					else:
						self.map_cont = 0
					self.map =  TileMap(self.maps[self.map_cont])
					self.Mapimage = self.map.make_map()
					self.Maprect = self.Mapimage.get_rect()
					self.camera = Camera(self.map.width,self.map.height)
					self.load()
					
			except:
				pass

		if self.changes_maps == True:
		
			self.map =  TileMap(self.maps[self.map_cont])
			self.Mapimage = self.map.make_map()
			self.Maprect = self.Mapimage.get_rect()
			self.camera = Camera(self.map.width,self.map.height)
			self.load()
			self.changes_maps = False			

		self.player.update()

	def draw(self):

		#SCREEN.fill(pg.Color("#2b425d"))


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

def Main():

	exit = False
	clock = pg.time.Clock()
	maps= ["map/map1.tmx","map/map2.tmx","map/map3.tmx","map/map4.tmx","map/map5.tmx","map/map6.tmx"]
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
			if event.type == pg.QUIT:
				exit = True
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_x:
					if game.player.cont_jump > 0:
						game.player.diffx = 0

						game.sound["jump"].stop()
						game.sound["jump"].play()

						game.player.vly = -8
						game.player.cont_jump -=1
						game.player.direcciony = -1

				if event.key == pg.K_RETURN:
					menu.exit = False

			if event.type == pg.KEYUP:
				if event.key == pg.K_RIGHT or event.key == pg.K_LEFT:
					game.player.stop = True
				if event.key == pg.K_c:
					if game.player.cont_shot >= 13:
						game.player.cont_shot = 0
						game.player.shot()
					else:
						game.player.cont_shot = 0
			
		if menu.changes_maps == True:
			game.map_cont = menu.position
			game.changes_maps = True
			menu.changes_maps = False
		
		if menu.exit != True:
			menu.update()
		

		#Dibujar el fondo laguea mucho, así que usé un hilo para dibujarlo aparte mientras el resto se carga, posiblemente use más hilos 

		th.Thread(target= draw_background(background) )
		
		#Cerrar el videojuego completamente sin pasar por dibujar el nivel actual(lvl1 por defecto)
		if menu.exit_game != True:
			game.draw()


		game.update()
		pg.display.flip()

if __name__ == "__main__":
	Main()
