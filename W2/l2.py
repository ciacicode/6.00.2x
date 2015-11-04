__author__ = 'ciacicode'
import pdb

def stdDevOfLengths(L):
    """
    L: a list of strings

    returns: float, the standard deviation of the lengths of the strings,
      or NaN if L is empty.
    """
    if len(L) <1:
        return float('NaN')
    else:
        diff = 0
        N = float(len(L))
        summation = 0
        # find average length
        for item in L:
            summation += len(item)
        average = float(summation/N)

        # calculate standard deviation
        for item in L:
            diff += float((len(item)-average)**2)
        variance = diff/N
        sd = variance**0.5
        return sd




