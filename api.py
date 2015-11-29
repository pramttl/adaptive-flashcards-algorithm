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


def weighted_combination(weights, distributions):
    """
    Returns a new distribution which is weighted combination of input distributions.
    weight0 corresponds to distribution0, weight1 to distribution1 and so on ...
    """
    assert sum(weights) == float(1)

    newd = {}
    ndist = len(distributions)

    cues = distributions[0].keys()

    for cue in cues:
        weighted_sum = 0
        for i in range(ndist):
            weighted_sum += weights[i] * distributions[i][cue]
        newd[cue] = weighted_sum

    return newd


class FlashcardAlgorithm():

    learning_rate = 10

    # Distribution dictionaries (cues are the keys)
    draw_dist = {}                  # Final distribution used to draw a card
    strength = {}                   # Strength distribution

    # Stores front side to back side hash map
    card = {}                       # cue-target dictionary
    last_draw_timestamp = {}        # cue-lastshown timestamp dictionary

    def __init__(self, learning_rate=10, data_file='data/cards.txt'):
        """
        Initialize the adaptive flash card algorithm
        """

        self.learning_rate = learning_rate

        # Loading the card dictionary from a data files
        f = open(data_file)
        lines = f.readlines()
        N = len(lines)

        for l in lines:
            cue, target = l.split('#')
            cue, target = cue.strip(), target.strip()
            self.strength[cue] = 1/len(lines)
            self.card[cue] = target

        # Initialize last_draw_timestamp to current time for all cards
        #XXX: Ideally these should be stored into a database or pickled to a file and reused at each restart
        now = datetime.now()
        for cue in self.card.keys():
            self.last_draw_timestamp[cue] = now

        self.state = 'WAIT_DRAW_CARD'

    def draw_card(self):
        """
        Returns next card (just the cue is returned)
        card[cue] can be used to get the target
        """
        telapsed = get_telapsed(self.last_draw_timestamp)
        tdist = softmax_norm(telapsed)                              # Time elapsed distribution

        #E_recall = get_expectation_of_recall(telapsed, self.strength)  # This dict indicates relative strength of recall of each card
                                                                    # Note: recall relative strength is different from strength
                                                                    # It also depends on number of seconds elapsed since card was last shown
        
        #E_notrecall = complementary_dict(E_recall)                  # Relative strength of not-recalling a word

        self.draw_dist = weighted_combination([1,0], [self.strength, tdist])

        # Draw a card from the distribution
        cue = weighted_pick(self.strength)               # Draw distribution should be updated as per the new times just before drawing a new card
        self.last_draw_timestamp[cue] = datetime.now()    # Update last shown time of card drawn to current time

        return cue


    def reply(self, cue, resp):
        """
        Reply from the human learner, whether he knows the card or not.
        1 if learner knows card, 0 if it doesn't (Binary feedback)
        """
        if resp == 1:
            # Learner knows card, increase the strength
            self.strength[cue] = self.strength[cue] / self.learning_rate
        else:
            # Learner does not know a card, reduce the strength
            self.strength[cue] = self.strength[cue] * self.learning_rate

        # Normalize all weights (Perhaps use softmax for normalizing)
        self.strength = softmax_norm(self.strength)

        pprint(self.strength)
        return True
