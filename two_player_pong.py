import picodisplay as display
from time import sleep
import random
from pens import green, deep_blue

height = display.get_height()
width = display.get_width()

background_colour = deep_blue
player_colour = green
ball_radius = 7

def draw_background():
    display.set_pen(deep_blue)
    display.clear()

def draw_ball(position):
    (x,y)=position
    if x < 0 or x > width or y < 0 or y > height:
        raise Exception('ball out of range')
    display.set_pen(player_colour)
    display.circle(x,y,ball_radius)

class Player:
    def __init__(self,player_number):
        self.position = 40
        self._vertical_position = 210 if player_number == 1 else 23
        self.speed = 5
        self.length = 30
        self.score = 0
        
    def draw_player(self,position):
        display.set_pen(player_colour)
        display.rectangle(self._vertical_position,position,7,self.length)
        
    def move_true_left(self):
        if self.position < 105:
            self.position += self.speed
    
    def move_true_right(self):
        if self.position > 0:
            self.position -= self.speed
    
def end_game(one_score,two_score):
    display.set_pen(green)
    display.text('  {} - {}'.format(two_score,one_score),40,40,100,4)
    display.update()
    display.set_led(255,0,0)
    sleep(5)
    display.set_led(0,0,255)

def play():
    player_one = Player(1)
    player_two = Player(2)
    ball_position_x = ball_position_y = 50
    ball_x_direction = ball_y_direction = 2
    kx = ky = 1
    x_upper_limit = 6
    y_upper_limit = 4
    playing_game = True
    while playing_game:
        draw_background()
        player_one.draw_player(player_one.position)
        player_two.draw_player(player_two.position)
        draw_ball((ball_position_x, ball_position_y))
        display.update()
        
        ball_falling = ball_x_direction > 0
        ball_moving_left = ball_y_direction > 0
        wall_collision = ball_position_y > 125 or ball_position_y < 7
        top_collision = ball_position_x < 15
        
        player_one_collision = ball_position_x > 195 and (ball_position_y + ball_radius > player_one.position) and (ball_position_y - ball_radius) < (player_one.position + player_one.length)
        
        ball_y_direction = ky*y_upper_limit if ball_y_direction > y_upper_limit else ball_y_direction
        ball_x_direction = kx*x_upper_limit if ball_x_direction > x_upper_limit else ball_x_direction
        
        lose_condition = ball_position_x > 215 and not player_one_collision
        if lose_condition:
            end_game(player_one.score,player_two.score)
            playing_game = False
        
        if wall_collision or top_collision or player_one_collision:
            x_low_limit = 2
            y_low_limit = 2
            rebound_chance = random.randint(0,6)
            kx = kx*-1 if wall_collision and rebound_chance == 2 else kx
            ky = ky*-1 if (top_collision or player_one_collision) and rebound_chance == 2 else ky
            if top_collision:
                x_low_limit = 15 - ball_position_x
                kx = 1
            if player_one_collision:
                player_one.score += 1
                x_low_limit = ball_position_x - 195
                kx = -1
                display.set_led(150,0,100)
                sleep(0.05)
                display.set_led(0,0,255)
            if wall_collision:
                if ball_position_y < 7:
                    y_low_limit = ball_position_y if ball_position_y > y_low_limit else y_low_limit
                    ky = 1
                else:
                    y_low_limit = ball_position_y - 125
                    ky = -1
            ball_x_direction = kx*(x_low_limit if x_low_limit >= x_upper_limit else random.randint(x_low_limit,x_upper_limit))
            ball_y_direction = ky*(y_low_limit if y_low_limit >= y_upper_limit else random.randint(y_low_limit,y_upper_limit))
    
        if display.is_pressed(display.BUTTON_Y):
            player_one.move_true_left()
        if display.is_pressed(display.BUTTON_X):
            player_one.move_true_right()
        if display.is_pressed(display.BUTTON_B):
            player_two.move_true_left()
        if display.is_pressed(display.BUTTON_A):
            player_two.move_true_right()
        
        ball_position_x += ball_x_direction
        ball_position_y += ball_y_direction