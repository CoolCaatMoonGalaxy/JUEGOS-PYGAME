import pygame
from PIL import Image
import constantes

# Función para escalar una imagen
def escalar_img(image, scale):
    if scale <= 0:
        raise ValueError("El factor de escala debe ser mayor que 0")
    w = image.get_width()
    h = image.get_height()
    nueva_imagen = pygame.transform.scale(image, (int(w * scale), int(h * scale)))
    return nueva_imagen

# Función para cargar un GIF y escalarlo
def cargar_gif(ruta_gif):
    try:
        imagen_gif = Image.open(ruta_gif)
        frames = []
        while True:
            frame = imagen_gif.copy()
            frame = frame.convert("RGBA")
            frame_pygame = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
            frame_pygame = escalar_img(frame_pygame, constantes.SCALE_CHAR)  # Escalar frame aquí
            frames.append(frame_pygame)
            imagen_gif.seek(imagen_gif.tell() + 1)
    except EOFError:
        pass
    except Exception as e:
        print(f"Error al cargar GIF {ruta_gif}: {e}")
    if not frames:
        print(f"Error: No se pudieron cargar frames desde {ruta_gif}.")
    return frames

# Cargar animación de ataque estático
animacion_ataque_estatico = cargar_gif("assets/character/KNIGHT/extra/AttackNoMovement.gif")

# Cargar animación de muerte
death_player_anim = []
for i in range(10):
    imgdeath = pygame.image.load(f'assets/character/KNIGHT/extra/death/Death_{i}.png')
    imgdeath = escalar_img(imgdeath, constantes.SCALE_CHAR)
    death_player_anim.append(imgdeath)

# Cargar sprite de golpe
hit_sprite = pygame.image.load('assets/character/KNIGHT/extra/hit/Hit.png')
hit_sprite = escalar_img(hit_sprite, constantes.SCALE_CHAR)

#cargar la animacion de orc death
orc_death_anim = []
for i in range(4):
    orcdeath = pygame.image.load(f'assets/enemies/ORC/death/images/Orc-Death_{i}.png')
    orcdeath = escalar_img(orcdeath, constantes.SCALE_CHAR)
    orc_death_anim.append(orcdeath)