import pygame
import constantes

class Personaje:
    def __init__(self, x, y):
        # Cargar la textura
        self.textura = pygame.image.load('assets/square.png').convert_alpha()

        # Ajustar el tamaño de la textura al tamaño del personaje cuadrado
        self.textura = pygame.transform.scale(self.textura, (constantes.ANCHO_PERSONAJE, constantes.ALTO_PERSONAJE))

        # Crear el rectángulo para la textura
        self.rect = self.textura.get_rect()
        self.rect.center = (x, y)

    def movimiento(self, delta_x, delta_y):
        # Actualiza la posición del jugador
        self.rect.x += delta_x
        self.rect.y += delta_y

    def dibujar(self, interfaz):
        # Dibujar la textura en la interfaz
        interfaz.blit(self.textura, self.rect)
