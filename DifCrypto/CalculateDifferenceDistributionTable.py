import sys
# S-Box of Cipher
SBox = [0xE,0x4,0xD,0x1,0x2,0xF,0xB,0x8,0x3,0xA,0x6,0xC,0x5,0x9,0x0,0x7]


DifferenceDistTable = [[0 for x in range(16)] for y in range(16)] 


# Berechne Difference Distribution Table
for x0 in range(0,16):
    for x1 in range(0,16):
        inputDiff = x0 ^ x1
        outputDiff = SBox[x0] ^ SBox[x1]
        DifferenceDistTable[outputDiff][inputDiff] += 1

# Gebe Difference Distribution Table aus
sys.stdout.write("   ")
for z in range(0,16):
    sys.stdout.write(str(z)+" ")
sys.stdout.write("\n")

for i in range(0,16):
    sys.stdout.write(str(i)+": ")
    for j in range(0,16):
        sys.stdout.write(str(DifferenceDistTable[j][i])+" ")
    sys.stdout.write("\n")


# Finde Maximum
# delta y, delta x, number of times
maximum = [0,0,0]
for i in range(0,16):
    for j in range(0,16):
        if DifferenceDistTable[j][i] >= maximum[2] and i != 0 and j !=0:
            maximum[0] = i
            maximum[1] = j
            maximum[2] = DifferenceDistTable[j][i]

# Gebe Maximum aus
print ""
print "Maximum"
print "Delta X: " + str(hex(maximum[0]))
print "Delta Y: " + str(hex(maximum[1]))
print "Auftreten: " + str(maximum[2])
print "Warscheinlichkeit: " + str(maximum[2]) +"/16"            
