"""
card: A dictionary mapping cue to target.
The terms cue and target are used and the mode of learning is called cued-recall

More specifically for, our flash card algorithm being used for vocabulary learning.
- cue is the  word
- target is the meaning of the word
"""

from __future__ import division
import math
from weighted_selection import weighted_pick
import numpy as np
from datetime import datetime
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

def complementary_dict(D):
    """
    Returns dict with 1 - current value in input dict
    """
    complement = {}
    for k in D.keys():
        complement[k] = 1 - D[k]
    return complement

def get_telapsed(last_draw_timestamp):
    """
    Takes in a dictionary that shows last-draw timestamp for each card
    and uses that to compute

    Returns: Time elapsed dictionary that shows seconds elapsed since last time each card was drawn
             (Key is the cue and value is seconds elapsed)
    """
    telapsed = {}
    now = datetime.now()
    for cue, tstamp in last_draw_timestamp.items():
        telapsed[cue] = (now - tstamp).seconds        #XXX: Not sure if we should make this microseconds
    return telapsed


def get_expectation_of_recall(tdist, strength):
    """
    :tdist: Normalized distribution of time elapsed since last time each card was shown
    :strength: Strength distribution

    :return: E_recall dictionary, which gives expected value of recalling each word

    # Calculation of E(Recall) based on human forgetting curve, described in paper
    # Memory: A Contribution to Experimental Psychology
    # Idea reused in Microsoft Research paper: http://research.microsoft.com/en-us/people/daedge/memreflex.pdf
    # Msft paper does not give details on the algorithm itself, also there is no indication whether strength
    # and timedist values are normalized in computing E(Recall) which may be important in our opinion

    Assumption: tdist, strength have the same keys which are the cues
    """
    E_recall = {}
    for cue in tdist.keys():
        t = tdist[cue]        # Normalized time elapsed for this card
        s = strength[cue]     # Normalized relative strength for this card
        E_recall[cue] = math.exp(-t/s)
    return E_recall

#############################################################
######  Distribution dictionaries (cues are the keys)  ######
#############################################################
draw_dist = {}                  # Final distribution used to draw a card
strength = {}                   # Strength distribution

# Stores front side to back side hash map
card = {}                       # cue-target dictionary
last_draw_timestamp = {}        # cue-lastshown timestamp dictionary

# Loading the card dictionary from a data files
f = open('data/cards.txt')
lines = f.readlines()
N = len(lines)

for l in lines:
    cue, target = l.split('#')
    cue, target = cue.strip(), target.strip()
    strength[cue] = 1/len(lines)
    card[cue] = target

# Starting epsilon value

# Learning rate (Keep this > 1)
alpha = 10

print "Enter 1 if you know card, 0 if you do not"
print "Print any non numeric character to exit"
print

# Initialize last_draw_timestamp to current time for all cards
#XXX: Ideally these should be stored into a database or pickled to a file and reused at each restart
now = datetime.now()
for cue in card.keys():
    last_draw_timestamp[cue] = now

while True:
    #pprint(draw_dist)
    #pprint(strength)
    #print

    telapsed = get_telapsed(last_draw_timestamp)
    tdist = softmax_norm(telapsed)                          # Time elapsed distribution
    E_recall = get_expectation_of_recall(tdist, strength)   # This dict indicates relative strength of recall of each card
                                                            # Note: recall relative strength is different from strength
                                                            # It also depends on number of seconds elapsed since card was last shown
    
    E_notrecall = complementary_dict(E_recall)              # Relative strength of not-recalling a word
    draw_dist = softmax_norm(E_notrecall)

    # Draw a card from the distribution
    cue = weighted_pick(draw_dist)               # Draw distribution should be updated as per the new times just before drawing a new card
    #cue = weighted_pick(strength)
    
    last_draw_timestamp[cue] = datetime.now()    # Update last shown time of card drawn to current time

    print cue

    try:
        s = int(raw_input())
    except:
        print "Quitting.."
        break

    if s == 1:
        # Learner knows card, reduce its weight
        strength[cue] = strength[cue] / alpha
    else:
        # Learner does not know a card, increase its weight
        strength[cue] = strength[cue] * alpha
        print "** ",
        print card[cue] ,
        print " **"
        print

    # Normalize all weights (Perhaps use softmax for normalizing)
    strength = softmax_norm(strength)

    print "--------------------"