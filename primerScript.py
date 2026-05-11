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


# =========================
# INTRO CARRERA TOP GEAR
# =========================

distancia_meta = 200
velocidad_intro = 0.9
intro_carrera_terminada = False
offset_pista = 0


def interpolar(a, b, t):
    return a + (b - a) * t


def reiniciar_intro_carrera():
    global distancia_meta, intro_carrera_terminada, offset_pista
    distancia_meta = 200
    intro_carrera_terminada = False
    offset_pista = 0


def dibujar_intro_pista():
    global distancia_meta, intro_carrera_terminada, offset_pista

    if not intro_carrera_terminada:
        distancia_meta -= velocidad_intro
        offset_pista += 9

        if distancia_meta <= 0:
            distancia_meta = 0
            intro_carrera_terminada = True

    progreso = 1 - (distancia_meta / 200)

    # =====================
    # CIELO CON DEGRADADO
    # =====================
    for y in range(0, ALTO):
        if y < 230:
            r = 80 + int(y * 0.25)
            g = 170 + int(y * 0.15)
            b = 235
            pygame.draw.line(ventana, (r, g, b), (0, y), (ANCHO, y))
        else:
            break

    # SOL
    pygame.draw.circle(ventana, (255, 220, 90), (670, 85), 45)
    pygame.draw.circle(ventana, (255, 240, 150), (670, 85), 30)

    # =====================
    # MONTAÑAS
    # =====================
    pygame.draw.polygon(ventana, (155, 105, 75), [(0, 230), (120, 115), (260, 230)])
    pygame.draw.polygon(ventana, (175, 120, 80), [(180, 230), (380, 80), (590, 230)])
    pygame.draw.polygon(ventana, (145, 95, 70), [(500, 230), (680, 105), (850, 230)])

    pygame.draw.polygon(ventana, (205, 155, 105), [(0, 250), (220, 150), (430, 250)])
    pygame.draw.polygon(ventana, (195, 145, 95), [(360, 250), (580, 145), (820, 250)])

    # =====================
    # SUELO / DESIERTO
    # =====================
    pygame.draw.rect(ventana, (210, 155, 90), (0, 230, ANCHO, ALTO))

    # franjas laterales para velocidad
    for i in range(18):
        y = 230 + ((i * 38 + offset_pista * 0.8) % 370)
        grosor = 8 + int((y - 230) / 18)
        color = (225, 175, 100) if i % 2 == 0 else (195, 135, 75)

        pygame.draw.rect(ventana, color, (0, y, 180, grosor))
        pygame.draw.rect(ventana, color, (620, y, 180, grosor))

    # =====================
    # CARRETERA PRINCIPAL
    # =====================
    carretera_top_y = 205
    carretera_bottom_y = 600

    izquierda_arriba = 340
    derecha_arriba = 460
    izquierda_abajo = -40
    derecha_abajo = 840

    pygame.draw.polygon(
        ventana,
        (32, 38, 42),
        [
            (izquierda_arriba, carretera_top_y),
            (derecha_arriba, carretera_top_y),
            (derecha_abajo, carretera_bottom_y),
            (izquierda_abajo, carretera_bottom_y)
        ]
    )

    # sombra central
    pygame.draw.polygon(
        ventana,
        (42, 48, 52),
        [
            (380, carretera_top_y),
            (420, carretera_top_y),
            (560, carretera_bottom_y),
            (240, carretera_bottom_y)
        ]
    )

    # =====================
    # FUNCIÓN DE PERSPECTIVA
    # =====================
    def punto_pista(x_top, x_bottom, escala):
        return interpolar(x_top, x_bottom, escala)

    # =====================
    # BORDES ROJO / BLANCO
    # =====================
    for i in range(22):
        y = carretera_top_y + ((i * 38 + offset_pista) % 430)
        escala = (y - carretera_top_y) / (carretera_bottom_y - carretera_top_y)

        izq = punto_pista(izquierda_arriba, izquierda_abajo, escala)
        der = punto_pista(derecha_arriba, derecha_abajo, escala)

        ancho_borde = 18 + escala * 55
        alto_borde = 8 + escala * 22

        color = (230, 30, 30) if i % 2 == 0 else (245, 245, 245)

        pygame.draw.polygon(
            ventana,
            color,
            [
                (izq - ancho_borde, y),
                (izq + 8, y),
                (izq + 18, y + alto_borde),
                (izq - ancho_borde - 20, y + alto_borde)
            ]
        )

        pygame.draw.polygon(
            ventana,
            color,
            [
                (der - 8, y),
                (der + ancho_borde, y),
                (der + ancho_borde + 20, y + alto_borde),
                (der - 18, y + alto_borde)
            ]
        )

    # =====================
    # LÍNEAS CENTRALES
    # =====================
    for i in range(12):
        y = carretera_top_y + 20 + ((i * 70 + offset_pista * 1.4) % 430)
        escala = (y - carretera_top_y) / (carretera_bottom_y - carretera_top_y)

        ancho = 5 + escala * 18
        largo = 20 + escala * 70

        x = ANCHO // 2

        pygame.draw.polygon(
            ventana,
            (235, 235, 220),
            [
                (x - ancho, y),
                (x + ancho, y),
                (x + ancho * 2, y + largo),
                (x - ancho * 2, y + largo)
            ]
        )



    # =====================
    # META ACERCÁNDOSE
    # =====================
    meta_y = interpolar(130, 390, progreso)
    meta_ancho = interpolar(120, 620, progreso)
    meta_alto = interpolar(28, 90, progreso)
    meta_x = ANCHO // 2 - meta_ancho // 2

    poste_alto = meta_alto + 110

    pygame.draw.rect(ventana, (60, 60, 60), (meta_x + 12, meta_y, 14, poste_alto))
    pygame.draw.rect(ventana, (60, 60, 60), (meta_x + meta_ancho - 26, meta_y, 14, poste_alto))

    pygame.draw.rect(ventana, (20, 20, 20), (meta_x - 4, meta_y - 4, meta_ancho + 8, meta_alto + 8))
    pygame.draw.rect(ventana, (240, 240, 240), (meta_x, meta_y, meta_ancho, meta_alto))

    cuadros_x = 14
    cuadros_y = 2
    cuadro_w = meta_ancho / cuadros_x
    cuadro_h = meta_alto / cuadros_y

    for fila in range(cuadros_y):
        for col in range(cuadros_x):
            if (fila + col) % 2 == 0:
                color = (20, 20, 20)
            else:
                color = (245, 245, 245)

            pygame.draw.rect(
                ventana,
                color,
                (
                    meta_x + col * cuadro_w,
                    meta_y + fila * cuadro_h,
                    cuadro_w,
                    cuadro_h
                )
            )

    fuente_meta = pygame.font.SysFont("arial", int(22 + progreso * 24), bold=True)
    texto_meta = fuente_meta.render("START", True, (255, 255, 255))
    ventana.blit(
        texto_meta,
        (ANCHO // 2 - texto_meta.get_width() // 2, meta_y + meta_alto + 12)
    )

    # =====================
    # AUTO AL LLEGAR A META
    # =====================
    if intro_carrera_terminada:
        auto_x = ANCHO // 2 - 85
        auto_y = 430

        auto = pygame.image.load("images/topgear/auto/img.png").convert_alpha()
        # El auto empieza pequeño porque está lejos,
        # y crece mientras la cámara se acerca a la meta.
        auto_ancho = int(45 + progreso * 125)
        auto_alto = int(25 + progreso * 65)

        auto = pygame.transform.scale(auto, (auto_ancho, auto_alto))

        auto_x = ANCHO // 2 - auto_ancho // 2

        # Se mantiene ubicado sobre la pista, cerca de la línea de meta
        auto_y = int(interpolar(meta_y + meta_alto + 120, 430, progreso))

        ventana.blit(auto, (auto_x, auto_y))

    # =====================
    # HUD
    # =====================
    fuente = pygame.font.SysFont("arial", 30, bold=True)

    texto = fuente.render(f"{int(distancia_meta)} m", True, (255, 255, 255))
    sombra = fuente.render(f"{int(distancia_meta)} m", True, (0, 0, 0))

    ventana.blit(sombra, (32, 32))
    ventana.blit(texto, (30, 30))

    if intro_carrera_terminada:
        texto2 = fuente.render("EN META - ESPERANDO CONTEO", True, (255, 255, 255))
        sombra2 = fuente.render("EN META - ESPERANDO CONTEO", True, (0, 0, 0))

        x = ANCHO // 2 - texto2.get_width() // 2
        ventana.blit(sombra2, (x + 2, 542))
        ventana.blit(texto2, (x, 540))

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
duracion = 10000

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
delay_gear = 1000  # milisegundos (0.5 segundos después del top)

pantalla_juego = pygame.image.load("images/topgear/img_6.png").convert()
pantalla_juego = pygame.transform.scale(pantalla_juego, (ANCHO, ALTO))
en_juego = False
ventana.blit(fondo, (0, 0))

menu_img_6 = pygame.image.load("images/topgear/img_6.png").convert()
menu_img_6 = pygame.transform.scale(menu_img_6, (ANCHO, ALTO))

menu_img_7 = pygame.image.load("images/topgear/img_7.png").convert()
menu_img_7 = pygame.transform.scale(menu_img_7, (ANCHO, ALTO))

sub_menu = pygame.image.load("images/topgear/img_9.png").convert()
sub_menu = pygame.transform.scale(sub_menu, (ANCHO, ALTO))

pantalla_carrera = pygame.image.load("images/topgear/mapa.png").convert()
pantalla_carrera = pygame.transform.scale(pantalla_carrera, (ANCHO, ALTO))

pantalla_carga = pygame.image.load("images/topgear/img_12.png").convert()
pantalla_carga = pygame.transform.scale(pantalla_carga, (ANCHO, ALTO))

pantalla_juego_final = pygame.image.load("images/topgear/juegocomotal.png").convert()
pantalla_juego_final = pygame.transform.scale(pantalla_juego_final, (ANCHO, ALTO))

tiempo_estado = 0

estado = "intro_menu"
opcion_menu = "img_6"
musica_juego_iniciada = False
while True:
    reloj.tick(FPS)
    if estado == "menu_opciones":

        if opcion_menu == "img_6":
            ventana.blit(menu_img_6, (0, 0))
        elif opcion_menu == "img_7":
            ventana.blit(menu_img_7, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_s:
                    opcion_menu = "img_7"

                if event.key == pygame.K_w:
                    opcion_menu = "img_6"

                if event.key == pygame.K_RETURN:
                    if opcion_menu == "img_6":
                        estado = "submenu"


                    elif opcion_menu == "img_7":

                        estado = "mapa"

                        tiempo_estado = pygame.time.get_ticks()

        pygame.display.update()
        continue

    if estado == "submenu":
        ventana.blit(sub_menu, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    estado = "menu_opciones"
                    opcion_menu = "img_6"

        pygame.display.update()
        continue

    if estado == "mapa":
        ventana.blit(pantalla_carrera, (0, 0))

        if pygame.time.get_ticks() - tiempo_estado > 3000:
            estado = "carga_juego"
            tiempo_estado = pygame.time.get_ticks()

            if not musica_juego_iniciada:
                pygame.mixer.music.load("images/sonido/lasvegas.mp3")
                pygame.mixer.music.play(-1)
                musica_juego_iniciada = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        continue

    if estado == "carga_juego":
        ventana.blit(pantalla_carga, (0, 0))

        if pygame.time.get_ticks() - tiempo_estado > 2000:
            reiniciar_intro_carrera()
            estado = "juego_final"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        continue

    if estado == "juego_final":
        dibujar_intro_pista()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    estado = "menu_opciones"

        pygame.display.update()
        continue

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
                estado = "menu_opciones"

    pygame.display.update()