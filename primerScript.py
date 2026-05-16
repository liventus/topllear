import pygame
import sys
import math


numeros = {
    "0": [[1,1,1],[1,0,1],[1,0,1],[1,0,1],[1,1,1]],
    "1": [[0,0,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1]],
    "2": [[1,1,1],[0,0,1],[1,1,1],[1,0,0],[1,1,1]],
    "3": [[1,1,1],[0,0,1],[1,1,1],[0,0,1],[1,1,1]],
    "4": [[1,0,1],[1,0,1],[1,1,1],[0,0,1],[0,0,1]],
    "5": [[1,1,1],[1,0,0],[1,1,1],[0,0,1],[1,1,1]],
    "6": [[1,1,1],[1,0,0],[1,1,1],[1,0,1],[1,1,1]],
    "7": [[1,1,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1]],
    "8": [[1,1,1],[1,0,1],[1,1,1],[1,0,1],[1,1,1]],
    "9": [[1,1,1],[1,0,1],[1,1,1],[0,0,1],[1,1,1]]
}
global velocidad_auto
pygame.init()
pygame.mixer.init()

velocidad_auto = 0
velocidad_max = 200
aceleracion = velocidad_max / 5

ANCHO = 800
ALTO = 600
FPS = 60

tiempo_inicio_conteo = None

ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("TOPLLEAR")
reloj = pygame.time.Clock()
# velocidad del auto


# movimiento lateral de pista
curva_pista = 0

tiempo_inicio_conteo = None
conteo_terminado = False
fase_carrera = "intro"

def dibujar_numero_display(numero, x, y, tamaño=8):
    matriz = numeros[str(numero)]

    for fila in range(len(matriz)):
        for col in range(len(matriz[fila])):
            if matriz[fila][col] == 1:
                pygame.draw.rect(
                    ventana,
                    (255, 0, 0),
                    (x + col * tamaño, y + fila * tamaño, tamaño, tamaño)
                )


def dibujar_barra_velocidad(velocidad):
    x_inicio = 40
    y_inicio = 540
    ancho = 14
    alto = 22
    separacion = 3

    total = 20
    activos = int((velocidad / velocidad_max) * total)

    for i in range(total):
        x = x_inicio + i * (ancho + separacion)

        if i < 7:
            color = (0, 255, 0)
        elif i < 14:
            color = (255, 255, 0)
        else:
            color = (255, 0, 0)

        if i >= activos:
            color = (40, 40, 40)

        pygame.draw.rect(ventana, color, (x, y_inicio, ancho, alto))


def dibujar_hud_velocidad():
    pygame.draw.rect(ventana, (0, 0, 0), (30, 520, 420, 65))

    dibujar_barra_velocidad(velocidad_auto)

    texto = str(int(velocidad_auto)).zfill(3)

    x = 330
    for digito in texto:
        dibujar_numero_display(digito, x, 530, 8)
        x += 32

def dibujar_auto(progreso):
    auto_ancho = int(45 + progreso * 85)
    auto_alto = int(28 + progreso * 52)

    auto = pygame.transform.scale(auto_jugador, (auto_ancho, auto_alto))

    auto_x = ANCHO // 2 - auto_ancho // 2
    auto_y = int(300 + progreso * 130)

    ventana.blit(auto, (auto_x, auto_y))

def cargar_imagen(ruta, size=None, alpha=False):
    img = pygame.image.load(ruta).convert_alpha() if alpha else pygame.image.load(ruta).convert()
    if size:
        img = pygame.transform.scale(img, size)
    return img


# =========================
# INTRO 1
# =========================

imagen_inicio = cargar_imagen("images/topgear/intro.png", (ANCHO, ALTO))
imagen_inicio2 = cargar_imagen("images/topgear/img.png", (130, 30))

pygame.mixer.music.load("images/sonido/intro.mp3")
pygame.mixer.music.play(-1)


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


fade_in()

tiempo_inicio = pygame.time.get_ticks()
duracion = 10000

fade_logo_in = 1500
tiempo_visible = 3500
fade_logo_out = 1500

mostrar_inicio = True

while mostrar_inicio:
    reloj.tick(FPS)

    tiempo_actual = pygame.time.get_ticks()
    tiempo_pasado = tiempo_actual - tiempo_inicio

    ventana.blit(imagen_inicio, (0, 0))

    alpha = 0

    if tiempo_pasado < fade_logo_in:
        alpha = int((tiempo_pasado / fade_logo_in) * 255)
    elif tiempo_pasado < fade_logo_in + tiempo_visible:
        alpha = 255
    elif tiempo_pasado < fade_logo_in + tiempo_visible + fade_logo_out:
        tiempo_salida = tiempo_pasado - fade_logo_in - tiempo_visible
        alpha = int(255 - (tiempo_salida / fade_logo_out) * 255)

    if alpha > 0:
        logo = imagen_inicio2.copy()
        logo.set_alpha(alpha)
        ventana.blit(logo, (320, 330))

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


# =========================
# IMÁGENES DEL MENÚ
# =========================

fondo = cargar_imagen("images/topgear/img_5.png", (ANCHO, ALTO))

titulo = cargar_imagen("images/topgear/top.png", (400, 150), True)
gear = cargar_imagen("images/topgear/gear.png", (400, 150), True)

menu_img_6 = cargar_imagen("images/topgear/img_6.png", (ANCHO, ALTO))
menu_img_7 = cargar_imagen("images/topgear/img_7.png", (ANCHO, ALTO))
sub_menu = cargar_imagen("images/topgear/img_9.png", (ANCHO, ALTO))
pantalla_carrera = cargar_imagen("images/topgear/mapa.png", (ANCHO, ALTO))
pantalla_carga = cargar_imagen("images/topgear/img_12.png", (ANCHO, ALTO))

# =========================
# IMÁGENES DE LA INTRO CARRERA
# =========================

road_texture = cargar_imagen("images/topgear/auto/road2.png")
auto_jugador = cargar_imagen("images/topgear/auto/img.png", alpha=True)


# =========================
# VARIABLES INTRO CARRERA
# =========================

distancia_meta = 200
velocidad_intro = 0.75
intro_carrera_terminada = False
offset_pista = 0


def reiniciar_intro_carrera():
    global distancia_meta, intro_carrera_terminada, offset_pista
    global tiempo_inicio_conteo, conteo_terminado, velocidad_auto
    global fase_carrera

    distancia_meta = 200
    intro_carrera_terminada = False
    offset_pista = 0
    tiempo_inicio_conteo = None
    conteo_terminado = False
    velocidad_auto = 0
    fase_carrera = "intro"

def dibujar_fondo_carrera():
    # Cielo
    for y in range(0, 240):
        r = 70 + int(y * 0.25)
        g = 165 + int(y * 0.18)
        b = 235
        pygame.draw.line(ventana, (r, g, b), (0, y), (ANCHO, y))

    # Sol
    pygame.draw.circle(ventana, (255, 225, 90), (665, 80), 45)
    pygame.draw.circle(ventana, (255, 245, 160), (665, 80), 28)

    # Montañas
    pygame.draw.polygon(ventana, (150, 105, 80), [(0, 240), (130, 105), (285, 240)])
    pygame.draw.polygon(ventana, (175, 125, 90), [(180, 240), (395, 75), (620, 240)])
    pygame.draw.polygon(ventana, (140, 95, 70), [(510, 240), (690, 110), (850, 240)])

    pygame.draw.polygon(ventana, (210, 160, 105), [(0, 260), (230, 155), (450, 260)])
    pygame.draw.polygon(ventana, (195, 145, 95), [(370, 260), (590, 150), (820, 260)])

    # Desierto
    pygame.draw.rect(ventana, (210, 155, 90), (0, 240, ANCHO, ALTO))


def dibujar_pista_textura(progreso):
    global offset_pista

    if fase_carrera == "intro":
        offset_pista -= 6
    elif fase_carrera == "carrera":
        offset_pista -= velocidad_auto * 0.10

    dibujar_fondo_carrera()

    horizonte_y = 260
    segmentos = 180

    for i in range(segmentos):
        t1 = i / segmentos
        t2 = (i + 1) / segmentos

        y1 = int(horizonte_y + t1 * (ALTO - horizonte_y))
        y2 = int(horizonte_y + t2 * (ALTO - horizonte_y))

        if y2 <= y1:
            continue

        ancho1 = int(120 + t1 * 2500)
        ancho2 = int(120 + t2 * 2500)

        x1 = ANCHO // 2 - ancho1 // 2
        x2 = ANCHO // 2 - ancho2 // 2

        textura_h = road_texture.get_height()
        textura_w = road_texture.get_width()

        slice_h = 2

        # perspectiva correcta:
        # arriba = más comprimido
        # abajo = más estirado
        profundidad = t1
        textura_pos = offset_pista + (profundidad * profundidad * textura_h)

        slice_y = int(textura_pos) % (textura_h - slice_h)

        road_slice = road_texture.subsurface((0, slice_y, textura_w, slice_h))
        road_slice = pygame.transform.smoothscale(road_slice, (ancho2, y2 - y1))

        mascara = pygame.Surface((ANCHO, y2 - y1), pygame.SRCALPHA)

        puntos = [
            (x1, 0),
            (x1 + ancho1, 0),
            (x2 + ancho2, y2 - y1),
            (x2, y2 - y1)
        ]

        pygame.draw.polygon(mascara, (255, 255, 255, 255), puntos)

        temp = pygame.Surface((ANCHO, y2 - y1), pygame.SRCALPHA)
        temp.blit(road_slice, (x2, 0))
        temp.blit(mascara, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        ventana.blit(temp, (0, y1))


def dibujar_meta_y_auto(progreso):
    # Meta acercándose
    meta_y = int(120 + progreso * 260)
    meta_ancho = int(130 + progreso * 560)
    meta_alto = int(30 + progreso * 70)
    meta_x = ANCHO // 2 - meta_ancho // 2

    poste_alto = meta_alto + 120

    pygame.draw.rect(ventana, (50, 50, 50), (meta_x + 12, meta_y, 14, poste_alto))
    pygame.draw.rect(ventana, (50, 50, 50), (meta_x + meta_ancho - 26, meta_y, 14, poste_alto))

    pygame.draw.rect(ventana, (15, 15, 15), (meta_x - 5, meta_y - 5, meta_ancho + 10, meta_alto + 10))

    cuadros_x = 14
    cuadros_y = 2
    cuadro_w = meta_ancho / cuadros_x
    cuadro_h = meta_alto / cuadros_y

    for fila in range(cuadros_y):
        for col in range(cuadros_x):
            color = (20, 20, 20) if (fila + col) % 2 == 0 else (245, 245, 245)
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

    # Texto START
    fuente_meta = pygame.font.SysFont("arial", int(22 + progreso * 24), bold=True)
    texto_meta = fuente_meta.render("START", True, (255, 255, 255))
    ventana.blit(
        texto_meta,
        (ANCHO // 2 - texto_meta.get_width() // 2, meta_y + meta_alto + 10)
    )

    # Auto esperando en la meta
    auto_ancho = int(40 + progreso * 150)
    auto_alto = int(25 + progreso * 75)

    auto = pygame.transform.scale(auto_jugador, (auto_ancho, auto_alto))
    auto_x = ANCHO // 2 - auto_ancho // 2

    auto_y = int((meta_y + meta_alto + 95) + progreso * 40)

    if progreso >= 1:
        auto_y = 430

    ventana.blit(auto, (auto_x, auto_y))


def dibujar_intro_carrera():
    global distancia_meta, intro_carrera_terminada
    global tiempo_inicio_conteo, conteo_terminado, fase_carrera

    if fase_carrera == "intro":
        distancia_meta -= velocidad_intro

        if distancia_meta <= 0:
            distancia_meta = 0
            intro_carrera_terminada = True
            fase_carrera = "conteo"
            tiempo_inicio_conteo = pygame.time.get_ticks()

    progreso = 1 - (distancia_meta / 200)

    dibujar_pista_textura(progreso)
    dibujar_auto(progreso)

    fuente = pygame.font.SysFont("arial", 30, bold=True)

    texto = fuente.render(f"{int(distancia_meta)} m", True, (255, 255, 255))
    sombra = fuente.render(f"{int(distancia_meta)} m", True, (0, 0, 0))

    ventana.blit(sombra, (32, 32))
    ventana.blit(texto, (30, 30))

    if fase_carrera == "conteo":
        tiempo_pasado = pygame.time.get_ticks() - tiempo_inicio_conteo

        if tiempo_pasado < 1000:
            numero = "3"
        elif tiempo_pasado < 2000:
            numero = "2"
        elif tiempo_pasado < 3000:
            numero = "1"
        else:
            numero = ""
            conteo_terminado = True
            fase_carrera = "carrera"

        if numero != "":
            fuente_conteo = pygame.font.SysFont("arial", 90, bold=True)
            texto2 = fuente_conteo.render(numero, True, (255, 255, 255))
            sombra2 = fuente_conteo.render(numero, True, (0, 0, 0))

            x = ANCHO // 2 - texto2.get_width() // 2
            y = 250

            ventana.blit(sombra2, (x + 4, y + 4))
            ventana.blit(texto2, (x, y))


# =========================
# VARIABLES MENÚ
# =========================

angulo = 360
angulo_gear = 360
mostrar_press_start = False
tiempo_final_titulo = None

y_titulo = -10
y_final = 140

y_gear = 650
y_gearfinal = 230

velocidad = 5

escala = 0.001
escala_final = 1.0
velocidad_escala = 0.01

mostrar_gear = False
delay_gear = 1000

tiempo_estado = 0
estado = "intro_menu"
opcion_menu = "img_6"
musica_juego_iniciada = False


# =========================
# LOOP PRINCIPAL
# =========================

while True:
    reloj.tick(FPS)

    # =========================
    # MENÚ DE OPCIONES
    # =========================
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

    # =========================
    # SUBMENÚ
    # =========================
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

    # =========================
    # MAPA
    # =========================
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

    # =========================
    # CARGA
    # =========================
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

    # =========================
    # INTRO CARRERA
    # =========================
    if estado == "juego_final":

        dt = reloj.get_time() / 1000

        if fase_carrera == "carrera":
            teclas = pygame.key.get_pressed()

            if teclas[pygame.K_SPACE]:
                velocidad_auto += aceleracion * dt

                if velocidad_auto > velocidad_max:
                    velocidad_auto = velocidad_max
            else:
                velocidad_auto -= aceleracion * dt * 0.5

                if velocidad_auto < 0:
                    velocidad_auto = 0

        dibujar_intro_carrera()

        if fase_carrera == "carrera":
            dibujar_hud_velocidad()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    estado = "menu_opciones"

        pygame.display.update()
        continue

    # =========================
    # INTRO MENÚ TOP GEAR
    # =========================

    ventana.blit(fondo, (0, 0))

    if y_titulo < y_final:
        y_titulo += velocidad
    else:
        y_titulo = y_final

    if escala < escala_final:
        escala += velocidad_escala
    else:
        escala = escala_final

    if y_titulo == y_final and escala == escala_final:
        if tiempo_final_titulo is None:
            tiempo_final_titulo = pygame.time.get_ticks()

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

    nuevo_ancho = int(400 * escala)
    nuevo_alto = int(150 * escala)

    titulo_escalado = pygame.transform.scale(titulo, (nuevo_ancho, nuevo_alto))
    gear_escalado = pygame.transform.scale(gear, (nuevo_ancho, nuevo_alto))

    titulo_final = pygame.transform.rotate(titulo_escalado, angulo)
    gear_final = pygame.transform.rotate(gear_escalado, angulo_gear)

    rect_titulo = titulo_final.get_rect()
    rect_titulo.x = 200
    rect_titulo.y = y_titulo

    rect_gear = gear_final.get_rect()
    rect_gear.x = 230
    rect_gear.y = y_gear

    ventana.blit(titulo_final, rect_titulo)

    if tiempo_final_titulo is not None:
        if pygame.time.get_ticks() - tiempo_final_titulo > delay_gear:
            mostrar_gear = True

    if mostrar_gear:
        ventana.blit(gear_final, rect_gear)

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