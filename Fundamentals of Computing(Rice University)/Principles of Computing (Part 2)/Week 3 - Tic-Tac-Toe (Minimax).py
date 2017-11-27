"""
Mini-max Tic-Tac-Toe Player
"""
# By Jaehwi Cho

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.

    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    move_list = board.get_empty_squares()
    score_list = []
    for dummy_move in move_list:
        current_board = board.clone()
        current_board.move(dummy_move[0], dummy_move[1], player)
        winner = current_board.check_win()
        if winner == player:
            return (SCORES[player], dummy_move)
        elif winner == provided.switch_player(player):
            return (SCORES[provided.switch_player(player)], dummy_move)
        elif winner == provided.DRAW:
            return (SCORES[provided.DRAW], dummy_move)
        else:
            score_list.append((mm_move(current_board, provided.switch_player(player))[0], dummy_move))
    final_score = score_list[0][0]
    final_move = score_list[0][1]
    for dummy_score in score_list:
        if SCORES[player] * final_score < SCORES[player] * dummy_score[0]:
            final_score = dummy_score[0]
            final_move = dummy_score[1]
    return (final_score, final_move)

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(move_wrapper, 1, False)
# poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)

# http://www.codeskulptor.org/#user43_pFZ5GdpDuslGjME.py
