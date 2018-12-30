class Lifes(pygame.sprite.Sprite):
    def __init__(self,x= 10,y = 10):
        pygame.sprite.Sprite.__init__(self)
        self.sheet = pygame.transform.scale2x(pygame.image.load(os.path.abspath("sprites") + "/image/Hugo_Juego2.0.png"))
        self.image = self.sheet.subsurface((149*2,65*2),(9*2,8*2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self,screen):
        screen.blit(self.image,self.rect)

class State():
	def __init__(self,num_lifes = 3):
		self.lifes = []
		self.num_lifes = num_lifes
	
	def life(self):
		x,y = 10,500
		for i in range(self.num_lifes):
			i = Lifes(x,y)
			self.lifes.append(i)
			x +=20
			#y +=10

	def draw(self,screen):
		for life in self.lifes:
			life.draw(screen)
	

	def remove(self):
		self.lifes.pop()

class Escena():
	def __init__(self):
		#self.state = State()
		#self.state.life()
		#self.scroll = True
		#self.escena = nivel.Nivel()
		#self.escena.generate()
		#self.mosaic = [[BLOCK for w in range(MAPWIDTH)] for h in range(MAPHEIGHT)]
		
		self.cerrar = False
		self.clock = pygame.time.Clock()
		#pygame.key.set_repeat(1, 1000//60)


	def loop(self):
		while self.cerrar != True:
			self.clock.tick(40)		
			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.cerrar = True
				if event.type == pygame.KEYUP:
					pass
					#self.escena.player.nomove()

			
			
			#for row in range(MAPHEIGHT):
			#	for column in range(MAPWIDTH):
			#		screen.blit(TEXTURES[TILEMAP[row][column]],(column*TILESIZE,row*TILESIZE))
			
			for tile in TILES:
				for i in tile: 
					i.scale2x()
					screen.blit(i.image,i.rect)


			#screen.scroll(int(self.escena.player.vlx),int(self.escena.player.vly))
			#self.escena.update()
			#self.escena.draw(screen)
			#self.state.draw(screen)