import pygame
from sprites import Elementos


WIDTH = 1000
HIGH = 480
VIOLET = (124,36,119)


VENTANA = pygame.display.set_mode((WIDTH,HIGH))
pygame.display.set_caption("MAPEADO")
group = pygame.sprite.Group()

nivel1 =["-------------------------",
		"-------------------------",
		"#E--------P------------S-",
		"####----###---#####---###",
		"#-------#-----#######--##",
		"#-----###-----########--#",
		"##------#-----####-----##",
		"#X----###-----####----###",
		"##-----##------------####",
		"####------XX--###########",
		"#########################"]


nivel2 =["#E--------P------------S-",
		"####----###---#####---###",
		"#-------#-----#######--##",
		"#-----###-----########--#",
		"##------#-----####-----##",
		"#X----###-----####----###",
		"##-----##------------####",
		"####------XX--###########",
		"#########################"]


nivel3 =["#E--------P------------S-",
		"####----###---#####---###",
		"#-------#-----#######--##",
		"#-----###-----########--#",
		"##------#-----####-----##",
		"#X----###-----####----###",
		"##-----##------------####",
		"####------XX--###########",
		"#########################"]

def convertir(nivel):

	
	x = 0
	y = 40

	for i in range(len(nivel)):
		nivel[i] = list(nivel[i])

	for i in range(len(nivel)):
		for j in range(len(nivel[0])):
			if nivel[i][j] == "E":
				pass

			elif nivel[i][j] == "#":
				j = Elementos.Block(x,y,(20*2,20*2),(0,0))
				j.scale2x()
				group.add(j)
			elif nivel[i][j] == "X":
				j = Elementos.Puas(x,y)
				group.add(j)

			elif nivel[i][j] == "S":
				j = Elementos.Puerta(x,y)
				group.add(j)
			elif nivel[i][j] == "-":
				pass  

			elif nivel[i][j] == "P":
				j = Elementos.Lemon(x,y)
				group.add(j)

			x +=40

		x = 0
		y +=40
	


def main():
	
	convertir(nivel1)
	clock = pygame.time.Clock()
	cerrar = False

	while cerrar != True:
		clock.tick(30)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				cerrar= True


		group.draw(VENTANA)
		pygame.display.update()

main()