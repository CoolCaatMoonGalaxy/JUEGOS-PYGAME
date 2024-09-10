import pygame
import constantes
from personaje import Personaje, Enemigo
from PIL import Image
import extra_anim

# Inicializamos Pygame
pygame.init()

# Creamos la ventana
ventana = pygame.display.set_mode((constantes.ANCHO_ventana, constantes.ALTO_ventana))

# Título de la ventana
pygame.display.set_caption("Pygame Proyecto")

# Función para cargar frames de un GIF usando Pillow
def cargar_gif(ruta_gif):
    imagen_gif = Image.open(ruta_gif)
    frames = []
    try:
        while True:
            frame = imagen_gif.copy()
            frame = frame.convert("RGBA")
            frame_pygame = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
            frame_pygame = pygame.transform.scale(frame_pygame, (constantes.ANCHO_PERSONAJE, constantes.ALTO_PERSONAJE))
            frames.append(frame_pygame)
            imagen_gif.seek(imagen_gif.tell() + 1)
    except EOFError:
        pass
    if not frames:
        print(f"Error: No se pudieron cargar frames desde {ruta_gif}.")
    return frames

# Cargamos las animaciones del personaje
animaciones_caminando = cargar_gif('assets/character/KNIGHT/run.gif')
animaciones_idle = cargar_gif('assets/character/KNIGHT/idle.gif')
animaciones_agachar = cargar_gif('assets/character/KNIGHT/crouch.gif')
animaciones_salto = cargar_gif('assets/character/KNIGHT/Jump.gif')
animaciones_caer = cargar_gif('assets/character/KNIGHT/JumpFallInbetween.gif')

# Cargamos las animaciones del enemigo
animaciones_enemigo_walk = cargar_gif('assets/character/enemies/Demon/walk.gif')
animaciones_enemigo_idle = cargar_gif('assets/character/enemies/Demon/idle.gif')
animaciones_enemigo_attack = cargar_gif('assets/character/enemies/Demon/attack.gif')

# Definir variables de movimiento del jugador
mover_izquierda = False
mover_derecha = False
agacharse = False
saltar = False

# Creamos el personaje con las animaciones
jugador = Personaje(50, 50, animaciones_caminando, animaciones_idle, animaciones_agachar,
                    animaciones_salto, animaciones_caer, extra_anim.animacion_ataque_estatico)

# Creamos el enemigo con las animaciones
demon = Enemigo(100, 0, animaciones_enemigo_walk, animaciones_enemigo_idle, [],  # Si no hay animación de agacharse para el enemigo
                [],  # Si no hay animación de salto para el enemigo
                [],  # Si no hay animación de caer para el enemigo
                animaciones_enemigo_attack, animaciones_enemigo_walk)  # Usa las animaciones específicas para enemigos

# Variable de control para mantener la ventana abierta
run = True

# Creamos el objeto clock para controlar el frame rate
clock = pygame.time.Clock()

# Bucle principal
while run:
    delta_x = 0

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
            elif event.key == pygame.K_LSHIFT:
                agacharse = True
            elif event.key == pygame.K_SPACE:  # Espacio para saltar
                saltar = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                mover_izquierda = False
            elif event.key == pygame.K_d:
                mover_derecha = False
            elif event.key == pygame.K_LSHIFT:
                agacharse = False
            elif event.key == pygame.K_SPACE:
                saltar = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 1 es el botón izquierdo del ratón
                jugador.ataque()  # Llamada al método de ataque

    # Verifica los movimientos horizontales
    if mover_derecha:
        delta_x = constantes.velocidad_move
    elif mover_izquierda:
        delta_x = -constantes.velocidad_move

    # Actualiza la posición del personaje
    jugador.movimiento(delta_x, agacharse, saltar)
    demon.movimiento(0, False, False)  # Ajusta el movimiento del enemigo según tu lógica

    # Limpiamos la pantalla
    ventana.fill(constantes.COLOR_BACKGROUND)

    # Dibujamos al personaje y al enemigo
    jugador.dibujar(ventana)
    demon.dibujar(ventana)

    # Actualizamos la pantalla
    pygame.display.update()

    # Controlamos el frame rate (FPS)
    clock.tick(constantes.FPS)

# Salimos correctamente de Pygame
pygame.quit()
