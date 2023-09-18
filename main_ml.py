import tensorflow as tf
import pandas as pd
import arcade
from apple import Apple
from snake import Snake

game_width=800
game_height=560

class Game(arcade.Window):
    def __init__(self):
        super().__init__(width=game_width, height=game_height, title="Super Snake AI")
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

        data = {"wu":None,
                "wr":None,
                "wd":None,
                "wl":None,
                "x_a":None,
                "y_a":None,
                "x_s":None,
                "y_s":None,
                "au":None,
                "ar":None,
                "ad":None,
                "al":None}

        data["wu"]=game_height-self.snake.center_y
        data["wr"]=game_width-self.snake.center_x
        data["wd"]=self.snake.center_y
        data["wl"]=self.snake.center_x

        data["x_a"]=self.food.center_x
        data["y_a"]=self.food.center_y

        data["x_s"]=self.snake.center_x
        data["y_s"]=self.snake.center_y

        if self.snake.center_x == self.food.center_x and self.snake.center_y < self.food.center_y:
            data["au"] = 1
            data["ar"] = 0
            data["ad"] = 0
            data["al"] = 0
        elif self.snake.center_x == self.food.center_x and self.snake.center_y > self.food.center_y:
            data["au"] = 0
            data["ar"] = 0
            data["ad"] = 1
            data["al"] = 0
        elif self.snake.center_x < self.food.center_x and self.snake.center_y == self.food.center_y:
            data["au"] = 0
            data["ar"] = 1
            data["ad"] = 0
            data["al"] = 0
        elif self.snake.center_x > self.food.center_x and self.snake.center_y == self.food.center_y:
            data["au"] = 0
            data["ar"] = 0
            data["ad"] = 0
            data["al"] = 1

        elif self.snake.center_x > self.food.center_x and self.snake.center_y > self.food.center_y:
            data["au"] = 0
            data["ar"] = 0
            data["ad"] = 1
            data["al"] = 1

        elif self.snake.center_x > self.food.center_x and self.snake.center_y < self.food.center_y:
            data["au"] = 1
            data["ar"] = 0
            data["ad"] = 0
            data["al"] = 1

        elif self.snake.center_x < self.food.center_x and self.snake.center_y > self.food.center_y:
            data["au"] = 0
            data["ar"] = 1
            data["ad"] = 1
            data["al"] = 0

        elif self.snake.center_x < self.food.center_x and self.snake.center_y < self.food.center_y:
            data["au"] = 1
            data["ar"] = 1
            data["ad"] = 0
            data["al"] = 0

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