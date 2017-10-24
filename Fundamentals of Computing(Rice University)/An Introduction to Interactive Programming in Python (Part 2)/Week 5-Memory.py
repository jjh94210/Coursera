# implementation of card game - Memory
# By Jaehwi Cho

import simplegui
import random

# helper function to initialize globals
def new_game():
    global card_deck, exposed, state, total_turns
# to make card deck for game
    card_deck1 = range(0, 8)
    card_deck2 = range(0, 8)
    card_deck = card_deck1 + card_deck2
    random.shuffle(card_deck)
# initialize globals
    exposed = [False] * 16
    state = 0
    total_turns = 0
    label.set_text("Turns = " + str(total_turns))

# define event handlers
def mouseclick(pos):
    # add game state logic here
    global exposed, state, idx1, idx2, total_turns
    current_idx = pos[0] // 50
    if not(exposed[current_idx]):
        exposed[current_idx] = True
        if state == 0:
            state = 1
            idx1 = current_idx
        elif state == 1:
            state = 2
            idx2 = current_idx
            total_turns += 1
            label.set_text("Turns = " + str(total_turns))
        else:
            state = 1
            if card_deck[idx1] != card_deck[idx2]:
                exposed[idx1] = False
                exposed[idx2] = False
            idx1 = current_idx

# cards are logically 50x100 pixels in size
def draw(canvas):
    for i in range(16):
        canvas.draw_text(str(card_deck[i]), (50 * i + 10, 65), 50, 'White', 'sans-serif')
        if not(exposed[i]):
            canvas.draw_polygon([[50 * i, 0], [50 * i, 100], [50 * (i + 1), 100], [50 * (i + 1), 0]], 1, 'Red', 'Green')

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

# Always remember to review the grading rubric
# http://www.codeskulptor.org/#user43_LwR8Uh8bzu_0.py
