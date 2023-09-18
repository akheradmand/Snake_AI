import arcade
import pandas as pd
from apple import Apple
from snake import Snake

game_width=800
game_height=560

class Game(arcade.Window):
    def __init__(self):
        super().__init__(width=game_width, height=game_height, title="Super Snake")
        arcade.set_background_color(arcade.color.KHAKI)

        self.snake=Snake(game_width,game_height)
        self.food=Apple(game_width,game_height)
        self.dataset=[]

    def on_draw(self):
        arcade.start_render()
        self.snake.draw()
        self.food.draw()
        arcade.draw_text(f"score: {self.snake.score}", 10, 10, arcade.color.BLACK)
        arcade.finish_render()

    def on_update(self, delta_time: float):

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
                "al":None,
                "direction":None}

        self.snake.move()

        dx=self.snake.center_x-self.food.center_x
        dy=self.snake.center_y-self.food.center_y

        if (abs(dx) < abs(dy) or dy==0) and dx > 0:
            self.snake.change_x = -1
            self.snake.change_y = 0
            data["direction"]=3 # left

        elif (abs(dx) < abs(dy) or dy==0) and dx < 0:
            self.snake.change_x = 1
            self.snake.change_y = 0
            data["direction"]=1 # right

        elif (abs(dx) > abs(dy) or dx==0) and dy > 0:
            self.snake.change_x = 0
            self.snake.change_y = -1
            data["direction"]=2 # down

        elif (abs(dx) > abs(dy) or dx==0) and dy < 0:
            self.snake.change_x = 0
            self.snake.change_y = 1
            data["direction"]=0 # up

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

        self.dataset.append(data)

        if arcade.check_for_collision(self.snake, self.food):
            self.snake.eat(self.food)
            self.food=Apple(game_width,game_height)

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol==arcade.key.Q:
            df = pd.DataFrame(self.dataset)
            df.to_csv('dataset\dataset.csv', index=False)
            arcade.close_window()
            exit(0)

        
if __name__=="__main__":
    game=Game()
    arcade.run()