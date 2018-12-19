import pygame
import nivel
import os 

#pygame.init()
#pygame.display.init()
pygame.joystick.init()

COLOR = pygame.Color("#0C6434")
ANCHO,ALTO = 1000,520
VENTANA = pygame.display.set_mode((ANCHO,ALTO))    
pygame.display.set_caption("LEMON BOY: THE GAME VS 0.11")  

class Fondo(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(os.path.abspath("sprites") + "/image/muroladrillos.png")
		self.rect = self.image.get_rect()


class Escena():
	def __init__(self):
		self.escena = nivel.Nivel1()
		self.escena.generate()
		#print(len(self.escena.group_inmovil))
		self.fondo = Fondo()

		self.cerrar = False
		self.clock = pygame.time.Clock()
		
		""" JOYSTICK 1"""
		#self.joystick =  pygame.joystick.Joystick(0)
		#self.joystick.init()
		

	def reset(self):
		self.escena.group_general.empty()
		self.escena.group_inmovil.empty()
		self.escena.group_dead.empty()
		self.escena.group_lemones.empty()
		self.escena.group_enemy.empty()
		self.escena.generate()		

	def loop(self):
		camara = pygame.Rect(0,0,1000,700)
		while self.cerrar != True:
			self.clock.tick(40)
			self.escena.update()
			
			if self.escena.player.reset_automatico == True:
				self.reset()

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.cerrar = True


				if event.type == pygame.KEYUP:
					self.escena.player.nomove()


				"""COMPROBAR BOTONES DE JOYSTICK"""
				if event.type == pygame.JOYBUTTONDOWN:
					print(event)
				if event.type == pygame.JOYBALLMOTION:
					print(event)
				if event.type == pygame.JOYAXISMOTION:
					print(event)

				if event.type == pygame.JOYHATMOTION:
					print(event.position)						
				
			#	print(self.joystick.get_hat(0))
			#	if self.joystick.get_hat(0) == (1,0):
			#		self.escena.player.direccionx = 1
			#		self.escena.player.vlx +=1
			#	elif self.joystick.get_hat(0) == (-1,0):
			#		self.escena.player.direccionx = -1
			#		self.escena.player.vlx -=1


			if self.escena.prox_escena != None:
				self.escena = self.escena.prox_escena
				self.reset()
			
			#print(self.joystick.get_name())			
			#print(self.joystick.get_button(3))
			VENTANA.fill(COLOR)
			#VENTANA.blit(self.fondo.image,self.fondo.rect)
			self.escena.draw(VENTANA)
			

		
			pygame.display.flip()


			
			
def main():
	escena = Escena()
	escena.loop()
		
if __name__ == '__main__':
	main()
	pygame.quit()
	
