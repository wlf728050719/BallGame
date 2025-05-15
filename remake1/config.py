import json


class Config:
    def __init__(self):
        self.background_image = None
        self.ball_images = []
        self.paddle_image = None
        self.fps = 0
        self.mode = None
        self.strategy_left = 0
        self.strategy_right = 0
        self.max_scores = 0
        self.ball_speed = 0
        self.paddle_speed = 0
        self.render = True
        self.save = True
        self.save_dir = None
    @classmethod
    def from_json_file(cls, file):
        config = Config()
        with open(file, "r") as f:
            config.__dict__ = json.load(f)
        return config

    def __str__(self):
        return str(self.__dict__)
