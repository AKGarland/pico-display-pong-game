import picodisplay as display
from pens import green, deep_blue

def display_1P_scores():
    viewing = True
    scores = retrieve_1P_scores()
    scores = [str(score) for score in scores] # convert back to string for printing
    while viewing:
        display.set_pen(deep_blue)
        display.clear()
        display.set_pen(green)
        display.text('TOP SCORES',10,10,230,4)
        display.text('x',210,100,200,4)
        display.text(scores[0],10,35,100,4)
        display.text(scores[1],10,65,100,4)
        display.text(scores[2],10,95,100,4)
        display.update()
        
        if display.is_pressed(display.BUTTON_Y):
            viewing = False
    
def retrieve_1P_scores():
    scores_file = open('1_scores.txt','r')
    scores_str = scores_file.read()
    scores_file.close()
    scores = scores_str.split(',')
    scores.pop(len(scores)-1)
    scores_dict = dict.fromkeys(scores) # this removes duplicates  
    scores = list(scores_dict)
    scores = [int(score) for score in scores] # convert to int to allow sorting
    scores.sort(reverse=True) # sort in reverse so highest score is first
    return scores
