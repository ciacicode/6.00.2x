# 6.00.2x Problem Set 4

import numpy
import random
import pylab
from W3.ps3b import *

#
# PROBLEM 1
#        
def simulationDelayedTreatment(numTrials):
    """
    Runs simulations and make histograms for problem 1.

    Runs numTrials simulations to show the relationship between delayed
    treatment and patient outcome using a histogram.

    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).

    numTrials: number of simulation runs to execute (an integer)
    """
    
    three_hundred_tuple =  simulationWithDrug(numTrials, 300 )
    hundred_fifty_tuple = simulationWithDrug(numTrials, 150 )
    seventy_five_tuple = simulationWithDrug(numTrials, 75 )
    zero_tuple = simulationWithDrug(numTrials, 0 )

    three_h = zip(*three_hundred_tuple)[1]
    hun_fifty = zip(*hundred_fifty_tuple)[1]
    sev_five = zip(*seventy_five_tuple)[1]
    zer = zip(*zero_tuple)[1]

    pylab.subplot(4,1,1)
    pylab.hist(three_h, bins=20)
    pylab.title("300 delayed steps")

    pylab.subplot(4,1,2)
    pylab.hist(hun_fifty, bins=20)
    pylab.title("150 delayed steps")

    pylab.subplot(4,1,3)
    pylab.hist(sev_five, bins=20)
    pylab.title("75 delayed steps")

    pylab.subplot(4,1,4)
    pylab.hist(zer, bins=20)
    pylab.title("0 delayed steps")
    pylab.show()






#
# PROBLEM 2
#
def simulationTwoDrugsDelayedTreatment(numTrials):
    """
    Runs simulations and make histograms for problem 2.

    Runs numTrials simulations to show the relationship between administration
    of multiple drugs and patient outcome.

    Histograms of final total virus populations are displayed for lag times of
    300, 150, 75, 0 timesteps between adding drugs (followed by an additional
    150 timesteps of simulation).

    numTrials: number of simulation runs to execute (an integer)
    """
    # TODO
