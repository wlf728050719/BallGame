import pygame

from remake1.constant.enums import Direction


class Paddle:
    def __init__(self, image, x, y, speed,height):
        self.surface = pygame.image.load(image)
        self.rect = self.surface.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.height = height
    def move(self, direction):
        if direction == Direction.UP:
            self.rect.y -= self.speed
        elif direction == Direction.DOWN:
            self.rect.y += self.speed
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.height:
            self.rect.bottom = self.height
    def render(self, screen):
        screen.blit(self.surface, self.rect)

    def set_position(self, y):
        self.rect.y = y

    def set_speed(self, speed):
        self.speed = speed

    def get_state(self):
        return {
            'x': self.rect.x,
            'y': self.rect.y,
            'speed': self.speed
        }

    def load_state(self, state):
        self.rect.x = state["x"]
        self.rect.y = state["y"]
        self.speed = state["speed"]
