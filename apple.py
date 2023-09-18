import random
import arcade

class Apple(arcade.Sprite):
    def __init__(self,game_width, game_height):
        super().__init__("assets/apple.png")
        self.width=32
        self.height=32
        self.center_x=random.randint(self.width//2, game_width-self.width//2) // 8 * 8
        self.center_y=random.randint(self.height//2, game_height-self.height//2) // 8 * 8
        self.change_x=0
        self.change_y=0