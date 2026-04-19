import pygame
import constantes




class Personaje():
    def __init__(self,x,y):
        self.forma = pygame.Rect(0,0,constantes.ALTO_PERSONAJE,constantes.ANCHO_PERSONAJE)
        self.forma.center = (x,y)

    def dibujar(self,interfaz):
        pygame.draw.rect(interfaz,constantes.COLOR_PERSONAJE,self.forma)