__author__ = 'ciacicode'

import random, pylab
import pdb

# You are given this function
def getMeanAndStd(X):
    mean = sum(X)/float(len(X))
    tot = 0.0
    for x in X:
        tot += (x - mean)**2
    std = (tot/len(X))**0.5
    return mean, std

# You are given this class
class Die(object):
    def __init__(self, valList):
        """ valList is not empty """
        self.possibleVals = valList[:]
    def roll(self):
        return random.choice(self.possibleVals)

# Implement this -- Coding Part 1 of 2
def makeHistogram(values, numBins, xLabel, yLabel, title=None):
    """
      - values, a sequence of numbers
      - numBins, a positive int
      - xLabel, yLabel, title, are strings
      - Produces a histogram of values with numBins bins and the indicated labels
        for the x and y axis
      - If title is provided by caller, puts that title on the figure and otherwise
        does not title the figure
    """
    pylab.hist(values, bins=numBins)
    pylab.xlabel(xLabel)
    pylab.ylabel(yLabel)
    if title is not None:
        pylab.title(title)
    pylab.show()



# Implement this -- Coding Part 2 of 2
def getAverage(die, numRolls, numTrials):
    """
      - die, a Die
      - numRolls, numTrials, are positive ints
      - Calculates the expected mean value of the longest run of a number
        over numTrials runs of numRolls rolls.
      - Calls makeHistogram to produce a histogram of the longest runs for all
        the trials. There should be 10 bins in the histogram
      - Choose appropriate labels for the x and y axes.
      - Returns the mean calculated
    """
    longest_runs = list()
    for trial in range(numTrials):
        roll_results= list()
        longest_run = 0
        longest_run_so_far = 0
        for roll in range(numRolls):
            result = die.roll()
            roll_results.append(result)
            if result == roll_results[roll-1]:
                longest_run += 1
            else:
                if longest_run > longest_run_so_far:
                    longest_run_so_far = longest_run
                longest_run = 1
        if longest_run > longest_run_so_far:
            longest_run_so_far = longest_run
        longest_runs.append(longest_run_so_far)
    makeHistogram(longest_runs, 10, "Longest Runs", "Trials")
    mean_and_stddev = getMeanAndStd(longest_runs)
    return mean_and_stddev[0]


# One test case
#print getAverage(Die([1,2,3,4,5,6,6,6,7]), 500, 10000)
#print getAverage(Die([1]), 10, 1000)
#print getAverage(Die([1,1]), 10, 1000)
#print getAverage(Die([1,2,3,4,5,6,6,6,7]), 1, 1000)
#print getAverage(Die([1,2,3,4,5,6]), 50, 1000)
print getAverage(Die([1,2,3,4,5,6,6,6,7]), 50, 1000)
