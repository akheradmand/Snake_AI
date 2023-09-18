import arcade

class Snake(arcade.Sprite):
    def __init__(self,game_width, game_height):
        super().__init__()
        self.game_width=game_width
        self.game_height=game_height
        self.width=32
        self.height=32
        self.center_x=game_width//2
        self.center_y=game_height//2
        self.color=arcade.color.GREEN
        self.change_x=0
        self.change_y=0
        self.speed=8
        self.score=0
        self.body=[]

    def draw(self):
        arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width, self.height, arcade.color.DARK_GREEN)
        for i in range(len(self.body)):
            if i%2==0:
                arcade.draw_rectangle_filled(self.body[i]['x'], self.body[i]['y'], self.width, self.height, self.color)
            else:
                arcade.draw_rectangle_filled(self.body[i]['x'], self.body[i]['y'], self.width, self.height, arcade.color.DARK_GREEN)

    def move(self):
        self.body.append({'x':self.center_x, 'y':self.center_y})

        if len(self.body) > self.score:
            self.body.pop(0)

        if self.center_x<0:
            self.center_x=self.game_width
        elif self.center_x>self.game_width:
            self.center_x=0
        elif self.center_y<0:
            self.center_y=self.game_height
        elif self.center_y>self.game_height:
            self.center_y=0
        
        self.center_x += self.change_x*self.speed
        self.center_y += self.change_y*self.speed

    def eat(self,food):
        del food
        self.score += 1