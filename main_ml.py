import tensorflow as tf
import numpy as np
import pandas as pd
import arcade
from apple import Apple
from snake import Snake

game_width=800
game_height=560

class Game(arcade.Window):
    def __init__(self):
        super().__init__(width=game_width, height=game_height, title="Super Snake V1")
        arcade.set_background_color(arcade.color.KHAKI)

        self.snake=Snake(game_width,game_height)
        self.food=Apple(game_width,game_height)
        self.model=tf.keras.models.load_model('weights\my_snake_model.h5')

    def on_draw(self):
        arcade.start_render()
        self.snake.draw()
        self.food.draw()
        arcade.draw_text(f"score: {self.snake.score}", 10, 10, arcade.color.BLACK)
        arcade.finish_render()

    def on_update(self, delta_time: float):
        self.snake.move()

        data = {"w0":None,
                "w1":None,
                "w2":None,
                "w3":None,
                "a0":None,
                "a1":None,
                "a2":None,
                "a3":None,
                "b0":None,
                "b1":None,
                "b2":None,
                "b3":None}

        data["w0"]=game_height-self.snake.center_y
        data['w1']=game_width-self.snake.center_x
        data["w2"]=self.snake.center_y
        data["w3"]=self.snake.center_x

        if self.snake.center_x == self.food.center_x and self.snake.center_y < self.food.center_y:
            data["a0"] = 1
            data["a1"] = 0
            data["a2"] = 0
            data["a3"] = 0
        elif self.snake.center_x == self.food.center_x and self.snake.center_y > self.food.center_y:
            data["a0"] = 0
            data["a1"] = 0
            data["a2"] = 1
            data["a3"] = 0
        elif self.snake.center_x < self.food.center_x and self.snake.center_y == self.food.center_y:
            data["a0"] = 0
            data["a1"] = 1
            data["a2"] = 0
            data["a3"] = 0
        elif self.snake.center_x > self.food.center_x and self.snake.center_y == self.food.center_y:
            data["a0"] = 0
            data["a1"] = 0
            data["a2"] = 0
            data["a3"] = 1

        for part in self.snake.body:
            if self.snake.center_x == part["x"] and self.snake.center_y < part["y"]:
                data["b0"] = 1
                data["b1"] = 0
                data["b2"] = 0
                data["b3"] = 0
            elif self.snake.center_x == part["x"] and self.snake.center_y > part["y"]:
                data["b0"] = 0
                data["b1"] = 0
                data["b2"] = 1
                data["b3"] = 0
            elif self.snake.center_x < part["x"] and self.snake.center_y == part["y"]:
                data["b0"] = 0
                data["b1"] = 1
                data["b2"] = 0
                data["b3"] = 0
            elif self.snake.center_x > part["x"] and self.snake.center_y == part["y"]:
                data["b0"] = 0
                data["b1"] = 0
                data["b2"] = 0
                data["b3"] = 1

        data = pd.DataFrame(data, index=[1])
        data.fillna(0, inplace=True)
        data=data.values
        print(data)

        output = self.model.predict(data)
        direction= output.argmax()

        if direction==0:
            self.snake.change_x = 0
            self.snake.change_y = 1
        elif direction==1:
            self.snake.change_x = 1
            self.snake.change_y = 0
        elif direction==2:
            self.snake.change_x = 0
            self.snake.change_y = -1
        elif direction==3:
            self.snake.change_x = -1
            self.snake.change_y = 0

        if arcade.check_for_collision(self.snake, self.food):
            self.snake.eat(self.food)
            self.food=Apple(game_width,game_height)

    def on_key_release(self, symbol: int, modifiers: int):
        pass

        
if __name__=="__main__":
    game=Game()
    arcade.run()