"""
The first card shown is marked unknown everytime it is encountered
"""

from api import *
from pprint import pprint

cards_shown = []
algo = FlashcardAlgorithm(1, 0)     # 1st param is weight to weakness dist, and 2nd param is weight to time dist

for t in xrange(1000):
    cue = algo.draw_card()
    print cue

    if t == 0:
        # Assuming first card shown will be marked as the unknown card
        unknown_card = cue

    cards_shown.append(cue)

    if cue == unknown_card:
        algo.reply(cue, 0)
    else:
        algo.reply(cue, 1)

#pprint(cards_shown)
mle_estimate = float(cards_shown.count(unknown_card))/len(cards_shown)

print "------------------------------------------"
print "unknown_card_mle_estimate", mle_estimate
pprint(algo.draw_dist)
print
print "weakness"
pprint(algo.weakness)
print "------------------------------------------"

print "Card deliberately marked unknown by simulation: ", unknown_card