from remake1.config import Config
from remake1.game import Game

if __name__ == "__main__":
    config = Config().from_json_file("pve.json")
    game = Game(config)
    game.start()



