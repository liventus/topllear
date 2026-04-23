print("Hola mundo")
import pygame
import constantes
from personaje import Personaje
from weapon import Weapon
pygame.init()
ventana = pygame.display.set_mode((constantes.ANCHO_VENTANA,
                                   constantes.ALTO_VENTANA))



pygame.display.set_caption("TOPLLEAR")

def escalar_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    nueva_imagen = pygame.transform.scale(image, (w*scale, h*scale))
    return nueva_imagen

animciones = []
for i in range(7):
    img = pygame.image.load(f"images//characteres//characteres//JUGADOR//Walking_KG_1_{i+1}.png").convert_alpha()
    img = escalar_img(img, constantes.SCALA_PERSONAJE)
    animciones.append(img)

imagen_pistola = pygame.image.load(f"images//characteres//characteres//weapons//gun.png").convert_alpha()
imagen_pistola = escalar_img(imagen_pistola, constantes.SCALA_ARMA)



jugador = Personaje(50,50,animciones)

pistola = Weapon(imagen_pistola)

#definir variables de movimiento del jugador

mover_arriba = False
mover_abajo = False
mover_derecha = False
mover_izquierda = False
#controlar el frame rate
reloj = pygame.time.Clock()

run = True

while run:

    #que vaya a 60 fps
    reloj.tick(constantes.FPS)


    ventana.fill(constantes.COLOR_BG)
    #calcular el movimiento del jugador
    delta_x = 0
    delta_y = 0
    if mover_arriba:
        delta_y = -constantes.VELOCIDAD
    if mover_abajo:
        delta_y = constantes.VELOCIDAD
    if mover_derecha:
        delta_x = constantes.VELOCIDAD
    if mover_izquierda:
        delta_x = -constantes.VELOCIDAD

    #mover al jugador
    jugador.movimiento(delta_x, delta_y)
    #actualiza el estado del jugador
    jugador.update()
    pistola.update(jugador)

    #actualiza el arma




    jugador.dibujar(ventana)
    pistola.dibujar(ventana)

    for event in pygame.event.get():


        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                mover_izquierda = True
            if event.key == pygame.K_d:
                mover_derecha = True
            if event.key == pygame.K_s:
                mover_abajo = True
            if event.key == pygame.K_w:
                mover_arriba = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                mover_izquierda = False
            if event.key == pygame.K_d:
                mover_derecha = False
            if event.key == pygame.K_s:
                mover_abajo = False
            if event.key == pygame.K_w:
                mover_arriba = False

    pygame.display.update()

pygame.quit()