########
# author: Ritesh Pradhan
# Codeskulptor project
# Pong
########


# Input arguments and flags:
# Ouput:
# 
# Assumptions: 
#   1. 
# Known issues:
#   1. How to disable a button
###Functions:
# 0. main                   : Control the program's flow
###Helper functions:
# 1. did_ball_touch_paddle  : Tells if ball has indeed hit a paddle
# 2. ball_init              : Resets ball position
# 3. ball_vel_change(plane) : Changes velocity - any one component of velocity vector - either X or Y
# 4. calculate_positions    : Calculates ball and paddle posistions, gets called from draw()
#### Event Handlers:
# 1. pause_game             : Pase button >>/||
# 2. new_game               : Reset button
# 3. draw                   : Draw upon canvas
# 4. keydown                : 
# 5. keyup                  :
###
###Change History:
# DATE    PRG  REASON
############################################################################################
# 20130514 YM   First release
#
############################################################################################
# Imported/external modules:
import simplegui
import random
import math
#
# initialize globals - pos and vel encode vertical info for paddles
###Globals
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
BALL_VEL_INCREMENT=1.1
PAD_VEL_INCREMENT=10
##
MAX_SPEED=50000
LEFT=1
RIGHT=2
#floats
paddle1_pos=[0.0,0.0]
paddle1_vel=[0.0,0.0]
#
paddle2_pos=[0.0,0.0]
paddle2_vel=[0.0,0.0]
#
ball_pos=[0.0, 0.0]
ball_vel=[0.0, 0.0]
BALL_STARTING_VEL=[1.0,-1.0]
#int
score1=0
score2 =0
x_direction=-1
y_direction=-1
###
current_key = ' '
###Flags
fGameInProgress=False
fPauseGame=False
####
##Global Controls - to be used for controls getting used in helper functinos
bPause=None
###
#Helper-functions    
def did_ball_touch_paddle(ball, paddle,whichpaddle):
############################################################################################
# Returns bool to indicate if ball has indeed touch the paddle
############################################################################################
   if  ( whichpaddle == RIGHT ):
       distance_from_edge = -PAD_WIDTH
   else:
       distance_from_edge = +PAD_WIDTH
#
   if( (ball[1] - BALL_RADIUS < paddle[1] + HALF_PAD_HEIGHT ) and (ball[1] + BALL_RADIUS> paddle[1] - HALF_PAD_HEIGHT )):
        if ( abs(ball[0] - paddle[0] - distance_from_edge ) <= BALL_RADIUS):
             return True
#
   return False
#
###

def ball_init(right):
############################################################################################
# Resets ball position
############################################################################################
    global ball_pos, ball_vel, y_direction # these are vectors stored as lists
#
    if fGameInProgress == False:
        ball_pos=[WIDTH/2, HEIGHT/2]
        ball_vel[0]=BALL_STARTING_VEL[0] + ( score1 + score2 )/2
        ball_vel[1]=BALL_STARTING_VEL[1] + ( score1 + score2 )/2
        ball_vel[0]=ball_vel[0]*x_direction
        ball_vel[1]=ball_vel[1]*y_direction
#
    if ((int(random.random()*10000)%2) == 0 ):
             y_direction=-1
    else:
             y_direction=1
#
    return
###
###
def ball_vel_change(plane):
############################################################################################
# Changes velocity - any one component of velocity vector - either X or Y
# plane - horizontal - X or Vertical - Y
############################################################################################
###
    global ball_vel
    if (plane=="Horizontal"):
        ball_vel[0]*=BALL_VEL_INCREMENT
        if (abs(ball_vel[0]) > MAX_SPEED):
            ball_vel[0]= ( ball_vel[0] / abs(ball_vel[0])) * MAX_SPEED
    elif(plane=="Vertical"):
        ball_vel[1]*=BALL_VEL_INCREMENT
        if (abs(ball_vel[1]) > MAX_SPEED):
            ball_vel[1]= ( ball_vel[1] /  abs(ball_vel[1])) * MAX_SPEED
    return
###
def calculate_positions():
############################################################################################
# Calculates ball and paddle posistions, gets called from draw()
############################################################################################
###
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, fGameInProgress, x_direction, y_direction
# 
### update paddle's vertical position, keep paddle on the screen
    paddle1_pos[0] = paddle1_pos[0] + paddle1_vel[0]
    paddle1_pos[1] = paddle1_pos[1] + paddle1_vel[1]
    if  ( paddle1_pos[1] + HALF_PAD_HEIGHT >= HEIGHT or paddle1_pos[1] - HALF_PAD_HEIGHT <= 0):
        paddle1_vel[1]=0
#
    paddle2_pos[0]=paddle2_pos[0]+paddle2_vel[0]
    paddle2_pos[1]=paddle2_pos[1]+paddle2_vel[1]
    if  ( paddle2_pos[1] + HALF_PAD_HEIGHT >= HEIGHT or paddle2_pos[1] - HALF_PAD_HEIGHT <= 0):
        paddle2_vel[1]=0
#

    if ( paddle1_pos[1] + HALF_PAD_HEIGHT + HALF_PAD_WIDTH > HEIGHT):
         paddle1_pos[1] -= HALF_PAD_WIDTH
    if ( paddle1_pos[1] -  HALF_PAD_HEIGHT < 0):
         paddle1_pos[1] = HALF_PAD_HEIGHT
#
    if ( paddle2_pos[1] + HALF_PAD_HEIGHT + HALF_PAD_WIDTH > HEIGHT):
         paddle2_pos[1] -= HALF_PAD_WIDTH
    if ( paddle2_pos[1] -  HALF_PAD_HEIGHT < 0):
         paddle2_pos[1] = HALF_PAD_HEIGHT
#
### Update ball position
    ball_pos[0]=ball_pos[0]+ball_vel[0]
    ball_pos[1]=ball_pos[1]+ball_vel[1]
###Bounce off the top, and the bottom edges of play-area:
    if ( ball_pos[1] - BALL_RADIUS <= 0 or ball_pos[1] + BALL_RADIUS > HEIGHT):
        ball_vel_change("Vertical")
        ball_vel[1] = -ball_vel[1]
###Bounce off the paddles:
####LEFT Paddle
    if ( did_ball_touch_paddle(ball_pos, paddle1_pos, LEFT) == True ):
        ball_vel_change("Horizontal")
        ball_vel[0] = -ball_vel[0] 
        fGameInProgress = False
####RIGHT Paddle
    if ( did_ball_touch_paddle(ball_pos, paddle2_pos,RIGHT) == True):
        ball_vel_change("Horizontal")
        ball_vel[0] = -ball_vel[0]
        fGameInProgress = False
#
    if ( ball_pos[0] < PAD_WIDTH+BALL_RADIUS and fGameInProgress ):
       score2 += 1
       x_direction=1
       fGameInProgress = False
       ball_init(-999)
#
    if ( ball_pos[0] > WIDTH - PAD_WIDTH - BALL_RADIUS and fGameInProgress ):
       score1 += 1
       x_direction=-1
       fGameInProgress = False
       ball_init(-999)
#
    fGameInProgress = True
    return
###     
# Define Event Handlers
def pause_game():
############################################################################################
# new / reset game
############################################################################################
###
    global fPauseGame, bPause
    fPauseGame = not fPauseGame
    if  fPauseGame:
        bPause.set_text(">")
    else:
         bPause.set_text("||")
#
    return
###
def new_game():
############################################################################################
# new / reset game
############################################################################################
###
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, ball_pos # these are floats
    global score1, score2 , x_direction , y_direction  # these are ints
    global fGameInProgress, fPauseGame

    paddle1_pos=[0,HEIGHT/2]
    paddle2_pos=[WIDTH,HEIGHT/2]

    paddle1_vel=[0.0,0.0]
    paddle2_vel=[0.0,0.0]
#
    score1=0
    score2 =0
#
    if ((int(random.random()*10000)%2) == 0 ):
             x_direction=-1
    else:
             x_direction=1
#
    fGameInProgress=False
    fPauseGame=False
    ball_init(-9999)
    ball_pos=[WIDTH/2, HEIGHT/2]
#
    return
###
def draw(c):
############################################################################################
#
############################################################################################
###
    global fPauseGame
#
    if not fPauseGame:
        calculate_positions()
    c.draw_polygon([ (0, HEIGHT), (WIDTH,HEIGHT),(WIDTH,HEIGHT+50),(0,HEIGHT+50)],0.001,"Grey","Teal") 
#
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
#   
# draw paddles

###Left:
    c.draw_polygon([(paddle1_pos[0]-HALF_PAD_WIDTH, paddle1_pos[1]+HALF_PAD_HEIGHT ),( paddle1_pos[0]+HALF_PAD_WIDTH, paddle1_pos[1]+HALF_PAD_HEIGHT ),( paddle1_pos[0]+HALF_PAD_WIDTH, paddle1_pos[1]-HALF_PAD_HEIGHT ), ( paddle1_pos[0]-HALF_PAD_WIDTH, paddle1_pos[1]- HALF_PAD_HEIGHT )], PAD_WIDTH, "White")
###Right:
    c.draw_polygon([(paddle2_pos[0]-HALF_PAD_WIDTH, paddle2_pos[1]+HALF_PAD_HEIGHT ),( paddle2_pos[0]+HALF_PAD_WIDTH, paddle2_pos[1]+HALF_PAD_HEIGHT ),( paddle2_pos[0]+HALF_PAD_WIDTH, paddle2_pos[1]-HALF_PAD_HEIGHT ), ( paddle2_pos[0]-HALF_PAD_WIDTH, paddle2_pos[1]- HALF_PAD_HEIGHT )], PAD_WIDTH, "Yellow")

    # Draw Ball 
    c.draw_circle((ball_pos[0], ball_pos[1]), BALL_RADIUS, 1, "Green","Red")
    # Draw Scores
    c.draw_text (str(score1), (100, HEIGHT+40),40, "White","monospace")
    c.draw_text (str(score2), [WIDTH/2+100,HEIGHT+40],40, "Yellow","monospace")
#
    return
###     
def keydown(key):
############################################################################################
#
############################################################################################
###
    global paddle1_vel, paddle2_vel
    if key==simplegui.KEY_MAP["up"]:
         paddle2_vel[1]= paddle2_vel[1] - PAD_VEL_INCREMENT
    elif key==simplegui.KEY_MAP["down"]:
         paddle2_vel[1]= paddle2_vel[1] + PAD_VEL_INCREMENT 
###
    elif key==simplegui.KEY_MAP["w"]:
         paddle1_vel[1]= paddle1_vel[1] - PAD_VEL_INCREMENT
    elif key==simplegui.KEY_MAP["s"]:
         paddle1_vel[1]= paddle1_vel[1] + PAD_VEL_INCREMENT    
##
    elif key==simplegui.KEY_MAP["space"]:
         pause_game()
#
    return
###   
def keyup(key):
############################################################################################
# Handler
############################################################################################
###
    global paddle1_vel, paddle2_vel
#
    global paddle1_vel, paddle2_vel
    if ( key==simplegui.KEY_MAP["up"] or key==simplegui.KEY_MAP["down"] ):
       paddle2_vel[1]=0.0
###
    elif ( key==simplegui.KEY_MAP["w"] or key==simplegui.KEY_MAP["s"] ):
        paddle1_vel[1]=0.0
    return
def main():
############################################################################################
#Control the program-flow
#1. Create frame
#2. Add/register controls
#3. Start the frame
############################################################################################
    """main - control the program flow
    """
    global bPause
# create frame
    frame = simplegui.create_frame("Pong", WIDTH, HEIGHT+50)
    frame.set_draw_handler(draw)
    frame.set_keydown_handler(keydown)
    frame.set_keyup_handler(keyup)
    bPause = frame.add_button("||",  pause_game, 30)
    bStart = frame.add_button("Reset",  new_game, 100)
# start frame
    frame.start()
#
    new_game()
    return
###
###Finally - don't run if this program is 'imported''
if __name__ == "__main__":
     main()
#
###End Of Program