print("Hola mundo")
import pygame
import constantes
from personaje import Personaje

pygame.init()

jugador = Personaje(50,50)


ventana = pygame.display.set_mode((constantes.ANCHO_VENTANA,
                                   constantes.ALTO_VENTANA))
pygame.display.set_caption("TOPLLEAR")
run = True

while run:
    jugador.dibujar(ventana)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()