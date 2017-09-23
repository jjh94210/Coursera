# Implementation of classic arcade game Pong
# By Jaehwi Cho

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
paddle1_pos = HEIGHT / 2
paddle2_pos = HEIGHT /2
paddle1_vel = 0
paddle2_vel = 0
score1 = 0
score2 = 0

# initialize globals - pos and vel encode info for ball
ball_pos = [0, 0]
ball_vel = [0, 0]

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    if direction:
        ball_vel[0] = random.randrange(120, 240) / 60
        ball_vel[1] = - random.randrange(60, 180) / 60
    else:
        ball_vel[0] = - random.randrange(120, 240) / 60
        ball_vel[1] = - random.randrange(60, 180) / 60

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    score1 = 0
    score2 = 0
    spawn_ball(RIGHT)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel

    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, 'White', 'White')

    # update paddle's vertical position, keep paddle on the screen
    # paddle 1
    paddle1_pos += paddle1_vel
    if paddle1_pos < PAD_HEIGHT / 2:
        paddle1_pos = PAD_HEIGHT / 2
    elif paddle1_pos > (HEIGHT - PAD_HEIGHT / 2):
        paddle1_pos = HEIGHT - PAD_HEIGHT / 2
    #paddle 2
    paddle2_pos += paddle2_vel
    if paddle2_pos < PAD_HEIGHT / 2:
        paddle2_pos = PAD_HEIGHT / 2
    elif paddle2_pos > (HEIGHT - PAD_HEIGHT / 2):
        paddle2_pos = HEIGHT - PAD_HEIGHT / 2

    # draw paddles
    canvas.draw_polygon([[0, paddle1_pos - HALF_PAD_HEIGHT], [0, paddle1_pos + HALF_PAD_HEIGHT], [PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT], [PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT]], 1, 'White', 'White')
    canvas.draw_polygon([[WIDTH, paddle2_pos - HALF_PAD_HEIGHT], [WIDTH, paddle2_pos + HALF_PAD_HEIGHT], [WIDTH - PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT], [WIDTH - PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT]], 1, 'White', 'White')

    # determine whether paddle and ball collide
    # determine the ball collides with and bounces off of the top and bottom walls
    if (ball_pos[1] - (HEIGHT - BALL_RADIUS)) * (ball_pos[1] - BALL_RADIUS) > 0:
        ball_vel[1] = -ball_vel[1]

    # determine the ball touches/collides with the left and right gutters
    # left gutters
    if ball_pos[0] < (PAD_WIDTH + BALL_RADIUS):
        if (ball_pos[1] - (paddle1_pos - HALF_PAD_HEIGHT)) * (ball_pos[1] - (paddle1_pos + HALF_PAD_HEIGHT)) < 0:
            ball_vel[0] = -1.1 * ball_vel[0]
            ball_vel[1] = 1.1 * ball_vel[1]
        else:
            score2 += 1
            spawn_ball(RIGHT)
    # right gutters
    if ball_pos[0] > (WIDTH - PAD_WIDTH - BALL_RADIUS):
        if (ball_pos[1] - (paddle2_pos - HALF_PAD_HEIGHT)) * (ball_pos[1] - (paddle2_pos + HALF_PAD_HEIGHT)) < 0:
            ball_vel[0] = -1.1 * ball_vel[0]
            ball_vel[1] = 1.1 * ball_vel[1]
        else:
            score1 += 1
            spawn_ball(LEFT)

    # draw scores
    canvas.draw_text(str(score1), (WIDTH / 4 - 10, 70), 45, 'White', 'sans-serif')
    canvas.draw_text(str(score2), (3 * WIDTH / 4 - 10, 70), 45, 'White', 'sans-serif')

def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = -7
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = 7
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = -7
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = 7

def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.add_button('Restart', new_game, 100)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

# start frame
new_game()
frame.start()

# http://www.codeskulptor.org/#user43_d4J9pYWIOD_0.py
