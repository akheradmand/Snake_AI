import arcade
import pandas as pd
# from sys import exit
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
        self.dataset=[]

    def on_draw(self):
        arcade.start_render()
        self.snake.draw()
        self.food.draw()
        arcade.draw_text(f"score: {self.snake.score}", 10, 10, arcade.color.BLACK)
        arcade.finish_render()

    def on_update(self, delta_time: float):

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
                "b3":None,
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