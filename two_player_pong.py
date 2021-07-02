import picodisplay as display
from time import sleep
import random
from pens import green, deep_blue

height = display.get_height()
width = display.get_width()

background_colour = deep_blue
player_colour = green

def draw_background():
    display.set_pen(deep_blue)
    display.clear()
    
class Ball:
    def __init__(self):
        self.radius = 7
        self.position_x = 120
        self.position_y = 67
        self.x_direction = 2
        self.y_direction = 2
        self._y_up_limit = 4
        self._x_up_limit = 6
        self._y_low_limit = 2
        self._x_low_limit = 2
        self._ky = 1
        self._kx = 1
    
    def draw(self):
        x = self.position_x
        y = self.position_y
        if x < 0 or x > width or y < 0 or y > height:
            raise Exception('ball out of range')
        display.set_pen(player_colour)
        display.circle(x,y,self.radius)
    
    def set_limited_direction(self):
        self.y_direction = self._ky*self._y_up_limit if self.y_direction > self._y_up_limit else self.y_direction
        self.x_direction = self._kx*self._x_up_limit if self.x_direction > self._x_up_limit else self.x_direction
        
    def has_hit_right_wall(self):
        return self.position_y < self.radius
    
    def has_hit_left_wall(self):
        return self.position_y > (height - self.radius - 5)
    
    def has_hit_player_one(self, player):
        return self.position_x > 195 and (self.position_y + self.radius > player.position) and (self.position_y - self.radius) < (player.position + player.length)
        
    def has_hit_player_two(self, player):
        return self.position_x < 35 and (self.position_y + self.radius > player.position) and (self.position_y - self.radius) < (player.position + player.length)
    
    def randomise_direction(self):
        rebound_chance = random.randint(0,6)
        if self.has_hit_right_wall() or self.has_hit_left_wall():
            self._kx = self._kx*-1 if rebound_chance == 2 else self._kx
            self._ky = -1 if self.has_hit_left_wall() else 1
            print('hit wall ky:{}'.format(self._ky))
        else:
            self._ky = self._ky*-1 if rebound_chance == 2 else self._ky
            self._kx = self._kx*-1 # hopefully these work
             
        self.x_direction = self._kx*random.randint(self._x_low_limit,self._x_up_limit)
        self.y_direction = self._ky*random.randint(self._y_low_limit,self._y_up_limit)
            
    def nudge_out_of_clip(self):
        left_clip = self.has_hit_left_wall() and self.y_direction < (height - self.position_y)
        right_clip = self.has_hit_right_wall() and self.y_direction < self.radius
        if left_clip or right_clip:
            self.y_direction = self._ky*self.radius
            print('nudge {}'.format(self.y_direction))
        
    def move(self):
        self.position_x += self.x_direction
        self.position_y += self.y_direction
        
    def reset_position(self):
        self.position_x = 120
        self.position_y = 67
        self.x_direction = 2
        self.y_direction = 2

class Player:
    def __init__(self,player_number):
        self.position = 40
        self._vertical_position = 210 if player_number == 1 else 23
        self._height = 7
        self.speed = 5
        self.length = 30
        self.score = 0
        
    def draw(self):
        display.set_pen(player_colour)
        display.rectangle(self._vertical_position,self.position,self._height,self.length)
        
    def move_true_left(self):
        if self.position < 105:
            self.position += self.speed
    
    def move_true_right(self):
        if self.position > 0:
            self.position -= self.speed

def end_game(one_score,two_score):
    show_score(one_score,two_score)
    display.set_led(255,0,0)
    sleep(5)
    display.set_led(0,0,255)
    
def show_score(one_score,two_score):
    display.set_pen(background_colour)
    display.clear()
    display.set_pen(green)
    display.text('{} - {}'.format(two_score,one_score),40,40,200,4)
    display.update()

def play():
    player_one = Player(1)
    player_two = Player(2)
    ball = Ball()
    playing_game = True
    while playing_game:
        draw_background()
        player_one.draw()
        player_two.draw()
        ball.draw()
        display.update()
        
        wall_collision = ball.has_hit_right_wall() or ball.has_hit_left_wall()
        player_one_hit_ball = ball.has_hit_player_one(player_one)
        player_two_hit_ball = ball.has_hit_player_two(player_two)
        
        ball.set_limited_direction()
        
        player_two_goal = ball.position_x > 215 and not player_one_hit_ball
        player_one_goal = ball.position_x < 15 and not player_two_hit_ball
        lose_condition = player_one.score + player_two.score >= 9
        
        if player_one_goal or player_two_goal:
            show_score(player_one.score,player_two.score)
            sleep(0.5)
            if player_one_goal:
                player_one.score += 1
            else:
                player_two.score += 1
            show_score(player_one.score,player_two.score)
            sleep(1)
            ball.reset_position()
            continue
        
        if lose_condition:
            end_game(player_one.score,player_two.score)
            playing_game = False
        
        if wall_collision or player_one_hit_ball or player_two_hit_ball:
            if player_one_hit_ball or player_two_hit_ball:
                display.set_led(150,0,100)
                sleep(0.05)
                display.set_led(0,0,255)

            ball.randomise_direction()
            ball.nudge_out_of_clip()
    
        if display.is_pressed(display.BUTTON_Y):
            player_one.move_true_left()
        if display.is_pressed(display.BUTTON_X):
            player_one.move_true_right()
        if display.is_pressed(display.BUTTON_B):
            player_two.move_true_left()
        if display.is_pressed(display.BUTTON_A):
            player_two.move_true_right()
        
        ball.move()
