import sys
import random
import math


# Present S-Box
Sbox = [0xc, 0x5, 0x6, 0xb, 0x9, 0x0, 0xa, 0xd, 0x3, 0xe, 0xf, 0x8, 0x4, 0x7, 0x1, 0x2]
Sbox_inv = [Sbox.index(x) for x in xrange(16)]

# Present Bit-Permutation
PBox = [0, 16, 32, 48, 1, 17, 33, 49, 2, 18, 34, 50, 3, 19, 35, 51,
        4, 20, 36, 52, 5, 21, 37, 53, 6, 22, 38, 54, 7, 23, 39, 55,
        8, 24, 40, 56, 9, 25, 41, 57, 10, 26, 42, 58, 11, 27, 43, 59,
        12, 28, 44, 60, 13, 29, 45, 61, 14, 30, 46, 62, 15, 31, 47, 63]
PBox_inv = [PBox.index(x) for x in xrange(64)]

# check if Bit is set
def testBit(x, pos):
        return (x >> (pos)) & 1


# Berechne volle Linear Approximation Table
print "Aufgabe 1:"
print "Calculate linear approximation table:"
print ("     0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F")
for inputMask in range(0,16):
        sys.stdout.write("%2d: " % inputMask)
        for outputMask in range(0,16):
                #sys.stdout.write(str(outputMask) + ", ")
                Counter = 0
                for inputSbox in range(0,16):
                        outputSbox = Sbox[inputSbox]                
                        if (testBit(inputMask,0) * testBit(inputSbox,0) ^ testBit(inputMask,1) * testBit(inputSbox,1) ^ testBit(inputMask,2) * testBit(inputSbox,2) ^ testBit(inputMask,3) * testBit(inputSbox,3) == testBit(outputMask,0) * testBit(outputSbox,0) ^ testBit(outputMask,1) * testBit(outputSbox,1) ^ testBit(outputMask,2) * testBit(outputSbox,2) ^ testBit(outputMask,3) * testBit(outputSbox,3)):
                                Counter += 1
                bias = int(float((float(Counter)/16)-0.5)*16)
                sys.stdout.write("%2d " % bias)
        print ""

print "\n"

print "Aufgabe 2:"
print "Calculate linear approximation table with one bit input and output:"
print ("     1  2  4  8")
for inputMask in [1,2,4,8]:
        sys.stdout.write("%2d: " % inputMask)
        for outputMask in [1,2,4,8]:
                #sys.stdout.write(str(outputMask) + ", ")
                Counter = 0
                for inputSbox in range(0,16):
                        outputSbox = Sbox[inputSbox]                
                        if (testBit(inputMask,0) * testBit(inputSbox,0) ^ testBit(inputMask,1) * testBit(inputSbox,1) ^ testBit(inputMask,2) * testBit(inputSbox,2) ^ testBit(inputMask,3) * testBit(inputSbox,3) == testBit(outputMask,0) * testBit(outputSbox,0) ^ testBit(outputMask,1) * testBit(outputSbox,1) ^ testBit(outputMask,2) * testBit(outputSbox,2) ^ testBit(outputMask,3) * testBit(outputSbox,3)):
                                Counter += 1
                bias = int(float((float(Counter)/16)-0.5)*16)
                sys.stdout.write("%2d " % bias)
        print ""


def getTotalBias(biasOfRounds):
        totalBias = biasOfRounds[0] / 16.0
        for bias in biasOfRounds[1:]:
                totalBias = totalBias * (bias/16.0)
        totalBias = pow(2,len(biasOfRounds) -1) * totalBias
        print "Total Bias for "+ str(len(biasOfRounds)) +" rounds: " + str(totalBias)

print ""
print "Aufgabe 3 und 4:"
# Find a linear Characteristic for 3 rounds

linApprox = {2:[[2,2],[4,2],[8,2]],4:[[2,2],[4,2],[8,2]],8:[[2,2],[8,2]]}

def findLinearChar(biasOfRounds,currentRounds,currentVal,currentSbox):
        if currentRounds >= rounds:
                return
        inputPbox = currentSbox * 4 + (currentVal[0] -1)
        outputPbox = PBox[inputPbox]
        nextSbox = outputPbox / 4
        nextinputMask = outputPbox % 4 
        print "S-Box("+str(currentRounds)+","+str(currentSbox)+"): "+str(currentVal[0]) + " --> " + str()
        biasOfRounds.append(currentVal[1])

        for nextval in linApprox[currentVal]:
                findLinearChar(biasOfRounds,currentRounds,nextval,nextSbox)

maxRounds = 10
for startSbox in range(0,16):
        startVal = random.choice([2,4,8])
        biasOfRounds = []
        nextVal = random.choice(linApprox[startVal])
        print "S-Box("+str(0)+","+str(startSbox)+"): "+str(startVal) + " --> " + str(nextVal[0])
        biasOfRounds.append(nextVal[1]) 
        for r in range(1,maxRounds):
                temp = {1:1,2:2,4:3,8:4}
                temp2 = {1:1,2:2,3:4,4:8}              
                inputPbox = (startSbox * 4) - 1 + temp[nextVal[0]] 
                outputPbox = PBox[inputPbox]
                startSbox = outputPbox / 4
                if outputPbox % 5 == 1 or outputPbox % 5 == 0:
                        break
                nextinputMask = temp2[outputPbox % 5] 
                nextVal = random.choice(linApprox[nextinputMask])
                biasOfRounds.append(nextVal[1])
                print "S-Box("+str(r)+","+str(startSbox)+"): "+str(nextinputMask) + " --> " + str(nextVal[0])                
        getTotalBias(biasOfRounds)
        print ""

print "Aufgabe 1.6"

def travelCipher(r,startSbox,startmask,finOutputMask,finSboxOut):
        global numberOfLinearChars
        for nextmask in [1,2,4,8]:

                inputPbox = int((startSbox * 4) + math.log(nextmask,2))
                outputPbox = PBox[inputPbox]
                startSbox = outputPbox / 4
                nextmask = int(math.pow(2, outputPbox % 5))
                if r == MaxHullRounds -1:
                        if nextmask == finOutputMask and startSbox == finSboxOut:
                                numberOfLinearChars += 1
                else:
                        travelCipher(r + 1,startSbox,nextmask,finOutputMask,finSboxOut)
        return 0
                

MaxHullRounds = 4
for sBoxIn in range(0,16):
        for SboxOut in range(0,16):
                for inputMask in [1,2,4,8]:
                        for outputMask in [1,2,4,8]:
                                numberOfLinearChars = 0
                                travelCipher(0,sBoxIn,inputMask,outputMask,SboxOut)
                                print "Number of Linear Characteristic for the linear hull (" + str(inputMask) + "," + str(outputMask) + ") started in Sbox " + str(sBoxIn) +  " and ended in Sbox " + str(SboxOut) + " :" + str(numberOfLinearChars)
print ""
print "Aufgabe 1.7"        
for key in range(0,16):
        print "Calculate linear approximation table with key "+ str(hex(key)) + " :"
        print ("     0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F")
        for inputMask in range(0,16):
                sys.stdout.write("%2d: " % inputMask)
                for outputMask in range(0,16):
                        #sys.stdout.write(str(outputMask) + ", ")
                        Counter = 0
                        for inputSbox in range(0,16):
                                outputSbox = Sbox[inputSbox ^ key]                
                                if (testBit(inputMask,0) * testBit(inputSbox,0) ^ testBit(inputMask,1) * testBit(inputSbox,1) ^ testBit(inputMask,2) * testBit(inputSbox,2) ^ testBit(inputMask,3) * testBit(inputSbox,3) == testBit(outputMask,0) * testBit(outputSbox,0) ^ testBit(outputMask,1) * testBit(outputSbox,1) ^ testBit(outputMask,2) * testBit(outputSbox,2) ^ testBit(outputMask,3) * testBit(outputSbox,3)):
                                        Counter += 1
                        bias = int(float((float(Counter)/16)-0.5)*16)
                        sys.stdout.write("%2d " % bias)
                print ""
        print ""                

