from __future__ import division
from weighted_selection import weighted_pick

f = open('data/cards.txt')

# Distribution dictionary
D = {}

lines = f.readlines()

N = len(lines)

for l in lines:
    w, m = l.split('#')
    D[w] = 1/len(lines)

print D

# Starting epsilon value

epsilon = 0.45

while True:
    print "Press e to exit"
    print "Enter 1 if you know card, 0 if you do not:"

    word = weighted_pick(D)

    s = input()

    if s == 1:
        # Increase weight of selected card
        pass
    else:
        # Reduce weight of selected card
        pass

    # Normalize all weights (Perhaps used softmax for normalizing)
