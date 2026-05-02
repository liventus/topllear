import pygame
import sys

pygame.init()
pygame.mixer.init()

ANCHO = 800
ALTO = 600
FPS = 60

ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("TOPLLEAR")
# INICIO INTRO 1
reloj = pygame.time.Clock()

# Cargar imagen de inicio
imagen_inicio = pygame.image.load("images/topgear/intro.png").convert()
imagen_inicio2 = pygame.image.load("images/topgear/img.png").convert()
imagen_inicio = pygame.transform.scale(imagen_inicio, (ANCHO, ALTO))
imagen_inicio2 = pygame.transform.scale(imagen_inicio2, (130, 30))

#aca cargo la musica
pygame.mixer.music.load("images/sonido/intro.mp3")
pygame.mixer.music.play(-1)  # -1 para que se repita


def fade_in():
    oscuridad = pygame.Surface((ANCHO, ALTO))
    oscuridad.fill((0, 0, 0))

    for alpha in range(255, -1, -5):
        ventana.blit(imagen_inicio, (0, 0))
        oscuridad.set_alpha(alpha)
        ventana.blit(oscuridad, (0, 0))
        pygame.display.update()
        reloj.tick(FPS)


def fade_out():
    oscuridad = pygame.Surface((ANCHO, ALTO))
    oscuridad.fill((0, 0, 0))

    for alpha in range(0, 256, 5):
        ventana.blit(imagen_inicio, (0, 0))
        oscuridad.set_alpha(alpha)
        ventana.blit(oscuridad, (0, 0))
        pygame.display.update()
        reloj.tick(FPS)


# Aparece desde oscuro
fade_in()

tiempo_inicio = pygame.time.get_ticks()
duracion = 7000

fade_logo_in = 1500     # aparece en 1.5 segundos
tiempo_visible = 3500   # se queda visible
fade_logo_out = 1500    # desaparece en 1.5 segundos


mostrar_inicio = True

while mostrar_inicio:
    reloj.tick(FPS)

    tiempo_actual = pygame.time.get_ticks()
    tiempo_pasado = tiempo_actual - tiempo_inicio

    ventana.blit(imagen_inicio, (0, 0))

    # Calcular opacidad de imagen_inicio2
    alpha = 0

    if tiempo_pasado < fade_logo_in:
        alpha = int((tiempo_pasado / fade_logo_in) * 255)

    elif tiempo_pasado < fade_logo_in + tiempo_visible:
        alpha = 255

    elif tiempo_pasado < fade_logo_in + tiempo_visible + fade_logo_out:
        tiempo_salida = tiempo_pasado - fade_logo_in - tiempo_visible
        alpha = int(255 - (tiempo_salida / fade_logo_out) * 255)

    else:
        alpha = 0

    # Dibujar imagen_inicio2 con transparencia
    if alpha > 0:
        logo = imagen_inicio2.copy()
        logo.set_alpha(alpha)

        rect_logo = logo.get_rect()
        rect_logo.x = 320
        rect_logo.y = 330

        ventana.blit(logo, rect_logo)


        ventana.blit(logo, rect_logo)

    # Cuando termina todo, recién desaparece el fondo
    if tiempo_pasado > duracion:
        fade_out()
        mostrar_inicio = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                fade_out()
                mostrar_inicio = False

    pygame.display.update()


# FIN INTRO 1
#pygame.mixer.music.stop()
angulo = 360
angulo_gear = 360
mostrar_press_start = False
tiempo_final_titulo = None

fondo = pygame.image.load("images/topgear/img_5.png").convert()
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

titulo = pygame.image.load("images/topgear/top.png").convert_alpha()
titulo = pygame.transform.scale(titulo, (400, 150))

gear = pygame.image.load("images/topgear/gear.png").convert_alpha()
gear = pygame.transform.scale(gear, (400, 150))

y_titulo = -10
y_final = 140

y_gear = 650   # empieza FUERA de pantalla (abajo)
y_gearfinal = 230

velocidad = 5

escala = 0.001
escala_final = 1.0
velocidad_escala = 0.01


mostrar_gear = False
delay_gear = 500  # milisegundos (0.5 segundos después del top)
while True:
    reloj.tick(FPS)

    ventana.blit(fondo, (0, 0))
    if y_titulo < y_final:
        y_titulo += velocidad
    else:
        y_titulo = y_final




    if escala < escala_final:
        escala += velocidad_escala
    else:
        escala = escala_final

    # Cuando ya llegó y ya creció, empieza el contador para PRESS START
    if y_titulo == y_final and escala == escala_final:
        if tiempo_final_titulo is None:
            tiempo_final_titulo = pygame.time.get_ticks()

    # Rotación
    if angulo > 0:
        angulo -= 4
    else:
        angulo = 0

    if mostrar_gear:
        if angulo_gear > 0:
            angulo_gear -= 4
        else:
            angulo_gear = 0

    if mostrar_gear:
        if y_gear > y_gearfinal:
            y_gear -= velocidad
        else:
            y_gear = y_gearfinal
    # Escalar primero
    nuevo_ancho = int(400 * escala)
    nuevo_alto = int(150 * escala)

    titulo_escalado = pygame.transform.scale(titulo, (nuevo_ancho, nuevo_alto))
    gear_escalado = pygame.transform.scale(gear, (nuevo_ancho, nuevo_alto))

    # Rotar después de escalar
    titulo_final = pygame.transform.rotate(titulo_escalado, angulo)
    gear_final = pygame.transform.rotate(gear_escalado, angulo_gear)

    # Posición manual centrada
    rect_titulo = titulo_final.get_rect()
    rect_titulo.x =200
    rect_titulo.y = y_titulo

    # Posición gear
    rect_gear = gear_final.get_rect()
    rect_gear.x = 230
    rect_gear.y = y_gear

    ventana.blit(titulo_final, rect_titulo)


    if tiempo_final_titulo is not None:
        if pygame.time.get_ticks() - tiempo_final_titulo > delay_gear:
            mostrar_gear = True

    if mostrar_gear:
        ventana.blit(gear_final, rect_gear)

    # Luego de 1 segundo aparece PRESS START
    if tiempo_final_titulo is not None:
        if pygame.time.get_ticks() - tiempo_final_titulo > 1500:
            mostrar_press_start = True

    if mostrar_press_start:
        fuente = pygame.font.SysFont("arial", 38)
        texto = fuente.render("PRESS START", True, (255, 255, 255))

        rect_texto = texto.get_rect()
        rect_texto.x = ANCHO // 2 - rect_texto.width // 2
        rect_texto.y = ALTO // 2 + 120

        ventana.blit(texto, rect_texto)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and mostrar_press_start:
                print("Empieza el juego")

    pygame.display.update()