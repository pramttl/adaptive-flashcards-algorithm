from __future__ import division
from weighted_selection import weighted_pick
import numpy as np
from pprint import pprint

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

    return D


f = open('data/cards.txt')

# Distribution dictionary
D = {}

# Stores front side to back side hash map
card = {}

lines = f.readlines()

N = len(lines)

for l in lines:
    w, m = l.split('#')
    w, m = w.strip(), m.strip()
    D[w] = 1/len(lines)
    card[w] = m

# Starting epsilon value

# Learning rate (Keep this > 1)
alpha = 2

print "Enter 1 if you know card, 0 if you do not"
print "Print any non numeric character to exit"
print

while True:
    pprint(D)
    print

    word = weighted_pick(D)
    print word

    try:
        s = int(raw_input())
    except:
        print "Quitting.."
        break

    if s == 1:
        # If I know a card, reduce its weight
        D[word] = D[word] / alpha
    else:
        # If I don't know a card, increase its weight
        D[word] = D[word] * alpha
        print "** ",
        print card[word] ,
        print " **"
        print
        print "Press any key to continue.."
        raw_input()

    # Normalize all weights (Perhaps use softmax for normalizing)
    D = softmax_norm(D)

    print "--------------------"