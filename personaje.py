import pygame

class Personaje:
    def __init__(self, x, y):
        self.shape = pygame.Rect(0, 0, 20, 20)
        self.shape.center = (x, y)

    def dibujar(self, interfaz):
        pygame.draw.rect(interfaz, (255, 255, 0), self.shape)
