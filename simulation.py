from api import *
from pprint import pprint

cards_shown = []
algo = FlashcardAlgorithm(1, 0)     # 1st param is weight to weakness dist, and 2nd param is weight to time dist

for t in xrange(1000):
    cue = algo.draw_card()
    cards_shown.append(cue)

    if cue == 'consternation':
        algo.reply(cue, 0)
    else:
        algo.reply(cue, 1)

pprint(cards_shown)
mle_estimate = float(cards_shown.count('consternation'))/len(cards_shown)

print "------------------------------------------"
print "consternation_mle_estimate", mle_estimate
pprint(algo.draw_dist)
pprint(algo.weakness)