import pygame
import constantes
from personaje import Personaje

jugador = Personaje(50, 50)


# Inicializamos Pygame
pygame.init()


# Creamos la ventana
ventana = pygame.display.set_mode((constantes.ANCHO_ventana,
                                    constantes.ALTO_ventana))


# Título de la ventana
pygame.display.set_caption("Pygame Proyecto")

# Variable de control para mantener la ventana abierta
run = True

# Bucle principal
while run:

    jugador.dibujar(ventana)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            # Verificamos si se presiona Alt + F4
            if event.key == pygame.K_F4 and pygame.key.get_mods() & pygame.KMOD_ALT:
                run = False

    pygame.display.update()
    
# Salimos correctamente de Pygame
pygame.quit()
