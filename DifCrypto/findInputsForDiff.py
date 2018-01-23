import sys
# Aufruf: pythone findInputsForDiff.py 11

inputDifference = int(sys.argv[1])
print "Input Difference: " + str(hex(inputDifference)) + "\n"
possibleInputPairs = []


for x0 in range (0,16):
    for x1 in range(0,16):
        if (x0 ^ x1) == inputDifference:
            possibleInputPairs.append([x0,x1])

for element in possibleInputPairs:
    print "Input 1: " + str(hex(element[0])) + " Input 2: " + str(hex(element[1])) + " Difference of Inputs: " + str(hex(element[0] ^ element[1]))  
