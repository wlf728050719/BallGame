import json

import pygame

from remake1.component.ball import Ball
from remake1.component.paddle import Paddle
from remake1.config import Config


class Replay:
    def __init__(self, filepath):
        with open(filepath, 'r') as f:
            self.data = json.load(f)

        # 从保存的数据还原Config
        self.config = Config()
        self.config.__dict__ = self.data["config"]

        # 初始化游戏窗口
        self.width, self.height = pygame.image.load(self.config.background_image).get_size()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.fps = self.config.fps

        # 初始化游戏对象
        self.ball = Ball(self.config.ball_images, 0, 0, 0, 0)
        self.paddles = [
            Paddle(self.config.paddle_image, 0, 0, 0, self.height),
            Paddle(self.config.paddle_image, 0, 0, 0, self.height)
        ]

    def load_frame(self, frame_data):
        self.ball.load_state(frame_data["ball"])
        self.paddles[0].load_state(frame_data["paddle1"])
        self.paddles[1].load_state(frame_data["paddle2"])

    def play(self):
        clock = pygame.time.Clock()
        for frame in self.data["frames"]:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            # 渲染背景
            self.screen.blit(pygame.image.load(self.config.background_image), (0, 0))
            self.load_frame(frame)

            # 渲染对象
            self.ball.render(frame["frame"], self.screen)
            self.paddles[0].render(self.screen)
            self.paddles[1].render(self.screen)

            pygame.display.flip()
            clock.tick(self.fps)