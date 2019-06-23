import pygame as pg 

from recursos import image,sound 

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
	
	def update(self,SCREEN):

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
							self.changes(SCREEN)
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

	def changes(self,SCREEN,exit = False,):
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