# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
# By Jaehwi Cho

import simplegui
import random
import math

# Initiallize number range and remaining gussess
num_range = 100
remaining_gussess = 0

# helper function to start and restart the game
def new_game():
    global secret_number
    secret_number = random.randrange(0, num_range)
    print "\nNew game. Range is [0," + str(num_range) + ")"
    global remaining_gussess
    remaining_gussess = int(math.ceil(math.log(num_range + 1, 2)))
    print "Number of remaining guesses is", remaining_gussess

# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game
    global num_range
    num_range = 100
    new_game()


def range1000():
    # button that changes the range to [0,1000) and starts a new game
    global num_range
    num_range = 1000
    new_game()

def input_guess(guess):
    # main game logic goes here
    guess_number = int(guess)
    print "\nGuess was", guess_number
    global remaining_gussess
    if(remaining_gussess == 1 and guess_number != secret_number):
        remaining_gussess -= 1
        print "Number of remaining guesses is", remaining_gussess
        print "You ran out of guesses. The number was", secret_number
        new_game()
    elif(guess_number < secret_number):
        remaining_gussess -= 1
        print "Number of remaining guesses is", remaining_gussess
        print "Higher!"
    elif(guess_number > secret_number):
        remaining_gussess -= 1
        print "Number of remaining guesses is", remaining_gussess
        print "Lower!"
    else:
        remaining_gussess -= 1
        print "Number of remaining guesses is", remaining_gussess
        print "Correct!"
        new_game()

# create frame

    """frame of the guessing game"""
frame = simplegui.create_frame("Guess the number", 200, 200)

# register event handlers for control elements and start frame
frame.add_button("Range is [0, 100)", range100, 200)
frame.add_button("Range is [0, 1000)", range1000, 200)
frame.add_input("Enter a guess", input_guess, 200)
frame.start()

# call new_game 
new_game()

# always remember to check your completed program against the grading rubric
# http://www.codeskulptor.org/#user43_YJfwAc31gv_0.py
