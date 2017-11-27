"""
Monte Carlo Tic-Tac-Toe Player
"""
# By Jaehwi Cho

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 7         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player

def mc_trial(board, player):
    """
    This function takes a current board and the next player to move.
    The function should play a game starting with the given player
    by making random moves, alternating between players.
    The function should return when the game is over.
    The modified board will contain the state of the game,
    so the function does not return anything.
    In other words, the function should modify the board input.
    """
    dummy_player = player
    while board.check_win() == None:
        empty_squares = board.get_empty_squares()
        move_target = random.choice(empty_squares)
        board.move(move_target[0], move_target[1], dummy_player)
        dummy_player = provided.switch_player(dummy_player)

def mc_update_scores(scores, board, player):
    """
    This function takes a grid of scores (a list of lists) with the
    same dimensions as the Tic-Tac-Toe board, a board from a completed game,
    and which player the machine player is.
    The function should score the completed board and update the scores grid.
    As the function updates the scores grid directly, it does not return anything.
    """
    state = board.check_win()
    state_constant = 0
    dim = board.get_dim()
    if state == player:
        state_constant = 1.0
    elif state == provided.switch_player(player):
        state_constant = -1.0
    for dummy_row in range(dim):
        for dummy_col in range(dim):
            dummy_square = board.square(dummy_row, dummy_col)
            if dummy_square == player:
                scores[dummy_row][dummy_col] += (state_constant * SCORE_CURRENT)
            elif dummy_square == provided.switch_player(player):
                scores[dummy_row][dummy_col] -= (state_constant * SCORE_OTHER)

def get_best_move(board, scores):
    """
    This function takes a current board and a grid of scores.
    The function should find all of the empty squares with the maximum score
    and randomly return one of them as a (row, column) tuple.
    It is an error to call this function with a board that has no empty squares
    (there is no possible next move), so your function may do whatever it wants in that case.
    The case where the board is full will not be tested.
    """
    empty_squares = board.get_empty_squares()
    if len(empty_squares) == 0:
        return
    max_score = scores[empty_squares[0][0]][empty_squares[0][1]]
    max_score_point = []
    for dummy_square in empty_squares:
        dummy_row = dummy_square[0]
        dummy_col = dummy_square[1]
        if scores[dummy_row][dummy_col] > max_score:
            max_score = scores[dummy_row][dummy_col]
            max_score_point = [(dummy_row, dummy_col)]
        elif scores[dummy_row][dummy_col] == max_score:
            max_score_point.append((dummy_row, dummy_col))
    return random.choice(max_score_point)

def mc_move(board, player, trials):
    """
    This function takes a current board, which player the machine player is,
    and the number of trials to run.
    The function should use the Monte Carlo simulation described above
    to return a move for the machine player in the form of a (row, column) tuple.
    Be sure to use the other functions you have written!
    """
    scores = [[0 for dummy_col in range(board.get_dim())] for dummy_row in range(board.get_dim())]
    for dummy_trial_idx in range(trials):
        dummy_board = board.clone()
        mc_trial(dummy_board, player)
        mc_update_scores(scores, dummy_board, player)
    return get_best_move(board, scores)

# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

# provided.play_game(mc_move, NTRIALS, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)

# http://www.codeskulptor.org/#user43_NzSEqHClogxiuxP.py
