# template for "Stopwatch: The Game"
# By Jaehwi Cho

import simplegui

# define global variables
# t is total time(with tenths of a second)
t = 0
# x is the number of successful stops and y is number of total stops.
x = 0
y = 0
# stoprun is the value determine stopwatch is running
stoprun = False

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    return str(t // 600) + ":" + str(((t // 10) % 60) // 10) + str((t // 10) % 10) + "." + str(t % 10)

# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global stoprun
    stoprun = True
    timer.start()

def stop():
    global stoprun, x, y
    timer.stop()
    if stoprun:
        if (t % 10) == 0:
            x += 1
            y += 1
        else:
            y += 1
        stoprun = False

def reset():
    global stoprun
    stoprun = False
    timer.stop()
    global t, x, y
    t = 0
    x = 0
    y = 0

# define event handler for timer with 0.1 sec interval
def tick():
    global t
    t += 1

# define draw handler
def draw(canvas):
    canvas.draw_text(format(t), (60, 85), 35, "White", "sans-serif")
    canvas.draw_text(str(x) + "/" + str(y), (153, 30), 25, "Green", "sans-serif")

# create frame
frame = simplegui.create_frame("Stopwatch: The Game", 200, 150)

timer = simplegui.create_timer(100, tick)

# register event handlers
frame.add_button("Start", start, 100)
frame.add_button("Stop", stop, 100)
frame.add_button("Reset", reset, 100)

frame.set_draw_handler(draw)

# start frame
frame.start()

# Please remember to review the grading rubric
# http://www.codeskulptor.org/#user43_todXc9TZRq_0.py
