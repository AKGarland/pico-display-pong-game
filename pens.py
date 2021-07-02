import picodisplay as display

height = display.get_height()
width = display.get_width()
d_buffer = bytearray(width*height*2)
display.init(d_buffer)

deep_blue = display.create_pen(0,51,204)
green = display.create_pen(0,255,0)
