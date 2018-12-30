import pygame

class Animation:
	def __init__(self,frame,tamano,hoja_sprite,lados = None):
		self.step = 0
		self.cont = 0
		self.frame_current = 0
		self.frame = frame
		self.hoja_sprite = hoja_sprite
		self.image = None
		self.tamano = tamano
		self.lados = lados	
		self.limite = 20
	def sprites(self,vlx,vly,direccion_x,pos_frame,salto = None):
		if vlx == 0:
			if self.lados != None:
				if direccion_x > 0:
					self.image =  self.hoja_sprite.subsurface(self.lados)
					self.frame_current = 0
				elif direccion_x < 0:
					self.image = pygame.transform.flip(self.hoja_sprite.subsurface(self.lados),True,False)
					self.frame_current = 0
			else:
				pass
		elif vlx < 0:
			if self.frame_current < self.frame:
				self.step +=5
				if self.step >= 10:
					self.image = pygame.transform.flip(self.hoja_sprite.subsurface(pos_frame[self.frame_current], self.tamano ),True,False)
					self.frame_current +=1
					self.step = 0
			else:
				self.frame_current = 0

		elif vlx > 0:
			if self.frame_current < self.frame:
				self.step +=5
				if self.step >=10:
					self.image = self.hoja_sprite.subsurface(pos_frame[self.frame_current], self.tamano )				
					self.frame_current +=1
					self.step = 0
			else:
				self.frame_current = 0
		if salto != None:
			if vly < 0:
				if direccion_x > 0:
					self.image = pygame.transform.flip(self.hoja_sprite.subsurface(salto),True,False)
				elif direccion_x < 0:
					self.image = self.hoja_sprite.subsurface(salto)
		return self.image

	def basic(self,lista,repetir = 0,loop = False ):
				
		self.image = self.hoja_sprite.subsurface(lista[self.frame_current],self.tamano)	
		if self.frame_current < self.frame -1:
			self.step +=5
			if self.step >= self.limite:			
				self.frame_current +=1
				self.step = 0
		else:
			if loop == False:		
				self.cont +=1
				if self.cont < repetir:
					self.frame_current = 0
			else:
				self.frame_current = 0
		return self.image
		

class New_Animation:
	def __init__(self,posiciones,hoja,tamano):
		self.step = 0
		self.cont = 0
		self.frame_current = 0
		self.hoja = hoja
		self.posiciones = posiciones
		self.image = None
		self.tamano = tamano
		

	def update(self,flip):
		if flip == True:
			self.image = self.hoja.subsurface(self.posiciones[self.frame_current], self.tamano )				
		elif flip == False:
			self.image = pygame.transform.flip(self.hoja.subsurface(self.posiciones[self.frame_current], self.tamano ),True,False)					
		if self.frame_current < len(self.posiciones) -1:
			self.step +=5
			if self.step >=30:	
					self.frame_current +=1
					self.step = 0

		else:
			self.frame_current = 0	

		return self.image

def main():
	pass


if __name__ == '__main__':
	main()