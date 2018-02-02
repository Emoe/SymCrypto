import sys

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


print "Aufgabe 3:"
# Find a linear Characteristic for 3 rounds
rounds = 1
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


r = 1
for startSbox in range(0,16):
        for startVal in linApprox:
                biasOfRounds = []
                for firstVal in linApprox[startVal]:


                        
                        r += 1
                        if r >= 1:
                                getTotalBias(biasOfRounds)
                                break   

#biasOfRounds = []
#findLinearChar(biasOfRounds,1,0)        
#for r in range(1,rounds + 1):
#        for startSBox in range(0,16):
#                for startVal in linApprox:
#                        biasOfRounds = []
#                        findLinearChar(biasOfRounds,r,startVal)

print "Aufgabe 4:"
# Pilling up Lema


