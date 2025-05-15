import pygame.image


class Ball:
    def __init__(self, images, x, y, speedx, speedy):
        self.origin_x = x
        self.origin_y = y
        self.origin_speedx = speedx
        self.origin_speedy = speedy
        self.surfaces = []
        for img_path in images:
            try:
                surface = pygame.image.load(img_path)
                self.surfaces.append(surface)
            except pygame.error as e:
                print(f"无法加载图片 {img_path}: {e}")
        self.rect = self.surfaces[0].get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speedx = speedx
        self.speedy = speedy

    def move(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

    def render(self, frame, screen):
        screen.blit(self.surfaces[(frame % len(self.surfaces))], self.rect)

    def is_hit(self, other_rect):
        return self.rect.colliderect(other_rect)

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def set_speed(self, speedx, speedy):
        self.speedx = speedx
        self.speedy = speedy

    def reset(self):
        self.set_position(self.origin_x, self.origin_y)
        self.set_speed(self.origin_speedx, self.origin_speedy)

    def get_state(self):
        return {
            'x': self.rect.x,
            'y': self.rect.y,
            'speedx': self.speedx,
            'speedy': self.speedy
        }

    def load_state(self, state):
        self.rect.x = state["x"]
        self.rect.y = state["y"]
        self.speedx = state["speedx"]
        self.speedy = state["speedy"]
