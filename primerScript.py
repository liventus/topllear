import pygame
import sys


pygame.init()
pygame.mixer.init()

ANCHO = 800
ALTO = 600
ALTO_PANTALLA = ALTO // 2
FPS = 60

ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("TOPLLEAR - 2 JUGADORES")
reloj = pygame.time.Clock()

velocidad_max = 200
aceleracion = velocidad_max / 5
FACTOR_DISTANCIA = 0.15

# =========================
# MAPA DE CURVAS
# curva positiva = curva hacia la derecha visual
# curva negativa = curva hacia la izquierda visual
# =========================
mapa_curvas = [
    {"desde": 0,   "hasta": 150, "curva": 0},
    {"desde": 150, "hasta": 300, "curva": 180},
    {"desde": 300, "hasta": 400, "curva": 0},
    {"desde": 400, "hasta": 550, "curva": -180},
    {"desde": 550, "hasta": 100000, "curva": 0}
]


def obtener_curva_por_distancia(distancia):
    for tramo in mapa_curvas:
        if tramo["desde"] <= distancia < tramo["hasta"]:
            return tramo["curva"]
    return 0


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


def cargar_imagen(ruta, size=None, alpha=False):
    img = pygame.image.load(ruta).convert_alpha() if alpha else pygame.image.load(ruta).convert()
    if size:
        img = pygame.transform.scale(img, size)
    return img


# =========================
# CLASE JUGADOR
# =========================
class Jugador:
    def __init__(self, nombre, izquierda, derecha, acelerar, frenar=None, carril_inicial=0):
        self.nombre = nombre
        self.izquierda = izquierda
        self.derecha = derecha
        self.acelerar = acelerar
        self.frenar = frenar

        self.velocidad = 0
        self.distancia = 0

        # Mueve la pista/cámara propia de este jugador
        self.desplazamiento_pista = 0

        # Carril inicial y carril actual
        self.carril_inicial = carril_inicial
        self.carril = carril_inicial

        self.offset_pista = 0
        self.imagen_actual = "centro"
        self.posicion = 1

    def reiniciar(self):
        self.velocidad = 0
        self.distancia = 0
        self.desplazamiento_pista = 0
        self.carril = self.carril_inicial
        self.offset_pista = 0
        self.imagen_actual = "centro"
        self.posicion = 1


jugador1 = Jugador(
    "JUGADOR 1",
    pygame.K_a,
    pygame.K_d,
    pygame.K_w,
    pygame.K_s,
    carril_inicial=-0.45
)

jugador2 = Jugador(
    "JUGADOR 2",
    pygame.K_j,
    pygame.K_l,
    pygame.K_i,
    pygame.K_k,
    carril_inicial=0.45
)

# =========================
# CARGA DE IMÁGENES
# =========================
imagen_inicio = cargar_imagen("images/topgear/intro.png", (ANCHO, ALTO))
imagen_inicio2 = cargar_imagen("images/topgear/img.png", (130, 30))

fondo = cargar_imagen("images/topgear/img_5.png", (ANCHO, ALTO))
titulo = cargar_imagen("images/topgear/top.png", (400, 150), True)
gear = cargar_imagen("images/topgear/gear.png", (400, 150), True)

menu_img_6 = cargar_imagen("images/topgear/img_6.png", (ANCHO, ALTO))
menu_img_7 = cargar_imagen("images/topgear/img_7.png", (ANCHO, ALTO))
sub_menu = cargar_imagen("images/topgear/img_9.png", (ANCHO, ALTO))
pantalla_carrera = cargar_imagen("images/topgear/mapa.png", (ANCHO, ALTO))
pantalla_carga = cargar_imagen("images/topgear/img_12.png", (ANCHO, ALTO))

road_texture = cargar_imagen("images/topgear/auto/road2.png")
auto_jugador = cargar_imagen("images/topgear/auto/img.png", alpha=True)
auto_izquierda = cargar_imagen("images/topgear/auto/img_1.png", alpha=True)
auto_derecha = cargar_imagen("images/topgear/auto/img_2.png", alpha=True)

# =========================
# VARIABLES DE ESTADO
# =========================
tiempo_inicio_conteo = None
conteo_terminado = False
fase_carrera = "intro"
distancia_meta = 200
velocidad_intro = 0.75
musica_juego_iniciada = False

# menú
angulo = 360
angulo_gear = 360
mostrar_press_start = False
tiempo_final_titulo = None
y_titulo = -10
y_final = 140
y_gear = 650
y_gearfinal = 230
velocidad_menu = 5
escala = 0.001
escala_final = 1.0
velocidad_escala = 0.01
mostrar_gear = False
delay_gear = 1000
tiempo_estado = 0
estado = "intro_menu"
opcion_menu = "img_6"


# =========================
# FUNCIONES INTRO INICIAL
# =========================
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


# =========================
# HUD
# =========================
def dibujar_numero_display(superficie, numero, x, y, tam=5, color=(255, 0, 0)):
    matriz = numeros[str(numero)]
    for fila in range(len(matriz)):
        for col in range(len(matriz[fila])):
            if matriz[fila][col] == 1:
                pygame.draw.rect(superficie, color, (x + col * tam, y + fila * tam, tam, tam))


def dibujar_hud_jugador(superficie, jugador):
    fuente = pygame.font.SysFont("arial", 18, bold=True)
    texto = fuente.render(f"{jugador.nombre}   POS {jugador.posicion}", True, (255, 255, 255))
    sombra = fuente.render(f"{jugador.nombre}   POS {jugador.posicion}", True, (0, 0, 0))
    superficie.blit(sombra, (17, 12))
    superficie.blit(texto, (15, 10))

    panel_x = 520
    panel_y = 12
    pygame.draw.rect(superficie, (0, 0, 0), (panel_x, panel_y, 250, 52))

    total = 20
    activos = int((jugador.velocidad / velocidad_max) * total)
    x_inicio = panel_x + 8
    y_inicio = panel_y + 10
    ancho = 8
    alto = 15
    separacion = 2

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
        pygame.draw.rect(superficie, color, (x, y_inicio, ancho, alto))

    texto_vel = str(int(jugador.velocidad)).zfill(3)
    x_num = panel_x + 160
    y_num = panel_y + 28
    for digito in texto_vel:
        dibujar_numero_display(superficie, digito, x_num, y_num, 4)
        x_num += 18


# =========================
# DIBUJO DE PISTA EN UNA MITAD DE PANTALLA
# =========================
def dibujar_fondo_carrera(superficie):
    ancho = superficie.get_width()
    alto = superficie.get_height()

    for y in range(0, 120):
        r = 70 + int(y * 0.25)
        g = 165 + int(y * 0.18)
        b = 235
        pygame.draw.line(superficie, (r, g, b), (0, y), (ancho, y))

    pygame.draw.circle(superficie, (255, 225, 90), (665, 40), 30)
    pygame.draw.circle(superficie, (255, 245, 160), (665, 40), 18)

    pygame.draw.polygon(superficie, (150, 105, 80), [(0, 120), (130, 45), (285, 120)])
    pygame.draw.polygon(superficie, (175, 125, 90), [(180, 120), (395, 35), (620, 120)])
    pygame.draw.polygon(superficie, (140, 95, 70), [(510, 120), (690, 55), (850, 120)])

    pygame.draw.rect(superficie, (210, 155, 90), (0, 120, ancho, alto))


def dibujar_pista_textura(superficie, jugador):

    if fase_carrera == "carrera":
        # La pista se mueve SOLO según la velocidad del auto.
        # Si velocidad = 0, la pista queda quieta.
        jugador.offset_pista -= jugador.velocidad * 0.10

    dibujar_fondo_carrera(superficie)

    ancho = superficie.get_width()
    alto = superficie.get_height()
    horizonte_y = 125
    segmentos = 420
    curva_actual = obtener_curva_por_distancia(jugador.distancia)

    for i in range(segmentos):
        t1 = i / segmentos
        t2 = (i + 1) / segmentos

        y1 = int(horizonte_y + t1 * (alto - horizonte_y))
        y2 = int(horizonte_y + t2 * (alto - horizonte_y))
        if y2 <= y1:
            continue

        ancho1 = int(10 + t1 * 2300)
        ancho2 = int(10 + t2 * 2300)

        curva1 = curva_actual * (t1 ** 2)
        curva2 = curva_actual * (t2 ** 2)

        x1 = ancho // 2 - ancho1 // 2 + int(jugador.desplazamiento_pista * t1) + int(curva1)
        x2 = ancho // 2 - ancho2 // 2 + int(jugador.desplazamiento_pista * t2) + int(curva2)

        textura_h = road_texture.get_height()
        textura_w = road_texture.get_width()
        slice_h = 3
        profundidad = min(1.0, t1 * 1.8)
        escala_textura = 160
        textura_pos = (jugador.offset_pista * profundidad) + (i / segmentos) * escala_textura
        slice_y = int(textura_pos) % (textura_h - slice_h)

        road_slice = road_texture.subsurface((0, slice_y, textura_w, slice_h))
        road_slice = pygame.transform.smoothscale(road_slice, (ancho2, y2 - y1))

        mascara = pygame.Surface((ancho, y2 - y1), pygame.SRCALPHA)
        puntos = [
            (x1, 0),
            (x1 + ancho1, 0),
            (x2 + ancho2, y2 - y1),
            (x2, y2 - y1)
        ]
        pygame.draw.polygon(mascara, (255, 255, 255, 255), puntos)

        temp = pygame.Surface((ancho, y2 - y1), pygame.SRCALPHA)
        temp.blit(road_slice, (x2, 0))
        temp.blit(mascara, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        superficie.blit(temp, (0, y1))


def obtener_imagen_auto(jugador):
    if jugador.imagen_actual == "izquierda":
        return auto_izquierda
    if jugador.imagen_actual == "derecha":
        return auto_derecha
    return auto_jugador


def dibujar_auto_jugador(superficie, jugador):
    auto_ancho = 100
    auto_alto = 60

    imagen = pygame.transform.scale(
        obtener_imagen_auto(jugador),
        (auto_ancho, auto_alto)
    )

    centro_pista = superficie.get_width() // 2
    separacion = 170

    auto_x = (
        centro_pista
        - auto_ancho // 2
        + int(jugador.carril * separacion)
    )

    auto_y = superficie.get_height() - auto_alto - 15

    superficie.blit(imagen, (auto_x, auto_y))


def dibujar_conteo(superficie):
    global conteo_terminado, fase_carrera
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
        fuente_conteo = pygame.font.SysFont("arial", 70, bold=True)
        texto = fuente_conteo.render(numero, True, (255, 255, 255))
        sombra = fuente_conteo.render(numero, True, (0, 0, 0))
        x = superficie.get_width() // 2 - texto.get_width() // 2
        y = superficie.get_height() // 2 - texto.get_height() // 2
        superficie.blit(sombra, (x + 4, y + 4))
        superficie.blit(texto, (x, y))


# =========================
# LÓGICA DE CARRERA
# =========================
def reiniciar_carrera():
    global distancia_meta, tiempo_inicio_conteo, conteo_terminado, fase_carrera
    distancia_meta = 0
    conteo_terminado = False
    fase_carrera = "conteo"
    tiempo_inicio_conteo = pygame.time.get_ticks()
    jugador1.reiniciar()
    jugador2.reiniciar()


def actualizar_jugador(jugador, teclas, dt):
    if teclas[jugador.derecha]:
        fuerza_giro = 4 + (jugador.velocidad * 0.05)

        # La pista/cámara se mueve en su pantalla
        jugador.desplazamiento_pista -= fuerza_giro

        # Posición real del jugador en la pista
        jugador.carril += 0.035 + jugador.velocidad * 0.00010

        jugador.imagen_actual = "derecha"

    elif teclas[jugador.izquierda]:
        fuerza_giro = 4 + (jugador.velocidad * 0.05)

        # La pista/cámara se mueve en su pantalla
        jugador.desplazamiento_pista += fuerza_giro

        # Posición real del jugador en la pista
        jugador.carril -= 0.035 + jugador.velocidad * 0.00010

        jugador.imagen_actual = "izquierda"

    else:
        jugador.imagen_actual = "centro"

    jugador.desplazamiento_pista = max(-500, min(500, jugador.desplazamiento_pista))
    jugador.carril = max(-1.0, min(1.0, jugador.carril))

    if teclas[jugador.acelerar]:
        jugador.velocidad += aceleracion * dt
        if jugador.velocidad > velocidad_max:
            jugador.velocidad = velocidad_max
    else:
        jugador.velocidad -= aceleracion * dt * 0.5

    if jugador.frenar is not None and teclas[jugador.frenar]:
        jugador.velocidad -= aceleracion * dt * 1.3

    if jugador.velocidad < 0:
        jugador.velocidad = 0

    jugador.distancia += jugador.velocidad * dt * FACTOR_DISTANCIA


def actualizar_posiciones():
    if jugador1.distancia >= jugador2.distancia:
        jugador1.posicion = 1
        jugador2.posicion = 2
    else:
        jugador1.posicion = 2
        jugador2.posicion = 1



def dibujar_auto_oponente(superficie, jugador_vista, oponente):
    diferencia = oponente.distancia - jugador_vista.distancia

    # =====================================================
    # REGLA CORRECTA:
    # - Si el rival está detrás, NO se ve.
    # - Si están casi al mismo nivel, SÍ se ve y del mismo tamaño.
    # - Si el rival está adelante, se ve más pequeño según distancia.
    # =====================================================

    tolerancia_mismo_nivel = 1.0

    # Rival detrás: no debe verse.
    if diferencia < -tolerancia_mismo_nivel:
        return

    distancia_visible_max = 55

    # Rival demasiado adelante: ya no se ve.
    if diferencia > distancia_visible_max:
        return

    ancho = superficie.get_width()
    alto = superficie.get_height()

    horizonte_y = 125

    # Misma posición vertical que el auto del jugador.
    auto_jugador_ancho = 100
    auto_jugador_alto = 60
    y_mismo_nivel = alto - auto_jugador_alto - 15

    # Si están casi iguales, lo tratamos como empate visual.
    if abs(diferencia) <= tolerancia_mismo_nivel:
        progreso = 0
    else:
        progreso = diferencia / distancia_visible_max

    progreso = max(0.0, min(1.0, progreso))

    # Cerca abajo, lejos arriba.
    auto_y = int(y_mismo_nivel - progreso * (y_mismo_nivel - horizonte_y))

    # Profundidad visual.
    t = (auto_y - horizonte_y) / (alto - horizonte_y)
    t = max(0.0, min(1.0, t))

    # Si están al mismo nivel, el rival tiene el MISMO tamaño.
    escala = 1.0 - progreso * 0.75
    escala = max(0.20, min(1.0, escala))

    auto_ancho = int(auto_jugador_ancho * escala)
    auto_alto = int(auto_jugador_alto * escala)

    if auto_ancho <= 10 or auto_alto <= 8:
        return

    imagen = pygame.transform.scale(
        obtener_imagen_auto(oponente),
        (auto_ancho, auto_alto)
    )

    curva_actual = obtener_curva_por_distancia(jugador_vista.distancia)

    # Centro visual de la pista según la cámara del jugador que mira.
    centro_pista_x = ancho // 2
    centro_pista_x += int(jugador_vista.desplazamiento_pista * t)
    centro_pista_x += int(curva_actual * (t ** 2))

    # El carril del rival depende SOLO del rival.
    carril_rival = oponente.carril

    # Separación lateral.
    if progreso == 0:
        # Cuando están juntos en la salida/meta, usa misma separación que el jugador.
        limite_lateral = 170
    else:
        # Cuando está adelante, aplica perspectiva.
        ancho_pista_visible = 80 + (t ** 1.45) * 620
        limite_lateral = ancho_pista_visible * 0.45

    auto_x = centro_pista_x - auto_ancho // 2
    auto_x += int(carril_rival * limite_lateral)

    auto_x = max(5, min(ancho - auto_ancho - 5, auto_x))

    superficie.blit(imagen, (auto_x, auto_y))


def dibujar_vista_jugador(jugador, oponente, y_destino):
    superficie = pygame.Surface((ANCHO, ALTO_PANTALLA))

    dibujar_pista_textura(superficie, jugador)

    dibujar_auto_oponente(superficie, jugador, oponente)
    dibujar_auto_jugador(superficie, jugador)

    if fase_carrera == "conteo":
        dibujar_conteo(superficie)

    if fase_carrera == "carrera":
        dibujar_hud_jugador(superficie, jugador)

    ventana.blit(superficie, (0, y_destino))


def dibujar_intro_carrera_split():
    global distancia_meta, fase_carrera, tiempo_inicio_conteo

    distancia_meta -= velocidad_intro
    if distancia_meta <= 0:
        distancia_meta = 0
        fase_carrera = "conteo"
        tiempo_inicio_conteo = pygame.time.get_ticks()
        jugador1.reiniciar()
        jugador2.reiniciar()

    for y_destino, nombre in [(0, "JUGADOR 1"), (ALTO_PANTALLA, "JUGADOR 2")]:
        superficie = pygame.Surface((ANCHO, ALTO_PANTALLA))
        dibujar_pista_textura(superficie, jugador1 if nombre == "JUGADOR 1" else jugador2)
        dibujar_auto_jugador(superficie, jugador1 if nombre == "JUGADOR 1" else jugador2)

        fuente = pygame.font.SysFont("arial", 24, bold=True)
        texto = fuente.render(f"{nombre} - {int(distancia_meta)} m", True, (255, 255, 255))
        sombra = fuente.render(f"{nombre} - {int(distancia_meta)} m", True, (0, 0, 0))
        superficie.blit(sombra, (17, 17))
        superficie.blit(texto, (15, 15))

        ventana.blit(superficie, (0, y_destino))




def dibujar_juego_final(dt):
    if fase_carrera == "intro":
        dibujar_intro_carrera_split()
        pygame.draw.rect(ventana, (0, 0, 0), (0, ALTO_PANTALLA - 3, ANCHO, 6))
        return

    if fase_carrera == "carrera":
        teclas = pygame.key.get_pressed()
        actualizar_jugador(jugador1, teclas, dt)
        actualizar_jugador(jugador2, teclas, dt)
        actualizar_posiciones()

    dibujar_vista_jugador(jugador1, jugador2, 0)
    dibujar_vista_jugador(jugador2, jugador1, ALTO_PANTALLA)
    pygame.draw.rect(ventana, (0, 0, 0), (0, ALTO_PANTALLA - 3, ANCHO, 6))


# =========================
# INTRO INICIAL
# =========================
try:
    pygame.mixer.music.load("images/sonido/intro.mp3")
    pygame.mixer.music.play(-1)
except Exception:
    pass

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
# LOOP PRINCIPAL
# =========================
while True:
    reloj.tick(FPS)
    dt = reloj.get_time() / 1000

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
                try:
                    pygame.mixer.music.load("images/sonido/lasvegas.mp3")
                    pygame.mixer.music.play(-1)
                except Exception:
                    pass
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
            reiniciar_carrera()
            estado = "juego_final"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        continue

    # =========================
    # JUEGO FINAL 2 JUGADORES
    # =========================
    if estado == "juego_final":
        dibujar_juego_final(dt)

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
        y_titulo += velocidad_menu
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
            y_gear -= velocidad_menu
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
