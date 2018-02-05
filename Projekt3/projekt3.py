import random
import itertools

# Standard AES-SBOX
Sbox = [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5,
        0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76, 
        0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 
        0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0, 
        0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 
        0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15, 
        0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 
        0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75, 
        0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 
        0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84, 
        0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 
        0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf, 
        0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 
        0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8, 
        0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 
        0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2, 
        0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 
        0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73, 
        0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 
        0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb, 
        0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 
        0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79, 
        0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 
        0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08, 
        0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 
        0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a, 
        0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 
        0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e, 
        0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 
        0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf, 
        0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 
        0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]

# SBOX-Liste durchgehen und umdrehen
Sbox_inv = [Sbox.index(x) for x in xrange(256)]

# Arbeiten mit Arrays daher die RCon als Array ;-)
Rcon = [[0x01,0x00,0x00,0x00], [0x02,0x00,0x00,0x00], [0x04,0x00,0x00,0x00],
    [0x08,0x00,0x00,0x00], [0x10,0x00,0x00,0x00], [0x20,0x00,0x00,0x00], 
    [0x40,0x00,0x00,0x00], [0x80,0x00,0x00,0x00],[0x1B,0x00,0x00,0x00], 
    [0x36,0x00,0x00,0x00]]

 
def rowsToCols(state):
    cols = []
    
    #convert from row representation to column representation
    cols.append([state[0][0], state[1][0], state[2][0], state[3][0]])
    cols.append([state[0][1], state[1][1], state[2][1], state[3][1]])
    cols.append([state[0][2], state[1][2], state[2][2], state[3][2]])
    cols.append([state[0][3], state[1][3], state[2][3], state[3][3]])
    
    return cols

def colsToRows(state):
    rows = []

    #convert from column representation to row representation 
    rows.append([state[0][0], state[1][0], state[2][0], state[3][0]])
    rows.append([state[0][1], state[1][1], state[2][1], state[3][1]])
    rows.append([state[0][2], state[1][2], state[2][2], state[3][2]])
    rows.append([state[0][3], state[1][3], state[2][3], state[3][3]])

    return rows

# Standard Galoirfeld Multiplikation, von Github
def galoisMult(a, b):
    p = 0
    hiBitSet = 0
    for i in range(8):
        if b & 1 == 1:
            p ^= a
        hiBitSet = a & 0x80
        a <<= 1
        if hiBitSet == 0x80:
            a ^= 0x1b
        b >>= 1
    return p % 256

def AddRoundKey(tempVal,keyShedule,r):
    for i in range(len(tempVal)):
        for j in range(len(tempVal[i])):
            tempVal[i][j] = tempVal[i][j] ^ keyShedule[r * 4 + i][j]

    return tempVal

def mixColumnInv(column):
    temp = []
    for i in range(len(column)):
        temp.append(column[i])
    
    column[0] = galoisMult(temp[0],0xE) ^ galoisMult(temp[3],0x9) ^ galoisMult(temp[2],0xD) ^ galoisMult(temp[1],0xB)
    column[1] = galoisMult(temp[1],0xE) ^ galoisMult(temp[0],0x9) ^ galoisMult(temp[3],0xD) ^ galoisMult(temp[2],0xB)
    column[2] = galoisMult(temp[2],0xE) ^ galoisMult(temp[1],0x9) ^ galoisMult(temp[0],0xD) ^ galoisMult(temp[3],0xB)
    column[3] = galoisMult(temp[3],0xE) ^ galoisMult(temp[2],0x9) ^ galoisMult(temp[1],0xD) ^ galoisMult(temp[0],0xB)    
                
    return column

def InvMixColumns(cols):
    #cols = rowsToCols(state)
    
    r = [0,0,0,0]
    for i in range(len(cols)):
        r[i] = mixColumnInv(cols[i])
                    
         
    return r

def InvShiftrows(tempVal):
    tempVal = colsToRows(tempVal)

    #move 1
    tempVal[1].insert(0,tempVal[1].pop())
    
    #move 2
    tempVal[2].insert(0,tempVal[2].pop())
    tempVal[2].insert(0,tempVal[2].pop())
    
    #move 3
    tempVal[3].insert(0,tempVal[3].pop())
    tempVal[3].insert(0,tempVal[3].pop())
    tempVal[3].insert(0,tempVal[3].pop())
    
    return rowsToCols(tempVal)   

def InvSubBytes(state):
    state = [list(c) for c in state]
    for i in range(len(state)):
        row = state[i]
        for j in range(len(row)):
            state[i][j] = Sbox_inv[state[i][j]]
    return state


def mixColumn(column):
    temp = []
    for i in range(len(column)):
        temp.append(column[i])
    
    column[0] = galoisMult(temp[0],2) ^ galoisMult(temp[3],1) ^ galoisMult(temp[2],1) ^ galoisMult(temp[1],3)
    column[1] = galoisMult(temp[1],2) ^ galoisMult(temp[0],1) ^ galoisMult(temp[3],1) ^ galoisMult(temp[2],3)
    column[2] = galoisMult(temp[2],2) ^ galoisMult(temp[1],1) ^ galoisMult(temp[0],1) ^ galoisMult(temp[3],3)
    column[3] = galoisMult(temp[3],2) ^ galoisMult(temp[2],1) ^ galoisMult(temp[1],1) ^ galoisMult(temp[0],3)    
                
    return column

def MixColumns(cols):
    
    r = [0,0,0,0]
    for i in range(len(cols)):
        r[i] = mixColumn(cols[i])

    return r

def Shiftrows(state):
    state = colsToRows(state)

    #move 1
    state[1].append(state[1].pop(0))
    
    #move 2
    state[2].append(state[2].pop(0))
    state[2].append(state[2].pop(0))
    
    #move 3
    state[3].append(state[3].pop(0))
    state[3].append(state[3].pop(0))
    state[3].append(state[3].pop(0))

    return rowsToCols(state)   


def SubBytes(state):
    state = [list(c) for c in state]
    for i in range(len(state)):
        row = state[i]
        for j in range(len(row)):
            state[i][j] = Sbox[state[i][j]]
    return state

def SboxWord(word):
    return [Sbox[word[0]],Sbox[word[1]],Sbox[word[2]],Sbox[word[3]]]

def XorWords(word1, word2):
    temp = []
    for i in range(0,len(word1)):
        temp.append(word1[i] ^ word2[i])
    return temp

def RotWord(word):
    return [word[1],word[2],word[3],word[0]]

def keySheduling(key):
    expanded = []
    
    numberOfColumns = 4
    numberOf32BitWords = 4
    numberOfRounds = 4
    
    for i in range(0,numberOfColumns * (numberOf32BitWords + 1)):
        expanded.append([0,0,0,0])
    
    i = 0

    while i<numberOf32BitWords:
        expanded[i] = [key[4 * i],key[4 * i + 1], key[4 * i + 2], key[4 * i + 3]]
        i += 1
    
    i = numberOf32BitWords
    
    
    while i < (numberOfColumns * (numberOf32BitWords + 1)):
        temp = expanded[i-1]

        if (i % numberOf32BitWords) == 0:

            temp = XorWords(SboxWord(RotWord(temp)), Rcon[i / numberOf32BitWords - 1])

        expanded[i] = XorWords(expanded[i-numberOf32BitWords], temp)
        i +=1
    
    return expanded

def encrypt(plaintext,key):
    tempVal = []

    tempVal.append(plaintext[:4])
    tempVal.append(plaintext[4:8])
    tempVal.append(plaintext[8:12])
    tempVal.append(plaintext[12:16])
    
    keyShedule = keySheduling(key)

    tempVal = AddRoundKey(tempVal,keyShedule,0)
    for i in range(1,4): 
        tempVal = SubBytes(tempVal)
        tempVal = Shiftrows(tempVal)
        tempVal = MixColumns(tempVal)
        tempVal = AddRoundKey(tempVal,keyShedule,i)
        
    tempVal = SubBytes(tempVal)
    tempVal = Shiftrows(tempVal)
    tempVal = AddRoundKey(tempVal,keyShedule,4)

    ciphertext = []
    for i in range(len(tempVal)):
        for j in range(len(tempVal[i])):
            ciphertext.append(tempVal[i][j])

    return ciphertext

def decrypt(ciphertext,key):
    tempval = []

    tempval.append(ciphertext[:4])
    tempval.append(ciphertext[4:8])
    tempval.append(ciphertext[8:12])
    tempval.append(ciphertext[12:16])

    keyShedule = keySheduling(key)

    tempval = AddRoundKey(tempval,keyShedule,4)
    tempval = InvShiftrows(tempval)
    tempval = InvSubBytes(tempval)
    for i in reversed(range(1,4)):
        tempval = AddRoundKey(tempval,keyShedule,i)
        tempval = InvMixColumns(tempval)
        tempval = InvShiftrows(tempval)
        tempval = InvSubBytes(tempval)

    tempval = AddRoundKey(tempval,keyShedule,0)

    output = []
    for i in range(len(tempval)):
        for j in range(len(tempval[i])):
            output.append(tempval[i][j])

    return output

def generateKey():
    key = []
    for i in range(0,16):
        key.append(random.randrange(0,255,1))
    return key

def generatePlaintexts():
    plaintexts = []
    for i in range(0,256):
        temp = [0] * 16
        temp[0] = i
        plaintexts.append(temp)    
    return plaintexts

def encryptAllPlaintexts(plaintexts,key):
    ciphertexts = []

    for plaintext in plaintexts:
        ciphertexts.append(encrypt(plaintext,key))
    
    return ciphertexts

def integrate(index):
    potential = []
    for candidateByte in range(256):
        sum = 0
        for ciph in ciphertexts:
            oneRoundDecr = Sbox_inv[ciph[index] ^ candidateByte]     # All we need is a single xor for the guessed byte, and InvSubBytes
            sum ^= oneRoundDecr
        if sum == 0:
            potential.append(candidateByte)
    return potential


def integral():
    candidates = []
    for i in range(16):
        candidates.append(integrate(i))

    # try all Roundkeys by building the cartesic product of those (all with all)
    for roundKey in itertools.product(*candidates):
        # Calculate MasterKey from Roundkey
        masterKey = round2master(roundKey)
        # Decrypt one Ciphertext
        plain = decrypt(ciphertexts[1], masterKey)
        # check if key Matches
        if  plaintexts[1] == plain:
            print "Guessed Key: ", masterKey
            return masterKey

# Calculate the master key candidate from the final round key candidate
def round2master(rk):
    numberOfColumns = 4
    numberOf32BitWords = 4
    numberOfRounds = 4
    w = []

    for i in range(numberOfColumns * ( numberOfRounds + 1)):
        w.append([0,0,0,0])
        
    i=0
    while i < numberOf32BitWords:
        w[i] = [rk[4*i],rk[4*i+1], rk[4*i+2], rk[4*i+3]]
        
        #printWord(w[i])
        i = i+1

    j = numberOf32BitWords
    while j < numberOfColumns * (numberOfRounds + 1):
        if (j % numberOf32BitWords) == 0:
            w[j][0] = w[j - numberOf32BitWords][0] ^ Sbox[w[j-1][1] ^ w[j-2][1]] ^ Rcon[numberOfRounds - j/numberOf32BitWords][0]
            for i in range(1,4):
                w[j][i] = w[j - numberOf32BitWords][i] ^ Sbox[w[j-1][(i+1) % 4] ^ w[j-2][(i+1) % 4]]
        else:
            w[j] = XorWords(w[j - numberOf32BitWords], w[j - numberOf32BitWords - 1])
        j = j+1
    

    m = []
    for i in range(16,20):
        for j in range(4):
            m.append(w[i][j])
            

    return m

# Generate a Key
key = generateKey()
print "Real Key:    ", key
# Generate 256 choosen Plaintexts
plaintexts = generatePlaintexts()
# Encrypt all these Plaintexts with generated
ciphertexts = encryptAllPlaintexts(plaintexts,key)
# Attack :D
integral()