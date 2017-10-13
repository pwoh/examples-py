import time
import subprocess
import sys
import os
from timeit import timeit
from subprocess import check_call, STDOUT
import csv
from time import gmtime, strftime
import json


def getAvgMs(start, repeat):
    return int(round(1000*(time.time() - start)/repeat))

def timeAvg(repeat, callArgs):
    start = time.time()
    for _ in range(0, repeat):
        try:
            check_call(callArgs, stdout=DEVNULL, stderr=STDOUT)
        except subprocess.CalledProcessError as err:
            print "Error running " + str(callArgs) + ", error: " + str(err)
            return -1
    return getAvgMs(start, repeat)

# Command line arguments
# Usage: python timer.py [vector or matrix size]
#                        [size increment]
#                        [JSON: {"columns": [...], "python": [{"filename":..., "maxDim":..., "args":[...]}...], "exe": [...]}] 
#                        [times to run]
#                        [output filename] 
dim = int(sys.argv[1])
incr = int(sys.argv[2])
toRun = json.loads(sys.argv[3])
repeat = int(sys.argv[4])
filename = sys.argv[5]

cols = toRun['columns']
toRunPy = toRun['python']
toRunStack = toRun['stack']

DEVNULL = open(os.devnull, 'wb', 0)

with open(filename + strftime("%Y-%m-%d-%H:%M:%S", gmtime()) + '.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='\'', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(cols)
    for d in xrange(1, dim+1, incr):
        if d == 0:
            continue
        resultrow = [d]
        for pyItem in toRunPy:
            curRes = " "
            maxDim = pyItem['maxDim']
            if (d <= maxDim):
                curRes = timeAvg(repeat, ['python', pyItem['filename'], str(d), '1'] + pyItem['args'])
            resultrow.append(curRes)
        for stackItem in toRunStack:
            curRes = " "
            maxDim = stackItem['maxDim']
            if (d <= maxDim):
                curRes = timeAvg(repeat, ['stack', 'exec', '--stack-yaml', stackItem['yaml'], stackItem['filename'], str(d), '1'] + stackItem['args'])
            resultrow.append(curRes)
        writer.writerow(resultrow)
