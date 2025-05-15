import json
import os
import sys

from datetime import datetime

import pygame.image

from remake1.component.ball import Ball
from remake1.component.paddle import Paddle
from remake1.constant.enums import Direction
from remake1.strategy.stragety import Strategy
from remake1.util.input_util import InputUtil

class Game:
    def __init__(self,config):
        self.config = config
        self.width,self.height = pygame.image.load(config.background_image).get_size()
        self.paddle_height,self.paddle_width = pygame.image.load(config.paddle_image).get_size()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.ball = Ball(config.ball_images,self.width//2,10,config.ball_speed,config.ball_speed)
        self.paddles = [
            Paddle(config.paddle_image,5,self.height//2,config.paddle_speed,self.height),
            Paddle(config.paddle_image,self.width-5,self.height//2,config.paddle_speed,self.height),
        ]
        self.game_history = []
        self.left_score = 0
        self.right_score = 0
    def save_state(self,direction1,direction2,frame):
        state = {
            'frame': frame,
            'ball': self.ball.get_state(),
            'paddle1': self.paddles[0].get_state(),
            'paddle2': self.paddles[1].get_state(),
            'actions': {
                'paddle1': direction1.name,
                'paddle2': direction2.name
            }
        }
        self.game_history.append(state)
    def update(self,direction1,direction2,frame):
        #更新物理位置
        self.ball.move() #更新球的位置
        self.paddles[0].move(direction1)
        self.paddles[1].move(direction2)
        #碰撞逻辑
        #挡板碰撞
        if self.ball.is_hit(self.paddles[0].rect):
            self.ball.rect.left = self.paddles[0].rect.right
            self.ball.speedx = -self.ball.speedx
        if self.ball.is_hit(self.paddles[1].rect):
            self.ball.rect.right = self.paddles[1].rect.left
            self.ball.speedx = -self.ball.speedx
        #上下边界碰撞
        if self.ball.rect.top < 0 or self.ball.rect.bottom > self.height:
            self.ball.speedy = -self.ball.speedy
        #左右边界计分
        if self.ball.rect.right < 0:
            self.ball.reset()
            self.right_score += 1
        if self.ball.rect.left > self.width:
            self.ball.reset()
            self.left_score += 1
        #渲染
        if self.config.render:
            self.ball.render(frame,self.screen)
            self.paddles[0].render(self.screen)
            self.paddles[1].render(self.screen)
    def winer(self):
        if self.right_score >= self.config.max_scores:
            return 1    #右边玩家win
        elif self.left_score >= self.config.max_scores:
            return -1   #左边玩家win
        else:
            return 0    #游戏继续
    def export_history(self):
        # 创建保存目录
        os.makedirs(self.config.save_dir, exist_ok=True)
        # 时间戳命名文件
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"game_{timestamp}.json"
        filepath = os.path.join(self.config.save_dir, filename)
        save_data = {
            "config": self.config.__dict__,
            "frames": self.game_history,
        }
        # 保存为json格式
        try:
            with open(filepath, 'w') as f:
                json.dump(save_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving game data: {e}")
            return False
    def start(self):
        pygame.init()
        clock = pygame.time.Clock()
        if self.config.mode == "PVE":
            input_listener = InputUtil([pygame.K_w, pygame.K_s])
        elif self.config.mode == "PVP":
            input_listener = InputUtil([pygame.K_w, pygame.K_s, pygame.K_UP, pygame.K_DOWN])
        else:
            input_listener = None
        frame = 0
        direction1 = Direction.IDLE
        direction2 = Direction.IDLE
        while True:
            if self.config.render:
                self.screen.blit(pygame.image.load(self.config.background_image),(0,0))
            for event in pygame.event.get():
                #按键监听
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    input_listener.press(event.key)
                if event.type == pygame.KEYUP:
                    input_listener.release(event.key)
            if self.config.mode == "PVP":
                #player1
                if input_listener.is_pressed(pygame.K_w):  # 多键输入优先向上
                    direction1 = Direction.UP
                elif input_listener.is_pressed(pygame.K_s):
                    direction1 = Direction.DOWN
                else:
                    direction1 = Direction.IDLE
                #player2
                if input_listener.is_pressed(pygame.K_UP):  # 多键输入优先向上
                    direction2 = Direction.UP
                elif input_listener.is_pressed(pygame.K_DOWN):
                    direction2 = Direction.DOWN
                else:
                    direction2 = Direction.IDLE
            elif self.config.mode == "PVE":
                # player1
                if input_listener.is_pressed(pygame.K_w):  # 多键输入优先向上
                    direction1 = Direction.UP
                elif input_listener.is_pressed(pygame.K_s):
                    direction1 = Direction.DOWN
                else:
                    direction1 = Direction.IDLE
                # ai
                if self.config.strategy_right == 1:
                    direction2 = Strategy.simple_ai(self.ball.get_state(), self.paddles[1].get_state())
                elif self.config.strategy_right == 2:
                    direction2 = Strategy.medium_ai(self.ball.get_state(), self.paddles[1].get_state(),self.paddle_height)
                elif self.config.strategy_right == 3:
                    direction2 = Strategy.advanced_ai(self.ball.get_state(), self.paddles[1].get_state(),self.width,self.paddle_height)
                elif self.config.strategy_right == 4:
                    direction2 = Strategy.expert_ai(self.ball.get_state(), self.paddles[1].get_state(),self.width,self.paddle_height)
                elif self.config.strategy_right == 5:
                    direction2 = Strategy.reactive_ai(self.ball.get_state(), self.paddles[1].get_state(),self.paddle_height)
            if self.config.save:
                self.save_state(direction1,direction2,frame)
            self.update(direction1,direction2,frame)
            if self.winer() != 0:
                if self.config.save:
                    self.export_history()
                break
            frame += 1
            pygame.display.update()
            clock.tick(self.config.fps)







