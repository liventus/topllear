import pygame
import sys

pygame.init()

ANCHO = 700
ALTO = 250
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("HUD Velocidad Top Gear")

reloj = pygame.time.Clock()

# 🔢 Números tipo display
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

def dibujar_numero(numero, x, y, tamaño=20):
    matriz = numeros[str(numero)]
    for fila in range(len(matriz)):
        for col in range(len(matriz[fila])):
            if matriz[fila][col] == 1:
                pygame.draw.rect(
                    ventana,
                    (255, 0, 0),
                    (x + col*tamaño, y + fila*tamaño, tamaño, tamaño)
                )

#  variables velocidad
velocidad = 0
velocidad_max = 200
aceleracion = velocidad_max / 5  # llega en 5 segundos

def dibujar_barra(velocidad):
    x_inicio = 50
    y_inicio = 50
    ancho = 18
    alto = 30
    separacion = 3

    total = 20
    activos = int((velocidad / velocidad_max) * total)

    for i in range(total):
        x = x_inicio + i * (ancho + separacion)

        # colores por zona
        if i < 7:
            color = (0, 255, 0)       # verde
        elif i < 14:
            color = (255, 255, 0)     # amarillo
        else:
            color = (255, 0, 0)       # rojo

        if i >= activos:
            color = (40, 40, 40)

        pygame.draw.rect(ventana, color, (x, y_inicio, ancho, alto))

# 🔁 loop
while True:
    dt = reloj.tick(60) / 1000  # segundos

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_SPACE]:
        velocidad += aceleracion * dt
    else:
        velocidad -= aceleracion * dt * 0.5  # freno suave

    velocidad = max(0, min(velocidad, velocidad_max))

    # 🎨 fondo
    ventana.fill((30, 30, 30))

    # panel
    pygame.draw.rect(ventana, (0, 0, 0), (40, 30, 600, 150))

    # barra
    dibujar_barra(velocidad)

    # número
    texto = str(int(velocidad)).zfill(3)

    x = 300
    for digito in texto:
        dibujar_numero(digito, x, 80)
        x += 70

    pygame.display.update()