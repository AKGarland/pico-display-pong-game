import picodisplay as display
import one_player_pong
import two_player_pong
from pens import green, deep_blue

height = display.get_height()
width = display.get_width()
d_buffer = bytearray(width*height*2)
display.init(d_buffer)

display.set_led(0,0,255)
display.set_backlight(1)

if __name__ == '__main__':
    while True:
        display.set_pen(deep_blue)
        display.clear()
        display.set_pen(green)
        display.text('1P         2P',10,10,100,6)
        display.update()
        if display.is_pressed(display.BUTTON_A):
            one_player_pong.play()
        if display.is_pressed(display.BUTTON_B):
            two_player_pong.play()
