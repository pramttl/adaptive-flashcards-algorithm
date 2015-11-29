from api import *

algo = FlashcardAlgorithm()

while True:
    cue = algo.draw_card()
    print cue

    try:
        s = int(raw_input())
    except:
        # If user entered non integer, quit
        print "Quitting.."
        break
    
    if s == 0:
        print "** ",
        print algo.card[cue] ,
        print " **"
        print

    algo.reply(cue, s)

    print "--------------------"