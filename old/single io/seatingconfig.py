import math
import random

f = open("input/sectionC.txt", "r", encoding="utf-8")
g = open("input/sectionC.txt", "r", encoding="utf-8")
h = open("input/sectionC.txt", "r", encoding="utf-8")

"""
m = length of seating area
n = width of seating area
"""
m = len(f.readline())-1
n = len(g.readlines())

numberOfSBlocks = 0

"""
Builds a table representation of the input file wherein
each entry to the list is another list that represents
each row of seating. Said table can be accessed by
table[y][x]
"""
seatingTable = []
for line in h.readlines():
    seatingTable.append(list(line.strip()))

"""
Replaces the string "0" in the table representation
to integer 0s
"""
for entry in seatingTable:
    for digit in entry:
        entry.remove("0")
        entry.append(0)

"""
Args:
    x (int): the x starting coordinate of the seating block
    y (int): the y starting coordinate of the seating block
    s (int): the size of the seating block

Returns:
    A list of all the individual seats that must be filled
    to satisfy this seating block
"""
def seatsToFill(x,y,s):
    ret = []
    p = divisors(s)
    dimensions = [[p,int(s/p)] for p in p] # creates a list of pairs of possible p/q values
    for dim in dimensions:
        possibility = []
        for xi in range(x, x+dim[0]):
            for yi in range(y, y+dim[1]):
                possibility.append([xi, yi])
        ret.append(possibility) # creates a list of lists where each inner list is all the seats that would need to be filled to accomodate that size/shape block
    return ret

"""
Args:
    n (int): number to calculate divisors

Returns:
    A list of all the divisors of n, except 1
    (to prevent entirely vertical blocks)
"""
def divisors(n):
    ret = []
    for i in range(1, int(n/2)+1):
        if n % i == 0:
            ret.append(i)
    ret.append(n) # adds n as a divisor to allow for horizontal line seating
    ret.remove(1) # removes 1 as a divisor to prevent vertical line seating
    return ret

"""
Args:
    x (int): the seat's x coordinate
    y (int): the seat's y coordinate
    seatingArea (list): the table storing seating
    arrangements

Returns:
    A modified table with the seat at (x,y) now
    marked as filled
"""
def markSeatFilled(x,y,seatingArea):
    seatingArea[y][x] = 1
    return seatingArea

"""
Args:
    x (int): the x starting coordinate of the seating block
    y (int): the y starting coordinate of the seating block
    xBuffer (int): the number of seats to block
    within a row to ensure proper distancing
    yBuffer (int): the number of seats to block
    across rows to ensure proper distancing
    diagonalBuffer (int): the number of seats
    diagonal from the filled seat to block to
    ensure proper distancing
    s (int): the size of the seating block
    seatingArea (list): the table storing seating
    arrangements

Returns:
    A modified table with all seats starting at (x,y) and
    within the block filled if and only if it's okay for them
    to be filled. This seating area is filled randomly and
    serves as a possibility for pickBestArrangement to choose from
"""
def fillSeats(x,y,xBuffer,yBuffer,diagonalBuffer,s,seatingArea):
    counter = 0
    possibilities = seatsToFill(x,y,s) # remember, for each seating block that could be filled, possibilities contains a list of the seats within that seating block that would need to be filled
    feasiblePossibilities = possibilities[:] # will store all seating arrangements in possibilities that are comprised of only seats that can be filled
    for possibility in possibilities:
        for seat in possibility:
            if seat[0] >= m or seat[0] < 0 or seat[1] >= n or seat[1] < 0 or not(seatOkay(seat[0], seat[1], xBuffer, yBuffer, diagonalBuffer, seatingArea)): # essentially, if these seats are not safe to fill either b/c they don't exist within the grid or they are too close to another seat
                feasiblePossibilities.remove(possibility)
                break
    if len(feasiblePossibilities) > 0: # if a block can be placed in the seatingArea
        selection = random.choice(feasiblePossibilities) # current algorithm relies on a random choice of which arrangement to pick
        for seat in selection: # fill each seat in the arrangement
            counter += 1
            xCoordSeat = seat[0]
            yCoordSeat = seat[1]
            markSeatFilled(xCoordSeat,yCoordSeat,seatingArea)
        return (seatingArea, counter)
    else:
        return (seatingArea, counter)

"""
Args:
    x (int): the x coordinate of the filled seat
    y (int): the y coordinate of the filled seat
    xBuffer (int): the number of seats to block
    within a row to ensure proper distancing
    yBuffer (int): the number of seats to block
    across rows to ensure proper distancing
    diagonalBuffer (int): the number of seats
    diagonal from the filled seat to block to
    ensure proper distancing

Returns:
    A list of seats that must remain blocked to
    provide proper distancing between the seat
    at [x,y] and other seats
"""
def blockedSeats(x,y,xBuffer,yBuffer,diagonalBuffer):
    bufferSeats = [] # a list that will store the seats that cannot be filled to account for a buffer around the seat at [x,y]
    for xi in range(x-xBuffer,x+xBuffer+1):
        if x != xi:
            bufferSeats.append([xi,y]) # append all seats too close in the x plane
    for yi in range(y-yBuffer,y+yBuffer+1):
        if y != yi:
            bufferSeats.append([x,yi]) # append all seats too close in the y plane
    for di in range(-diagonalBuffer,diagonalBuffer+1):
        if di != 0:
            bufferSeats.append([x-di,y+di])
            bufferSeats.append([di+x,di+y]) # append all seats too close diagonally
    return bufferSeats

"""
Args:
    x (int): the x coordinate of the seat to check
    y (int): the y coordinate of the seat to check
    xBuffer (int): the number of seats to block
    within a row to ensure proper distancing
    yBuffer (int): the number of seats to block
    across rows to ensure proper distancing
    diagonalBuffer (int): the number of seats
    diagonal from the filled seat to block to
    ensure proper distancing
    seatingArea (list): the table storing seating
    arrangements

Returns:
    A boolean value representing whether it is safe
    to sell the ticket at (x,y) given a safety buffer
    specified by xBuffer, yBuffer, and diagonalBuffer
    and calculated by the blockedSeats function
"""
def seatOkay(x,y,xBuffer,yBuffer,diagonalBuffer,seatingArea):
    seatsToCheck = blockedSeats(x,y,xBuffer,yBuffer,diagonalBuffer) # blockedSeats returns a list of seats that cannot be filled to ensure spacing
    for seat in seatsToCheck:
        seatXCoord = seat[0]
        seatYCoord = seat[1]
        if seatXCoord < 0 or seatXCoord >= m:
            continue # this seat is out of the grid so it is okay to not account it as buffer
        elif seatYCoord < 0 or seatYCoord >= n:
            continue # this seat is out of the grid so it is okay to not account it as buffer
        elif seatingArea[seatYCoord][seatXCoord] == 1:
            return False # one of our seats we would need to block to fill [x,y] is filled, therefore, [x,y] cannot be filled
    return True # since we have gone through all of our seats that would need to be blocked off and none are already filled, [x,y] can be filled


"""
Args:
    m (int): the length of the rectangle
    n (int): the width of the rectangle
    xBuffer (int): the number of seats to block
    within a row to ensure proper distancing
    yBuffer (int): the number of seats to block
    across rows to ensure proper distancing
    diagonalBuffer (int): the number of seats
    diagonal from the filled seat to block to
    ensure proper distancing
    s (int): the size of the seating block
    seatingArea (list): the table storing seating
    arrangements

Returns:
    A new table filled with the most blocks of size
    s possible given the shape returned by fillSeats
    (since the algorithm is currently brute force, 
    this is usually not the optimal shape)
"""
def fillRectangle(m,n,xBuffer,yBuffer,diagonalBuffer,s,seatingArea,squeeze):
    sizeTrackDict = {} # dictionary to keep track of the number of blocks of each size in seatingArea
    counter = 0 
    fillS = True # bool to indicate whether we will be adding a block of size s or another size each time
    otherSeatingBlockSizes = [1,2,4,8] # other sizes to use when fillS == False
    xj = 0
    yj = 0
    if m*n < math.sqrt(s):
        return sizeTrackDict # if the seating grid is too small to hold a single block of size s, don't do anything
    while yj < n:
        while xj < m:
            if fillS: # if we're filling a block of size s
                seatingTuple = fillSeats(xj,yj,xBuffer,yBuffer,diagonalBuffer,s,seatingArea)
                if s not in sizeTrackDict.keys():
                    sizeTrackDict[s] = 0
                sizeTrackDict[s] += seatingTuple[1]
                seatingArea = seatingTuple[0]
            else: # if we're not filling a block of size s
                blockSize = random.choice(otherSeatingBlockSizes) # choose randomly from provided sizes
                seatingTuple = fillSeats(xj,yj,xBuffer,yBuffer,diagonalBuffer,blockSize,seatingArea)
                if blockSize not in sizeTrackDict.keys(): # if the dictionary keeping track of size hasn't seen a block of this size before
                    sizeTrackDict[blockSize] = 0 # initialize in dictionary with value 0
                sizeTrackDict[blockSize] += seatingTuple[1] # add number of seats filled of that block size
                seatingArea = seatingTuple[0]
            if not(squeeze): # if we're squeezing in blocks at the end, we only want it to fill blocks of size s
                fillS = bool(random.getrandbits(1)) # quicker way of implementing random than choice
            xj += 1 # move to next seat
        yj += 1 # move to next row
        xj = 0 # move to first seat in new row
    return sizeTrackDict

"""
Args:
    m (int): the length of the rectangle
    n (int): the width of the rectangle
    xBuffer (int): the number of seats to block
    within a row to ensure proper distancing
    yBuffer (int): the number of seats to block
    across rows to ensure proper distancing
    diagonalBuffer (int): the number of seats
    diagonal from the filled seat to block to
    ensure proper distancing
    s (int): the size of the seating block
    seatingArea (list): the table storing seating
    arrangements
    reps (int): the number of times to try filling
    the seating area; as reps increases, so should
    the number of seats filled in the seatingArea
    returned, to a point: the optimal solution

Returns:
    A list of seatingArea choices which are immmediately
    passed into pickBestArrangements to choose the one
    that allows for the sale of the most seats
"""
def automateWhile(m,n,xBuffer,yBuffer,diagonalBuffer,s,seatingArea,reps):
    choices = []
    while reps > 0:
        resetMap(seatingArea) # resets the seating Table by settting every seat back to 0
        sizeTrackDict = fillRectangle(m,n,xBuffer,yBuffer,diagonalBuffer,s,seatingArea,False)
        seating2 = copyList(seatingArea.copy()) # performs a deep copy of seatingArea
        choices.append((seating2,sizeTrackDict)) # append choices list with tuple containing the filled seatingArea at index 0 and the dictionary keeping track of block sizes at index 1
        reps -= 1
    return choices

"""
Args:
    seatingArea (list): the table storing seating
    arrangements

Returns:
    A deep copy of seatingArea, created due to the
    inability of native Python to create deep copies
    of lists that are within lists - ugh!
"""
def copyList(seatingArea):
    ret = []
    pointer = []
    for row in seatingArea:
        ret.append([])
        pointer = ret[-1]
        for i in range(len(row)):
            pointer.append(row[i])
    return ret

"""
Args:
    seatingArea (list): the table storing seating
    arrangements

Returns:
    A cleared copy of seatingArea (all seats set
    to 0)
"""
def resetMap(seatingArea):
    for row in seatingArea:
        for i in range(len(row)):
            row[i] = 0 # seat each seat to 0 (empty)
    return seatingArea

"""
Args:
    degreeFilled (int): numSeats/maxNumSeats
    weightDegreeFilled (int): (0-1) the weight
    that degreeFilled will hold in the goodness score
    proportionNotS (int): 

Returns:
    A cleared copy of seatingArea (all seats set
    to 0)
"""
def goodnessFunction(degreeFilled, weightDegreeFilled, proportionNotS):
    weightPropNotS = 1 - weightDegreeFilled # to ensure two proportions sum to 1
    return (degreeFilled * weightDegreeFilled) + (proportionNotS * weightPropNotS)

"""
Args:
    s (int): the size of the seating block
    seatingList (list): a list of randomly generated
    seating tables

Returns:
    A tuple with the first element being the seating
    table with the maximum number of seats filled in
    seatingList and the second being the number of
    blocks of size s filled (saves computation time
    over calculating this later)
"""
def pickBestArrangement(s, seatingList):
    maxList = []
    for i in range(len(seatingList)):
        arrangementTuple = seatingList[i]
        arrangement = arrangementTuple[0]
        keepTrackDict = arrangementTuple[1]
        total = 0
        for key in keepTrackDict:
            total += keepTrackDict[key] # calculating total number of seats filled
        maxList.append([total,i]) # keep track of number of seats in index 0 and index in seatingList in index 1
    maxSeats = max(maxList, key = lambda x : x[0])[0] # find max number of seats found
    for i in range(len(maxList)): # go through all seating arrangements
        seatingDistributionDict = seatingList[i][1] # dictionary storing number of each block size
        proportionNotS = propNotS(s,seatingDistributionDict,maxList[i][0]) # returns proportion of blocks that aren't of size s
        numSeats = maxList[i][0] # the number of seats filled in the current seating arrangement
        maxList[i][0] = numSeats / maxSeats # set maxList tracker to the fill percentage as compared to the most filled arrangement
        degreeFilled = maxList[i][0] # pass above onto degreeFilled parameter for clarity
        maxList[i][0] = goodnessFunction(degreeFilled, 0.75, proportionNotS)
    return (seatingList[maxList.index(max(maxList, key = lambda x : x[0]))],max(maxList, key = lambda x : x[0])[0]) # return a tuple with the best seating arrangement as defined by goodness function at index 1 and that arrangement's goodness score at index 1

def propNotS(s,seatingDistributionDict,totalSeats):
    totalSeatsNotS = 0
    for key in seatingDistributionDict.keys(): # for all block sizes present
        if key != s: # as long as the block size does not equal s
            totalSeatsNotS += seatingDistributionDict[key] # add to tally
    return totalSeatsNotS/totalSeats # return the ratio

"""
Args:
    m (int): the length of the rectangle
    n (int): the width of the rectangle
    xBuffer (int): the number of seats to block
    within a row to ensure proper distancing
    yBuffer (int): the number of seats to block
    across rows to ensure proper distancing
    diagonalBuffer (int): the number of seats
    diagonal from the filled seat to block to
    ensure proper distancing
    s (int): the size of the seating block
    seatingArea (list): the table storing seating
    arrangements

Returns:
    A new seatingArea after attempting to squeeze in
    as many smaller blocks of sizes 8, 4, and 2 as
    possible
"""
def squeezeBlocksIn(m,n,xBuffer,yBuffer,diagonalBuffer,s,seatingArea,masterDict):
    s -= 1
    while s != 0: # iterating through all possible block sizes to squeeze in
        sizeTrackDict = fillRectangle(m,n,xBuffer,yBuffer,diagonalBuffer,s,seatingArea,True)
        for key in sizeTrackDict.keys():
            if key not in masterDict.keys(): # if we haven't seen this block size before
                masterDict[key] = 0 # initialize it
            masterDict[key] += sizeTrackDict[key] # regardless, add the number of seats added (if any) of this block size to it
        s -= 1
    return masterDict

choices = automateWhile(m,n,2,2,1,12,seatingTable.copy(),100)
seatingDoubleTuple = pickBestArrangement(12, choices)
seatingTuple = seatingDoubleTuple[0]
goodnessScore = seatingDoubleTuple[1]
seatingTable = seatingTuple[0]
currentDict = seatingTuple[1]
sizeTrackDict = squeezeBlocksIn(m,n,2,2,1,12,seatingTable,currentDict)

"""
Convert int 0s back into strings for printing
and count the number of seats that can be sold
"""
numSeats = 0
totalSeats = m*n
for line in seatingTable:
    for i in range(len(line)):
        numSeats += line[i]
        line[i] = str(line[i])

seatingEfficiency = (numSeats/totalSeats) * 100

"""
Handles file output from table into output
text document
"""
outputFile = open("output.txt", "w", encoding = "utf-8")
outputFile.writelines("    Sellable Seats: %d\n" % numSeats)
outputFile.writelines("  Section Capacity: %d\n" % totalSeats)
outputFile.writelines("Seating Efficiency: %.2f%%\n\n" % round(seatingEfficiency,2))
outputFile.writelines("Goodness Score: %.3f\n\n" % round(goodnessScore,3))
for key in sorted(sizeTrackDict.keys(),reverse = True):
    if sizeTrackDict[key] != 0:
        outputFile.writelines("Sellable %d Blocks: %d\n" % (key,sizeTrackDict[key]/key))
outputFile.writelines("\n")
outputFile.writelines("%s\n" % "".join(line) for line in seatingTable)
print("Done")