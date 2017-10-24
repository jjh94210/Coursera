# Mini-project #6 - Blackjack
# By Jaehwi Cho

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

# initialize some useful global variables
in_play = False
outcome_dealer = ""
outcome_player = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)


# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.card_list = []

    def __str__(self):
        # return a string representation of a hand
        output = "Hand contains "
        for i in range(len(self.card_list)):
            output += (str(self.card_list[i]) + " ")
        return output

    def add_card(self, card):
        # add a card object to a hand
        self.card_list.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        self.value = 0
        for i in range(len(self.card_list)):
            self.value += VALUES[self.card_list[i].get_rank()]
        for i in range(len(self.card_list)):
            if (self.card_list[i].get_rank() == 'A') and self.value <= 11:
                self.value += 10
        return self.value

    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        self.pos = pos
        for i in range(len(self.card_list)):
            self.card_list[i].draw(canvas, self.pos)
            self.pos[0] += (4.0 / 3.0) * CARD_SIZE[0]


# define deck class
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck = []
        for i in range(len(SUITS)):
            for j in range(len(RANKS)):
                self.deck.append(Card(SUITS[i], RANKS[j]))

    def shuffle(self):
        # shuffle the deck
        # use random.shuffle()
        random.shuffle(self.deck)

    def deal_card(self):
        # deal a card object from the deck
        return self.deck.pop(len(self.deck) - 1)

    def __str__(self):
        # return a string representing the deck
        output = "Deck contains "
        for i in range(len(self.deck)):
            output += (self.deck[i].get_suit() + self.deck[i].get_rank() + " ")
        return output


#define event handlers for buttons
def deal():
    global outcome_dealer, outcome_player, in_play, score

    # your code goes here
    global dealer, player
    global deck

    deck = Deck()
    deck.shuffle()
    dealer = Hand()
    player = Hand()
    for i in range(2):
        player.add_card(deck.deal_card())
        dealer.add_card(deck.deal_card())
    outcome_dealer = ""
    outcome_player = "Hit or stand?"
    if in_play:
        score -= 1
    in_play = True

def hit():
    # replace with your code below
    global player, outcome_dealer, outcome_player, in_play, score

    # if the hand is in play, hit the player
    if in_play:
        player.add_card(deck.deal_card())
    # if busted, assign a message to outcome, update in_play and score
        if player.get_value() > 21:
            in_play = False
            outcome_dealer = "You went bust and lose."
            outcome_player = "New deal?"
            score -= 1

def stand():
    # replace with your code below
    global player, dealer, in_play, outcome_dealer, outcome_player, score

    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        while dealer.get_value() < 17:
            dealer.add_card(deck.deal_card())

    # assign a message to outcome, update in_play and score
        if dealer.get_value() > 21:
            outcome_dealer = "Dealer went bust and you win."
            score += 1
        elif dealer.get_value() >= player.get_value():
            outcome_dealer = "You lose."
            score -= 1
        else:
            outcome_dealer = "You win."
            score += 1
        in_play = False
    outcome_player = "New deal?"

# draw handler
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    dealer.draw(canvas, [1.0 * CARD_SIZE[0], 600 - 4.2 * CARD_SIZE[1]])
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [1.0 * CARD_BACK_SIZE[0] + CARD_BACK_CENTER[0], 600 - 4.2 * CARD_BACK_SIZE[1] + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
    player.draw(canvas, [1.0 * CARD_SIZE[0], 600 - 2.1 * CARD_SIZE[1]])

    canvas.draw_text('Dealer', (1.0 * CARD_SIZE[0], 600 - 4.5 * CARD_SIZE[1]), 27, 'Black', 'sans-serif')
    canvas.draw_text('Player', (1.0 * CARD_SIZE[0], 600 - 2.4 * CARD_SIZE[1]), 27, 'Black', 'sans-serif')
    canvas.draw_text(outcome_dealer, (3.0 * CARD_SIZE[0] , 600 - 4.5 * CARD_SIZE[1]), 27, 'Black', 'sans-serif')
    canvas.draw_text(outcome_player, (3.0 * CARD_SIZE[0] , 600 - 2.4 * CARD_SIZE[1]), 27, 'Black', 'sans-serif')

    canvas.draw_text('Blackjack', ((4.0 / 3.0) * CARD_SIZE[0], CARD_SIZE[1]), 48, 'Aqua', 'sans-serif')
    canvas.draw_text('Score ' + str(score), (5.2 * CARD_SIZE[0], CARD_SIZE[1]), 27, 'Black', 'sans-serif')

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()

# remember to review the gradic rubric
# http://www.codeskulptor.org/#user43_t6xUDcXkQg_0.py
