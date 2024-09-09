import pygame
import constantes
from personaje import Personaje

# Inicializamos Pygame
pygame.init()

# Creamos la ventana
ventana = pygame.display.set_mode((constantes.ANCHO_ventana, constantes.ALTO_ventana))

# Título de la ventana
pygame.display.set_caption("Pygame Proyecto")

# Definir variables de Player (movimiento)
mover_arriba = False
mover_abajo = False
mover_izquierda = False
mover_derecha = False

# Creamos el personaje
jugador = Personaje(20, 20)

# Variable de control para mantener la ventana abierta
run = True

# Creamos el objeto clock para controlar el frame rate
clock = pygame.time.Clock()

# Bucle principal
while run:

    delta_x = 0
    delta_y = 0

    # Manejamos los eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F4 and pygame.key.get_mods() & pygame.KMOD_ALT:
                run = False
            elif event.key == pygame.K_a:
                mover_izquierda = True
            elif event.key == pygame.K_d:
                mover_derecha = True
            elif event.key == pygame.K_w:
                mover_arriba = True
            elif event.key == pygame.K_s:
                mover_abajo = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                mover_izquierda = False
            elif event.key == pygame.K_d:
                mover_derecha = False
            elif event.key == pygame.K_w:
                mover_arriba = False
            elif event.key == pygame.K_s:
                mover_abajo = False

    # Verifica los movimientos horizontales
    if mover_derecha:
        delta_x = 5
    elif mover_izquierda:
        delta_x = -5

    # Verifica los movimientos verticales
    if mover_arriba:
        delta_y = -5
    elif mover_abajo:
        delta_y = 5

    # Actualiza la posición del personaje
    jugador.movimiento(delta_x, delta_y)

    # Limpiamos la pantalla
    ventana.fill(constantes.COLOR_BACKGROUND)  # Usa el color de fondo definido en constantes

    # Dibujamos al personaje
    jugador.dibujar(ventana)

    # Actualizamos la pantalla
    pygame.display.update()

    # Controlamos el frame rate (FPS)
    clock.tick(constantes.FPS)  # Limita el juego a 60 FPS

# Salimos correctamente de Pygame
pygame.quit()
