import pygame
from sprites import Elementos
pygame.init()

WIDTH = 400
HIGH = 400
VIOLET = (124,36,119)


VENTANA = pygame.display.set_mode((WIDTH,HIGH))
group = pygame.sprite.Group()
pygame.display.set_caption("MAPEADO")




def main():



    clock = pygame.time.Clock()
    cerrar = False
    mousepos = None

    Tierra = Elementos.Block(10,340,(20*2,20*2),(0,0))
    Tierra.scale2x()
    
    group.add(Tierra)

    arrastrar = False

    while cerrar != True:

        clock.tick(30)
        mousepos = pygame.mouse.get_pos()
        #print(mousepos)
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                    cerrar = True
                    


            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    print("SOY DE IZQUIERDA")
                    for tiles in group:
                        if mousepos[1] >= tiles.rect.top and mousepos[1] <= tiles.rect.bottom and mousepos[0] >= tiles.rect.left and mousepos[0] <= tiles.rect.right:
                            tiles.arrastrar = True
                 
                if event.button == 3:
                    print("SOY DE DERECHA")

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    for tiles in group:
                        tiles.arrastrar = False


        for tiles in group:
            if tiles.arrastrar == True:
                
                tiles.rect.x = mousepos[0]
                tiles.rect.y = mousepos[1]
        


        
        VENTANA.fill(VIOLET)
        group.draw(VENTANA)
        pygame.display.update()


    pygame.quit()



main()