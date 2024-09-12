import pygame
import constantes 

class Personaje(pygame.sprite.Sprite):
    def __init__(self, x, y, animaciones_caminando, animaciones_idle, animaciones_agachar, animacion_ataque_estatico, energia, escala=0):
        super().__init__()
        self.energia = energia
        self.animaciones_caminando = animaciones_caminando
        self.animaciones_idle = animaciones_idle
        self.animaciones_agachar = animaciones_agachar
        self.animacion_ataque_estatico = animacion_ataque_estatico
        self.ataque_activo = False
        self.frame_ataque_actual = 0
        self.tiempo_ataque = pygame.time.get_ticks()
        self.frame_actual = 0
        self.flip = False
        self.agachado = False
        self.velocidad_y = 0
        self.tiempo_cambio_animacion = pygame.time.get_ticks()

        self.escala = escala  # Factor de escala

        # Escalar las animaciones
        self.animaciones_caminando = [pygame.transform.scale(img, (int(img.get_width() * escala), int(img.get_height() * escala))) for img in animaciones_caminando]
        self.animaciones_idle = [pygame.transform.scale(img, (int(img.get_width() * escala), int(img.get_height() * escala))) for img in animaciones_idle]
        self.animaciones_agachar = [pygame.transform.scale(img, (int(img.get_width() * escala), int(img.get_height() * escala))) for img in animaciones_agachar]
        self.animacion_ataque_estatico = [pygame.transform.scale(img, (int(img.get_width() * escala), int(img.get_height() * escala))) for img in animacion_ataque_estatico]

        self.textura = self.animaciones_idle[self.frame_actual]
        self.rect = self.textura.get_rect(topleft=(x, y))

        # Definir el rectángulo de colisión más pequeño
        self.rect_colision = pygame.Rect(
            self.rect.x + 5,  # Ajusta la posición x más cerca del centro
            self.rect.y + 5,  # Ajusta y más cerca del centro
            self.rect.width - 10,  # Reduce el ancho
            self.rect.height - 10  # Reduce el alto
        )

    def actualizar_rect_colision(self):
        # Actualiza la posición del rectángulo de colisión en cada frame para que siga al personaje
        self.rect_colision.topleft = self.rect.topleft

    def ataque(self):
        if not self.ataque_activo:
            self.ataque_activo = True
            self.frame_ataque_actual = 0
            self.tiempo_ataque = pygame.time.get_ticks()

    def movimiento(self, delta_x, delta_y, agacharse):
        if self.ataque_activo:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.tiempo_ataque > 32:
                self.frame_ataque_actual = (self.frame_ataque_actual + 1) % len(self.animacion_ataque_estatico)
                self.textura = self.animacion_ataque_estatico[self.frame_ataque_actual]
                self.tiempo_ataque = tiempo_actual

                if self.frame_ataque_actual == len(self.animacion_ataque_estatico) - 1:
                    self.ataque_activo = False
                    self.textura = self.animaciones_idle[self.frame_actual]

        # Actualización de la posición
        self.rect.x += delta_x
        self.rect.y += delta_y

        # Asegúrate de actualizar el rectángulo de colisión
        self.actualizar_rect_colision()

        if delta_x < 0:
            self.flip = True
        elif delta_x > 0:
            self.flip = False

        tiempo_actual = pygame.time.get_ticks()

        # Animación al agacharse
        if agacharse:
            if tiempo_actual - self.tiempo_cambio_animacion > 100:
                self.frame_actual = (self.frame_actual + 1) % len(self.animaciones_agachar)
                self.textura = self.animaciones_agachar[self.frame_actual]
                self.tiempo_cambio_animacion = tiempo_actual
        # Animación al caminar (horizontal o vertical)
        elif delta_x != 0 or delta_y != 0:
            if tiempo_actual - self.tiempo_cambio_animacion > 30:
                self.frame_actual = (self.frame_actual + 1) % len(self.animaciones_caminando)
                self.textura = self.animaciones_caminando[self.frame_actual]
                self.tiempo_cambio_animacion = tiempo_actual
        # Animación idle
        else:
            if tiempo_actual - self.tiempo_cambio_animacion > 100:
                self.frame_actual = (self.frame_actual + 1) % len(self.animaciones_idle)
                self.textura = self.animaciones_idle[self.frame_actual]
                self.tiempo_cambio_animacion = tiempo_actual

    def dibujar(self, interfaz):
        if self.flip:
            image_flip = pygame.transform.flip(self.textura, flip_x=True, flip_y=False)
            interfaz.blit(image_flip, self.rect)
        else:
            interfaz.blit(self.textura, self.rect)

        # El rectángulo de colisión no se dibuja, por lo que es invisible
        # pygame.draw.rect(interfaz, pygame.Color('red'), self.rect_colision, 1)  # Esta línea está comentada para que el rectángulo sea invisible

    def colision_con_enemigos(self, enemigos, distancia_max):
        for enemigo in enemigos:
            if self.rect_colision.colliderect(enemigo.rect_colision):
                distancia_x = abs(self.rect_colision.centerx - enemigo.rect_colision.centerx)
                distancia_y = abs(self.rect_colision.centery - enemigo.rect_colision.centery)
                if distancia_x < distancia_max and distancia_y < distancia_max:
                    return True
        return False
