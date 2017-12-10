
import random
from collections import Counter



SBox = {0x0:0x6, 0x1:0x4, 0x2:0xc, 0x3:0x5, 0x4:0x0, 0x5:0x7, 0x6:0x2, 0x7:0xe, 0x8:0x1, 0x9:0xf, 0xa:0x3, 0xb:0xd, 0xc:0x8, 0xd:0xa, 0xe:0x9, 0xf:0xb}
SBoxInverted = dict([[v,k] for k,v in SBox.items()])
DistributionTable = {'u0':[],'u1':[],'v0':[],'v1':[],'diff_v':[]}
Cipherkey = [0x0,0x1,0x2]
message = 0xb
K1Kanidates = []
K2Kanidates = []

def getSBoxValue(input):
    return SBox[input]

def getInverseSBoxValue(input):
    return SBoxInverted[input]

# Calculate Distribution Table
def calculateDistributionTable():
    global DistributionTable
    for u0 in range(0,16):
        u1 = u0 ^ 0xf # u1 = u0 xor 0xf
        v0 = getSBoxValue(u0) # v0 = SBox(u0)
        v1 = getSBoxValue(u1) # v1 = SBox(u1)
        diff_v = v0 ^ v1 # v0 xor v1
        DistributionTable['u0'].append(u0)
        DistributionTable['u1'].append(u1)
        DistributionTable['v0'].append(v0)
        DistributionTable['v1'].append(v1)
        DistributionTable['diff_v'].append(diff_v)

def encrypt(message):
    global Cipherkey

    u = message ^ Cipherkey[0] 
    print "Intermediate Value U: " + str(u)
    v = getSBoxValue(u)
    print "Intermediate Value V: " + str(v)
    w = v ^ Cipherkey[1]
    print "Intermediate Value W: " + str(w)
    x = getSBoxValue(w)
    print "Intermediate Value X: " + str(x)
    ciphertext = x ^ Cipherkey[2] 
    return ciphertext

def getRandomValue():
    return random.randint(0,15)

def initCipher():
    global Cipherkey
    k0 = getRandomValue()
    k1 = getRandomValue()
    k2 = getRandomValue()
    Cipherkey[0] = k0
    Cipherkey[1] = k1
    Cipherkey[2] = k2
    print "K0: " + hex(k0)
    print "K1: " + hex(k1)
    print "K2: " + hex(k2)

def initAttack():
    # Generate two messages and Ciphertext Pairs
    m1 = 0
    m2 = 0
    while (m1 ^ m2) != 0xf:
        m1 = getRandomValue()        
        m2 = getRandomValue()
    
    print "m1: " + hex(m1)
    c1 = encrypt(m1)
    print "c1: " + hex(c1)

    print "m2: " + hex(m2)
    c2 = encrypt(m2)
    print "c2: " + hex(c2)
    
    return {m1:c1,m2:c2}

#  Todo Change from here
def Attack(MessageCipherPairs):
    global K1Kanidates
    global K2Kanidates
    global DistributionTable

    m1 = MessageCipherPairs.keys()[0]
    m2 = MessageCipherPairs.keys()[1]
    c1 = MessageCipherPairs[m1]
    c2 = MessageCipherPairs[m2]
    # u0 xor u1 = (m0 xor k0) xor (m1 xor k0) = m0 xor m1
    diff_m = m1 ^ m2
    diff_u = diff_m

    highestDifferenzofV = Counter(DistributionTable['diff_v'])
    print "List of highest Differences for v0 and v1:"
    print highestDifferenzofV
    diff_v = 0
    occurence_V =0
    for item in highestDifferenzofV:
        if highestDifferenzofV[item] > occurence_V:
            diff_v = item
            occurence_V = highestDifferenzofV[item]
    print "Assumption for difference of " + hex(diff_v) + " has a probalitiy of " + str(highestDifferenzofV[diff_v]) + "/16\n"  

    # Guess k1 
    for guessed_k2 in range(0,15):
        #print "Key Guess: " + str(guessed_k1)
        
        # calculate v1' and v2'
        x1Tick = c1 ^ guessed_k2 # v1' = c1 xor k2
        x2Tick = c2 ^ guessed_k2 # v2' = c2 cor k2
 
        w1Tick = getInverseSBoxValue(x1Tick)
        w2Tick = getInverseSBoxValue(x2Tick)
        diff_w = w1Tick ^ w2Tick
        diff_vTick = diff_w

        if diff_v == diff_vTick:
            K2Kanidates.append(guessed_k2)


    print "All Kanidates for k2:"
    for key in K2Kanidates:
        print "Kanidate: " + hex(key)
    print "Probability that key is right is " + str(highestDifferenzofV[diff_v]) + "/16\n"
   
calculateDistributionTable()
print "Init the Cipher"
initCipher()
print "\nChoose random Messages and decrypt them"
MessageCipherPairs = initAttack()
print "\nBeginn Attack on k1:"
Attack(MessageCipherPairs)