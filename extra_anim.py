import pygame
from PIL import Image
import constantes

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

#cargar animacion de ataque
animacion_ataque_estatico = cargar_gif("assets/character/KNIGHT/extra/AttackNoMovement.gif")



