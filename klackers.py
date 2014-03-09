# klackers.py

# A Monte Carlo simulation to determine the optimal strategy for playing the game
#  klackers (aka Shut the Box).

import random
import itertools
from numpy import zeros
import json

def combogen(target, tiles):
    '''Generate all combinations that sum to 1-9.
    combogen(int,list of ints) --> list of sets'''

    a = [1,2,3,4,5,6,7,8,9]

    sets = []
    for subset in itertools.chain(*(itertools.combinations(a, n) for n in range(len(a) + 1))):
        if sum(subset) == target:
            sets += [subset]

    used_tiles = set(a) - set(tiles)

    # Test if list contains "used" tiles
    # return False if found <---
    def inusedtiles(alist, used_tiles=used_tiles):
        for anum in alist:
            if anum in used_tiles:
                return False

        return True

    sets = filter(inusedtiles,sets)

    return sets

def removetiles(flipped, tiles):
    '''Remove currently chosen tiles from available tiles list.
    removetiles(sequence,list) --> list'''

    return [tile for tile in tiles if tile not in flipped]

# ------ Choosing functions -----------
def randchoice(sumsets):
    '''Randomly choose a set summing to dice roll.
    randchoice(list of sets) --> set'''

    return random.choice(sumsets)

def mosttiles(sumsets):
    '''Chose tile set with most tiles.
    mosttiles(list of sets) --> set'''

    # Number of tiles in each set, decending order
    # First shuffle sets to avoid choice repetition
    random.shuffle(sumsets)
    tilecounts = sorted(sumsets,key=len,reverse=True)

    return tilecounts[0]

def leasttiles(sumsets):
    '''Chose tile set with least tiles.
    leasttiles(list of sets) --> set'''

    # Number of tiles in each set, ascending order
    # First shuffle sets to avoid choice repetition
    random.shuffle(sumsets)
    tilecounts = sorted(sumsets,key=len,reverse=False)

    return tilecounts[0]

# ----------------------------------------

def montecarlo(chooser,maxgames):
    '''Monte Carlo sequence for Klackers simulation.
    montecarlo(fn,int) --> list of ints'''

    # List to tally resulting scores
    # This is an occurance counter
    scores = zeros(46)

    for game in range(maxgames):
        tiles = [1,2,3,4,5,6,7,8,9]

        reroll = True

        while reroll:
            roll = random.randint(1,6) + random.randint(1,6)
            sets = combogen(roll,tiles)
            if sets == []:
                scores[sum(tiles)] += 1
                reroll = False
            else:
                flip = chooser(sets)
                tiles = removetiles(flip,tiles)

    return scores

def histmean(histo):
    '''Calculate the mean value of a histogram whose bins have integer values.
    histmean(array) --> number

    The score array for klackers has bins ranging from 0-45 of width 1.'''

    return sum([v*c/float(sum(histo)) for v,c in zip(range(46),histo)])

def main():
    '''Run Monte Carlo and write scores to a file'''

    choosers = [randchoice,mosttiles,leasttiles]
    maxgames = 10000000

    for chooser in choosers:
        scores = montecarlo(chooser,maxgames)
        filename = './klackers-'+chooser.func_name+'-'+str(maxgames)+'-games.json'
        with open(filename,'wb') as f:
            json.dump(scores,f)
