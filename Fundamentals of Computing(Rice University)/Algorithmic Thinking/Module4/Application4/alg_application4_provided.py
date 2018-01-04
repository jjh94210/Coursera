"""
Provide code and solution for Application 4
"""

DESKTOP = True

import math
import random
import urllib2
import time

if DESKTOP:
    import matplotlib.pyplot as plt
    import alg_project4_solution as student
else:
    import simpleplot
    import userXX_XXXXXXX as student
    

# URLs for data files
PAM50_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_PAM50.txt"
HUMAN_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_HumanEyelessProtein.txt"
FRUITFLY_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_FruitflyEyelessProtein.txt"
CONSENSUS_PAX_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_ConsensusPAXDomain.txt"
WORD_LIST_URL = "http://storage.googleapis.com/codeskulptor-assets/assets_scrabble_words3.txt"



###############################################
# provided code

def read_scoring_matrix(filename):
    """
    Read a scoring matrix from the file named filename.  

    Argument:
    filename -- name of file containing a scoring matrix

    Returns:
    A dictionary of dictionaries mapping X and Y characters to scores
    """
    scoring_dict = {}
    scoring_file = urllib2.urlopen(filename)
    ykeys = scoring_file.readline()
    ykeychars = ykeys.split()
    for line in scoring_file.readlines():
        vals = line.split()
        xkey = vals.pop(0)
        scoring_dict[xkey] = {}
        for ykey, val in zip(ykeychars, vals):
            scoring_dict[xkey][ykey] = int(val)
    return scoring_dict


def read_protein(filename):
    """
    Read a protein sequence from the file named filename.

    Arguments:
    filename -- name of file containing a protein sequence

    Returns:
    A string representing the protein
    """
    protein_file = urllib2.urlopen(filename)
    protein_seq = protein_file.read()
    protein_seq = protein_seq.rstrip()
    return protein_seq


def read_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    # load assets
    word_file = urllib2.urlopen(filename)
    
    # read in files as string
    words = word_file.read()
    
    # template lines and solution lines list of line string
    word_list = words.split('\n')
    print "Loaded a dictionary with", len(word_list), "words"
    return word_list


# Q1
HumanEyelessProtein = read_protein(HUMAN_EYELESS_URL)
FruitflyEyelessProtein = read_protein(FRUITFLY_EYELESS_URL)

PAM50 = read_scoring_matrix(PAM50_URL)

alignment_matrix_Q1 = student.compute_alignment_matrix(HumanEyelessProtein, FruitflyEyelessProtein, PAM50, False)

result_Q1 = student.compute_local_alignment(HumanEyelessProtein, FruitflyEyelessProtein, PAM50, alignment_matrix_Q1)

# Q2
TempHumanSeq = result_Q1[1]
FruitflySeq = result_Q1[2]
HumanSeq = TempHumanSeq[:len(TempHumanSeq) - 3] + TempHumanSeq[len(TempHumanSeq) - 2:]

ConsensusPAXDomain = read_protein(CONSENSUS_PAX_URL)

alignment_matrix_Q2_Human = student.compute_alignment_matrix(HumanSeq, ConsensusPAXDomain, PAM50, True)
alignment_matrix_Q2_Fruitfly = student.compute_alignment_matrix(FruitflySeq, ConsensusPAXDomain, PAM50, True)

result_Q2_Human = student.compute_global_alignment(HumanSeq, ConsensusPAXDomain, PAM50, alignment_matrix_Q2_Human)
result_Q2_Fruitfly = student.compute_global_alignment(FruitflySeq, ConsensusPAXDomain, PAM50, alignment_matrix_Q2_Fruitfly)

def calculate_score(seq1, seq2):
    if len(seq1) != len(seq2):
        print "Wrong!"
        return
    else:
        num_equal = 0
        for dummy_idx in range(len(seq1)):
            if seq1[dummy_idx] == seq2[dummy_idx]:
                num_equal += 1
        return (float(num_equal) / float(len(seq1)) * 100)

print 'Human :'
print calculate_score(result_Q2_Human[1], result_Q2_Human[2])
print 'Fruitfly :'
print calculate_score(result_Q2_Fruitfly[1], result_Q2_Fruitfly[2])

# Q4
def generate_null_distribution(seq_x, seq_y, scoring_matrix, num_trial):
    
    scoring_distribution = dict()

    for dummy_idx in range(num_trial):
        rand_y = list(seq_y)
        random.shuffle(rand_y)
        rand_y = ''.join(rand_y)
        alignment_matrix = student.compute_alignment_matrix(seq_x, rand_y, scoring_matrix, False)
        result = student.compute_local_alignment(seq_x, rand_y, scoring_matrix, alignment_matrix)
        score = result[0]
        if scoring_distribution.has_key(score):
            scoring_distribution[score] += 1
        else:
            scoring_distribution[score] = 1
    return scoring_distribution

start = time.time()
num_trial = 1000
scoring_distribution = generate_null_distribution(HumanEyelessProtein, FruitflyEyelessProtein, PAM50, num_trial)
end = time.time() - start
print end

scores = []
number_of_score = []

for score in scoring_distribution.keys():
    scores.append(score)
    number_of_score.append(scoring_distribution[score] / float(num_trial))

plt.figure()
plt.bar(scores, number_of_score)
plt.title('Null distribution for hypothesis testing(1000 trials)')
plt.xlabel('Scores')
plt.ylabel('Fraction of trials(number_of_score/total_trials)')
plt.show()

# Q5
mean = 0
sigma = 0

for idx in range(len(scores)):
    mean += scores[idx] * number_of_score[idx]

for idx in range(len(scores)):
    sigma += (((scores[idx] - mean) * (scores[idx] - mean)) * number_of_score[idx])

sigma = math.sqrt(sigma)

alignment_matrix_Q5 = student.compute_alignment_matrix(HumanEyelessProtein, FruitflyEyelessProtein, PAM50, False)
result_Q5 = student.compute_local_alignment(HumanEyelessProtein, FruitflyEyelessProtein, PAM50, alignment_matrix_Q5)

z_value = (result_Q5[0] - mean) / sigma

print 'mean : '+ str(mean)
print 'standard deviation : ' + str(sigma)
print 'z value : ' + str(z_value)

# Q8
word_list = read_words(WORD_LIST_URL)

scoring_matrix = student.build_scoring_matrix('abcdefghijklmnopqrstuvwxyz', 2, 1, 0)

def check_spelling(checked_word, dist, word_list):
    answer = []
    for word in word_list:
        alignment_matrix = student.compute_alignment_matrix(checked_word, word, scoring_matrix, True)
        result = student.compute_local_alignment(checked_word, word, scoring_matrix, alignment_matrix)
        if (len(checked_word) + len(word) - result[0]) <= dist:
            answer.append(word)
    return answer

print check_spelling('humble', 1, word_list)
print check_spelling('firefly', 2, word_list)
