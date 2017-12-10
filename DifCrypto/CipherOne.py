
import random

SBox = {0x0:0x6, 0x1:0x4, 0x2:0xc, 0x3:0x5, 0x4:0x0, 0x5:0x7, 0x6:0x2, 0x7:0xe, 0x8:0x1, 0x9:0xf, 0xa:0x3, 0xb:0xd, 0xc:0x8, 0xd:0xa, 0xe:0x9, 0xf:0xb}
SBoxInverted = dict([[v,k] for k,v in SBox.items()])
Cipherkey = [0x0,0x1]
message = 0xb
K1Kanidates = []

def getSBoxValue(input):
    return SBox[input]

def getInverseSBoxValue(input):
    return SBoxInverted[input]

def encrypt(message):
    global Cipherkey
    u = message ^ Cipherkey[0] 
    #print "Intermediate Value U: " + str(u)
    v = getSBoxValue(u)
    #print "Intermediate Value V: " + str(v)
    ciphertext = v ^ Cipherkey[1] 
    return ciphertext

def getRandomValue():
    return random.randint(0,15)

def initCipher():
    global Cipherkey
    k1 = getRandomValue()
    k2 = getRandomValue()
    Cipherkey[0] = k1
    Cipherkey[1] = k2
    print "K0: " + hex(k1)
    print "K1: " + hex(k2)

def initAttack():
    # Generate two messages and Ciphertext Pairs
    m1 = getRandomValue()
    print "m1: " + hex(m1)
    m2 = getRandomValue()
    print "m2: " + hex(m2)
    if m1 == m2:
        m2 = getRandomValue()
    c1 = encrypt(m1)
    print "c1: " + hex(c1)
    c2 = encrypt(m2)
    print "c2: " + hex(c2)
    return {m1:c1,m2:c2}

def Attack(MessageCipherPairs):
    global K1Kanidates

    m1 = MessageCipherPairs.keys()[0]
    m2 = MessageCipherPairs.keys()[1]
    c1 = MessageCipherPairs[m1]
    c2 = MessageCipherPairs[m2]
    # u0 xor u1 = (m0 xor k0) xor (m1 xor k0) = m0 xor m1
    diff_m = m1 ^ m2
    diff_u = diff_m

    # Guess k1 
    for guessed_k1 in range(0,16):
        #print "Key Guess: " + str(guessed_k1)
        
        # calculate v1' and v2'
        v1Tick = c1 ^ guessed_k1 # v1' = c1 xor k1
        v2Tick = c2 ^ guessed_k1 # v2' = c2 cor k1
    
        u1Tick = getInverseSBoxValue(v1Tick)
        u2Tick = getInverseSBoxValue(v2Tick)
        
        if diff_u == (u1Tick ^ u2Tick):
            K1Kanidates.append(guessed_k1)

    print "All Kanidates for k1:"
    for key in K1Kanidates:
        print "Kanidate: " + hex(key)

print "Init the Cipher"
initCipher()
print "\nChoose random Messages and decrypt them"
MessageCipherPairs = initAttack()
print "\nBeginn Attack on k1:"
Attack(MessageCipherPairs)