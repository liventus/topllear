import pygame
import sys

pygame.init()
pygame.mixer.init()

ANCHO = 800
ALTO = 600
FPS = 60

ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Mi nuevo juego")

reloj = pygame.time.Clock()

# Cargar imagen de inicio
imagen_inicio = pygame.image.load("images/topgear/intro.png").convert()
imagen_inicio = pygame.transform.scale(imagen_inicio, (ANCHO, ALTO))

# Cargar música
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

tiempo_inicio = pygame.time.get_ticks()  # tiempo inicial
duracion = 10000  # 10 segundos en milisegundos

mostrar_inicio = True

while mostrar_inicio:
    reloj.tick(FPS)

    ventana.blit(imagen_inicio, (0, 0))

    # Texto opcional
    fuente = pygame.font.SysFont("arial", 32)
    texto = fuente.render("cargando...", True, (255, 255, 255))
    ventana.blit(texto, (320, 520))

    tiempo_actual = pygame.time.get_ticks()

    # Si pasan 10 segundos → fade out y salir
    if tiempo_actual - tiempo_inicio > duracion:
        fade_out()
        mostrar_inicio = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                fade_out()
                mostrar_inicio = False

    pygame.display.update()


# Aquí empieza tu juego real
#pygame.mixer.music.stop()
angulo = 360
mostrar_press_start = False
tiempo_final_titulo = None

fondo = pygame.image.load("images/topgear/intro.png").convert()
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

titulo = pygame.image.load("images/topgear/intro.png").convert_alpha()
titulo = pygame.transform.scale(titulo, (400, 150))
while True:
    reloj.tick(FPS)

    ventana.blit(fondo, (0, 0))

    # Título girando
    if angulo > 0:
        angulo -= 4
    else:
        angulo = 0
        if tiempo_final_titulo is None:
            tiempo_final_titulo = pygame.time.get_ticks()

    titulo_rotado = pygame.transform.rotate(titulo, angulo)
    rect_titulo = titulo_rotado.get_rect(center=(ANCHO // 2, ALTO // 2 - 80))
    ventana.blit(titulo_rotado, rect_titulo)

    # Luego de 1 segundo aparece PRESS START
    if tiempo_final_titulo is not None:
        if pygame.time.get_ticks() - tiempo_final_titulo > 1000:
            mostrar_press_start = True

    if mostrar_press_start:
        fuente = pygame.font.SysFont("arial", 38)
        texto = fuente.render("PRESS START", True, (255, 255, 255))
        rect_texto = texto.get_rect(center=(ANCHO // 2, ALTO // 2 + 120))
        ventana.blit(texto, rect_texto)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and mostrar_press_start:
                print("Empieza el juego")
                # aquí luego llamas a tu juego principal

    pygame.display.update()