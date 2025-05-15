from remake1.constant.enums import Direction


class Obstacle:
    def __init__(self, image, x, y, speed, moving_frame, is_vertical):
        self.surface = image
        self.rect = self.surface.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.moving_frame = moving_frame
        self.last_frame = 0
        if is_vertical:
            self.direction = Direction.UP
        else:
            self.direction = Direction.RIGHT

    def move(self, frame):
        if frame - self.last_frame >= self.moving_frame:  # 超过运动时长反向
            self.last_frame = frame
            if self.direction == Direction.UP:
                self.direction = Direction.DOWN
            elif self.direction == Direction.DOWN:
                self.direction = Direction.UP
            elif self.direction == Direction.LEFT:
                self.direction = Direction.RIGHT
            elif self.direction == Direction.RIGHT:
                self.direction = Direction.DOWN
        if self.direction == Direction.UP:
            self.rect.y += self.speed
        elif self.direction == Direction.DOWN:
            self.rect.y -= self.speed
        elif self.direction == Direction.LEFT:
            self.rect.x += self.speed
        elif self.direction == Direction.RIGHT:
            self.rect.x += self.speed

    def render(self, screen):
        screen.blit(self.surface, self.rect)