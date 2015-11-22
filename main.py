from __future__ import division
from weighted_selection import weighted_pick
import numpy as np

def softmax_norm(D):
    """
    Normalize using softmax function
    D is the distribution dictionary, keys are the card front faces or words.
    Values are the distribution values.
    """
    denominator = 0    # Denominator sum(e^z) of softmax function
    for v in D.values():
        denominator += np.exp(v)

    # Numerators already updated, now updating denominators for all values
    D.update((w, np.exp(v)/denominator) for w, v in D.items())

    print "sumD", sum(D.values())
    return D


f = open('data/cards.txt')

# Distribution dictionary
D = {}

lines = f.readlines()

N = len(lines)

for l in lines:
    w, m = l.split('#')
    D[w] = 1/len(lines)

# Starting epsilon value

# Learning rate (Keep this > 1)
alpha = 2

while True:
    print D
    print "Press e to exit"
    print "Enter 1 if you know card, 0 if you do not:"

    word = weighted_pick(D)
    print word

    s = input()
    print "--------------------"

    if s == 1:
        # If I know a card, reduce its weight
        D[word] = D[word] / alpha
    else:
        # If I don't know a card, increase its weight
        D[word] = D[word] * alpha

    # Normalize all weights (Perhaps use softmax for normalizing)
    D = softmax_norm(D)
