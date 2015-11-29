from api import *
from pprint import pprint

cards_shown = []
for t in xrange(10000):
    algo = FlashcardAlgorithm()
    cue = algo.draw_card()
    cards_shown.append(cue)

    if cue == 'consternation':
        algo.reply(cue, 0)
    else:
        algo.reply(cue, 1)

pprint(cards_shown)
unknown_count = cards_shown.count('consternation')
mle_estimate = float(unknown_count)/len(cards_shown)

print "consternation_mle_estimate", mle_estimate
print algo.draw_dist