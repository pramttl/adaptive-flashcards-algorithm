from api import *
from pprint import pprint

cards_shown = []
for t in xrange(20):
    algo = FlashcardAlgorithm()
    #if t==0:
    #   print 'initial', algo.draw_dist
    cue = algo.draw_card()
    cards_shown.append(cue)

    if cue == 'consternation':
        algo.reply(cue, 0)
    else:
        algo.reply(cue, 1)

    #print cue
    #print algo.draw_dist
    #print "------------------------------------------"

pprint(cards_shown)
unknown_count = cards_shown.count('consternation')
mle_estimate = float(unknown_count)/len(cards_shown)

print "------------------------------------------"
print "consternation_mle_estimate", mle_estimate
print pprint(algo.draw_dist)
print pprint(algo.strength)