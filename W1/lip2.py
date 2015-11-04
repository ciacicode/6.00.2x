__author__ = 'ciacicode'
import random


def genEven():
    '''
    Returns a random even number x, where 0 <= x < 100
    '''
    # Your code here
    even = random.randrange(0,101,2)
    return even


def deterministicNumber():
    '''
    Deterministically generates and returns an even number between 9 and 21
    '''
    # Your code here
    random.seed(4)
    detNumber = random.randrange(9,21)
    if detNumber % 2 is 0:
        return detNumber
    else:
        return detNumber+1


def stochasticNumber():
    '''
    Stochastically generates and returns a uniformly distributed even number between 9 and 21
    '''
    # Your code here
    random.SystemRandom()
    stochNumber = random.randrange(9,21)
    if stochNumber % 2 is 0:
        return stochNumber
    else:
        return stochNumber+1
