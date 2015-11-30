"""
Random time sleeps between subsequent card pick ups
"""

from api import *
from pprint import pprint
import random
from time import sleep

cards_shown = []
algo = FlashcardAlgorithm(0, 1)     # 1st param is weight to weakness dist, and 2nd param is weight to time dist

for t in xrange(10):
    pprint(algo.get_tdist())
    cue = algo.draw_card()
    cards_shown.append(cue)

    print cue
    random_time_gap = random.randint(1, 2)
    print random_time_gap
    print "---------------"

    sleep(random_time_gap)
    algo.reply(cue, 1)

#pprint(cards_shown)
mle_estimate = float(cards_shown.count('consternation'))/len(cards_shown)

print "======= Simulation Complete ======="
print "consternation_mle_estimate", mle_estimate
pprint(algo.draw_dist)
pprint(algo.weakness)