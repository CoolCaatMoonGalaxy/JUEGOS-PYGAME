import pygame
from enemies import Enemie
import constantes
from personaje import Personaje
from PIL import Image
import extra_anim

# Inicializamos Pygame
pygame.init()

# Creamos la ventana
ventana = pygame.display.set_mode((constantes.ANCHO_ventana, constantes.ALTO_ventana))

# Título de la ventana
pygame.display.set_caption("Pygame Proyecto")

# Hacemos un sprite grupo para las colisiones del enemigo
grupo_enemigos = pygame.sprite.Group()

# Creamos la función que agrega a los enemigos al grupo
def crear_enemigos(cantidad_enemigos):
    enemigos_creados = []
    for i in range(cantidad_enemigos):
        enemigo = Enemie(100 + i * 50, 80 + i * 30, enem_sprites_idle, enem_sprites_walk, enem_sprites_attack,extra_anim.orc_death_anim, energia_enemie=100)
        grupo_enemigos.add(enemigo)  # Agregamos el enemigo al grupo de colisiones
        enemigos_creados.append(enemigo) 
    return len(enemigos_creados)  # Devolvemos el número de enemigos creados
    

# Creamos la función para escalar la imagen (solo escalar una vez)
def escalar_img(image, scale):
    if scale <= 0:
        raise ValueError("El factor de escala debe ser mayor que 0")
    w = image.get_width()
    h = image.get_height()
    nueva_imagen = pygame.transform.scale(image, (int(w * scale), int(h * scale)))
    return nueva_imagen

# Función para cargar frames de un GIF usando Pillow
def cargar_gif(ruta_gif, escala):
    imagen_gif = Image.open(ruta_gif)
    frames = []
    try:
        while True:
            frame = imagen_gif.copy()
            frame = frame.convert("RGBA")
            frame_pygame = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
            frame_pygame = escalar_img(frame_pygame, escala)  # Escalar una vez
            frames.append(frame_pygame)
            imagen_gif.seek(imagen_gif.tell() + 1)
    except EOFError:
        pass
    if not frames:
        print(f"Error: No se pudieron cargar frames desde {ruta_gif}.")
    return frames

# Cargamos las animaciones del personaje
animaciones_caminando = cargar_gif('assets/character/KNIGHT/run.gif', constantes.SCALE_CHAR)
animaciones_idle = cargar_gif('assets/character/KNIGHT/idle.gif', constantes.SCALE_CHAR)
animaciones_agachar = cargar_gif('assets/character/KNIGHT/crouch.gif', constantes.SCALE_CHAR)

# Cargamos los sprites del enemigo
enem_sprites_idle = [escalar_img(pygame.image.load(f'assets/enemies/ORC/idle/Orc-Idle_{i}.png'), constantes.SCALE_CHAR) for i in range(6)]
enem_sprites_walk = [escalar_img(pygame.image.load(f'assets/enemies/ORC/walk/images/Orc-walk_{i}.png'), constantes.SCALE_CHAR) for i in range(8)]
enem_sprites_attack = [escalar_img(pygame.image.load(f'assets/enemies/ORC/attack/Orc-Attack_{i}.png'), constantes.SCALE_CHAR) for i in range(6)]

# Definir variables de movimiento del jugador
mover_izquierda = False
mover_derecha = False
mover_arriba = False
mover_abajo = False
agacharse = False

# Creamos el personaje con las animaciones
jugador = Personaje(50, 50, animaciones_caminando, animaciones_idle, animaciones_agachar, extra_anim.animacion_ataque_estatico, energia=100, escala=1)

# En esta parte llamamos a la función para crear enemigos y agregamos la cantidad al grupo (en este caso, 3)
cantidad_enemigos = crear_enemigos(3)

# Variable de control para mantener la ventana abierta
run = True

# Creamos el objeto clock para controlar el frame rate
clock = pygame.time.Clock()

# Bucle principal
# Bucle principal
while run:
    delta_x = 0
    delta_y = 0

    # Manejo de eventos
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
            elif event.key == pygame.K_LSHIFT:
                agacharse = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                mover_izquierda = False
            elif event.key == pygame.K_d:
                mover_derecha = False
            elif event.key == pygame.K_w:
                mover_arriba = False
            elif event.key == pygame.K_s:
                mover_abajo = False
            elif event.key == pygame.K_LSHIFT:
                agacharse = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 1 es el botón izquierdo del ratón
                jugador.ataque()  # Llamada al método de ataque

    # Actualizar movimiento del jugador
    if mover_derecha:
        delta_x = constantes.velocidad_move
    elif mover_izquierda:
        delta_x = -constantes.velocidad_move

    if mover_arriba:
        delta_y = -constantes.velocidad_move
    elif mover_abajo:
        delta_y = constantes.velocidad_move

    jugador.movimiento(delta_x, delta_y, agacharse)

    # Actualizar los enemigos
    for enemigo in grupo_enemigos:
        enemigo.actualizar(jugador)

    # Verificar colisión y ataque
    for enemigo in grupo_enemigos:
        if pygame.sprite.collide_rect(jugador, enemigo) and jugador.ataque_activo:  # Usar un flag de ataque
            enemigo.energia_enemie -= 2  # Reducir la energía del enemigo al colisionar

            print("¡Colisión durante ataque! Energía del enemigo reducida.")
            print(f'{enemigo.energia_enemie}')

    # Renderizar
    ventana.fill(constantes.COLOR_BACKGROUND)
    jugador.dibujar(ventana)
    grupo_enemigos.draw(ventana)

    # Actualizar pantalla y control de frames
    pygame.display.update()
    clock.tick(constantes.FPS)

pygame.quit()
