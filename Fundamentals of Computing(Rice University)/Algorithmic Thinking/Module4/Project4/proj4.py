"""
Four function for project #4
"""

def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    """
    Input: a set of characters 'alphabet' and three scores 'diag_score', 'off_diag_score', and 'dash_score'

    Output: 'scoring matrix'
    """
    copy_alphabet = list(alphabet)
    copy_alphabet.append('-')
    scoring_matrix = {row:{col:off_diag_score for col in copy_alphabet} for row in copy_alphabet}
    for dummy_alphabet in copy_alphabet:
        scoring_matrix[dummy_alphabet][dummy_alphabet] = diag_score
        scoring_matrix[dummy_alphabet]['-'] = dash_score
        scoring_matrix['-'][dummy_alphabet] = dash_score

    return scoring_matrix

def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
    """
    Input: two sequences 'seq_x' and 'seq_y' whose elements share a common alphabet with the scoring matrix 'scoring_matrix'

    Output: 'alignment_matrix' for 'seq_x' and 'seq_y'
    """
    len_x = len(seq_x)
    len_y = len(seq_y)
    alignment_matrix = [[0 for col in range(len_y + 1)] for row in range(len_x + 1)]
    if global_flag:
        for col in range(1, len_x + 1):
            alignment_matrix[col][0] = alignment_matrix[col - 1][0] + scoring_matrix[seq_x[col - 1]]['-']
        for row in range(1, len_y + 1):
            alignment_matrix[0][row] = alignment_matrix[0][row - 1] + scoring_matrix['-'][seq_y[row - 1]]
        for col in range(1, len_x + 1):
            for row in range(1, len_y + 1):
                alignment_matrix[col][row] = max([alignment_matrix[col - 1][row - 1] + scoring_matrix[seq_x[col - 1]][seq_y[row - 1]], alignment_matrix[col - 1][row] + scoring_matrix[seq_x[col - 1]]['-'], alignment_matrix[col][row - 1] + scoring_matrix['-'][seq_y[row - 1]]])
    else:
        for col in range(1, len_x + 1):
            alignment_matrix[col][0] = 0
        for row in range(1, len_y + 1):
            alignment_matrix[0][row] = 0
        for col in range(1, len_x + 1):
            for row in range(1, len_y + 1):
                temp_value = max([alignment_matrix[col - 1][row - 1] + scoring_matrix[seq_x[col - 1]][seq_y[row - 1]], alignment_matrix[col - 1][row] + scoring_matrix[seq_x[col - 1]]['-'], alignment_matrix[col][row - 1] + scoring_matrix['-'][seq_y[row - 1]]])
                if temp_value < 0:
                    alignment_matrix[col][row] = 0
                else:
                    alignment_matrix[col][row] = temp_value
    return alignment_matrix

def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    Input: two sequences 'seq_x' and 'seq_y' whose elements share a common alphabet with the scoring matrix 'scoring_matrix', global alignment matrix 'alignment_matrix'.
    Output: global alignment of 'seq_x' and 'seq_y'. The function returns a tuple of the form (score, align_x, align_y) where 'score' is the score of the global alignment 'align_x' and 'align_y'. Note that 'align_x' and 'align_y' should have the same length and may include the padding character '-'.
    """
    idx_x = len(seq_x)
    idx_y = len(seq_y)
    align_x = ''
    align_y = ''
    score = alignment_matrix[idx_x][idx_y]
    while idx_x and idx_y:
        if alignment_matrix[idx_x][idx_y] == alignment_matrix[idx_x - 1][idx_y - 1] + scoring_matrix[seq_x[idx_x - 1]][seq_y[idx_y - 1]]:
            align_x = seq_x[idx_x - 1] + align_x
            align_y = seq_y[idx_y - 1] + align_y
            idx_x -= 1
            idx_y -= 1
        elif alignment_matrix[idx_x][idx_y] == alignment_matrix[idx_x - 1][idx_y] + scoring_matrix[seq_x[idx_x - 1]]['-']:
            align_x = seq_x[idx_x - 1] + align_x
            align_y = '-' + align_y
            idx_x -= 1
        else:
            align_x = '-' + align_x
            align_y = seq_y[idx_y - 1] + align_y
            idx_y -= 1
    while idx_x:
        align_x = seq_x[idx_x - 1] + align_x
        align_y = '-' + align_y
        idx_x -= 1
    while idx_y:
        align_x = '-' + align_x
        align_y = seq_y[idx_y - 1] + align_y
        idx_y -= 1
    return (score, align_x, align_y)

def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    Input: two sequences 'seq_x' and 'seq_y' whose elements share a common alphabet with the scoring matrix 'scoring_matrix', local alignment matrix 'alignment_matrix'.
    Output: local alignment of 'seq_x' and 'seq_y'. The function returns a tuple of the form (score, align_x, align_y) where 'score' is the score of the optimal local alignment 'align_x' and 'align_y'. Note that 'align_x' and 'align_y' should have the same length and may include the padding character '-'.
    """
    align_x = ''
    align_y = ''
    score = 0
    idx_x = 0
    idx_y = 0
    for row in range(len(seq_x) + 1):
        for col in range(len(seq_y) + 1):
            if score < alignment_matrix[row][col]:
                score = alignment_matrix[row][col]
                idx_x = row
                idx_y = col
    idx_y = alignment_matrix[idx_x].index(score)
    while alignment_matrix[idx_x][idx_y]:
        if alignment_matrix[idx_x][idx_y] == alignment_matrix[idx_x - 1][idx_y - 1] + scoring_matrix[seq_x[idx_x - 1]][seq_y[idx_y - 1]]:
            align_x = seq_x[idx_x - 1] + align_x
            align_y = seq_y[idx_y - 1] + align_y
            idx_x -= 1
            idx_y -= 1
        elif alignment_matrix[idx_x][idx_y] == alignment_matrix[idx_x - 1][idx_y] + scoring_matrix[seq_x[idx_x - 1]]['-']:
            align_x = seq_x[idx_x - 1] + align_x
            align_y = '-' + align_y
            idx_x -= 1
        else:
            align_x = '-' + align_x
            align_y = seq_y[idx_y - 1] + align_y
            idx_y -= 1
    return (score, align_x, align_y)
