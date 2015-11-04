__author__ = 'ciacicode'
import string
import pdb
import pylab

PATH_TO_FILE = '/home/maria/Desktop/ciacicode/6.00.2x/W1/julyTemps.txt'

def load_temperatures():
    try:
        inFile = open(PATH_TO_FILE, 'r', 0)
    except IOError: "Could not find file " + PATH_TO_FILE
    highs = list()
    lows = list()
    for line in inFile:
        #split the line
        fields = line.split()
        if len(fields) != 3 or 'Boston' == fields[0] or 'Day' == fields[0]:
            # detect things that are not valid values
            pass
        else:
            highs.append(int(fields[1]))
            lows.append(int(fields[2]))

    return highs, lows


def diff_temps(tempTuple):
    highs = tempTuple[0]
    lows = tempTuple[1]
    diff_list = list()
    for h, l in zip(highs, lows):
        diff = h - l
        diff_list.append(diff)
    return diff_list


def create_plot():
    temperatures = load_temperatures()
    differences = diff_temps(temperatures)
    pylab.plot(range(1,32), differences)
    pylab.title("Day by Day Ranges in Temperature in Boston in July 2012")
    pylab.ylabel("Temperature Ranges")
    pylab.xlabel("Days")
    pylab.show()