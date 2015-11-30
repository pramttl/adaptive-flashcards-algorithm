"""
2 cards are randomly drawn without replacement (sampled) from the set of cards
Let's say the user takes 10 attempts to learn the first card and 5 seconds to learn
the second card. The simulation will print the cards generated, mle 
"""

MAX_ATTEMPTS_CARD1 = 10
MAX_ATTEMPTS_CARD2 = 5

from api import *
from pprint import pprint
import random

cards_shown = []
algo = FlashcardAlgorithm(1, 0)     # 1st param is weight to weakness dist, and 2nd param is weight to time dist

cues = algo.card.keys()
c1, c2 = random.sample(cues, 2)


for t in xrange(1000):
    cue = algo.draw_card()
    print cue
    cards_shown.append(cue)

    if cue == c1:
        if algo.unknown_count[cue] <= MAX_ATTEMPTS_CARD1:
            algo.reply(cue, 0)
        else:
            algo.reply(cue, 1)

    if cue == c2:
        if algo.unknown_count[cue] <= MAX_ATTEMPTS_CARD2:
            algo.reply(cue, 0)
        else:
            algo.reply(cue, 1)
    else:
        algo.reply(cue, 1)

print "------------------------------------------"
#pprint(cards_shown)
mle_estimates = []
mle_estimates.append(float(cards_shown.count(c1))/len(cards_shown))
mle_estimates.append(float(cards_shown.count(c2))/len(cards_shown))

print "MLE estimates for card c1 and c2"
pprint(mle_estimates)
pprint(algo.draw_dist)
print
print "weakness"
pprint(algo.weakness)
print "------------------------------------------"

print "Card deliberately marked unknown by simulation: ", c1, c2
