import math
import random

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
            xCoord = seat[0]
            yCoord = seat[1]
            yBound = len(seatingArea)
            if yCoord < yBound:
                xBound = len(seatingArea[yCoord])
            else:
                feasiblePossibilities.remove(possibility)
                break
            if seat[0] >= xBound or seat[0] < 0 or seat[1] >= yBound or seat[1] < 0 or not(seatOkay(seat[0], seat[1], xBuffer, yBuffer, diagonalBuffer, seatingArea)): # essentially, if these seats are not safe to fill either b/c they don't exist within the grid or they are too close to another seat
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
        yBound = len(seatingArea)
        if seatYCoord < 0 or seatYCoord >= yBound:
            continue # this seat is out of the grid so it is okay to not account it as buffer
        xBound = len(seatingArea[seatYCoord])
        if seatXCoord < 0 or seatXCoord >= xBound:
            continue # this seat is out of the grid so it is okay to not account it as buffer
        elif seatingArea[seatYCoord][seatXCoord] == 1:
            return False # one of our seats we would need to block to fill [x,y] is filled, therefore, [x,y] cannot be filled
    return True # since we have gone through all of our seats that would need to be blocked off and none are already filled, [x,y] can be filled


"""
Args:
    xBuffer (int): the number of seats to block
    within a row to ensure proper distancing
    yBuffer (int): the number of seats to block
    across rows to ensure proper distancing
    diagonalBuffer (int): the number of seats
    diagonal from the filled seat to block to
    ensure proper distancing
    aisleBuffer (int): the number of seats to leave
    empty in the aisle
    aisleDirection (string): categorical string designating
    which side of the figure is the aisle; choices: "left"
    "right" "up" "down"
    s (int): the size of the seating block
    seatingArea (list): the table storing seating
    arrangements
    squeeze (boolean): whether or not this is the
    post-processing step to squeeze more blocks in
    (see squeezeBlocksIn function)

Returns:
    A new table filled with the most blocks of size
    s possible given the shape returned by fillSeats
    (since the algorithm is currently brute force, 
    this isn't necessarily the optimal arrangement)
"""
def fillRectangle(xBuffer,yBuffer,diagonalBuffer,aisleBuffer,aisleDirection,s,seatingArea,squeeze):
    sizeTrackDict = {} # dictionary to keep track of the number of blocks of each size in seatingArea
    counter = 0 
    fillS = True # bool to indicate whether we will be adding a block of size s or another size each time
    otherSeatingBlockSizes = [1,2,4,8] # other sizes to use when fillS == False
    xj = 0
    yj = 0
    yBound = len(seatingArea)
    if aisleDirection == "up":
        yj = 2
    elif aisleDirection == "down":
        yBound -= 2
    #if m*n < math.sqrt(s): ## FLAG: is this even necessary?
        #return sizeTrackDict # if the seating grid is too small to hold a single block of size s, don't do anything
    while yj < yBound:
        xBound = len(seatingArea[yj])
        if aisleDirection == "left":
            xj = 2
        elif aisleDirection == "right":
            xBound -= 2
        while xj < xBound:
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
    xBuffer (int): the number of seats to block
    within a row to ensure proper distancing
    yBuffer (int): the number of seats to block
    across rows to ensure proper distancing
    diagonalBuffer (int): the number of seats
    diagonal from the filled seat to block to
    ensure proper distancing
    aisleBuffer (int): the number of seats to leave
    empty in the aisle
    aisleDirection (string): categorical string designating
    which side of the figure is the aisle; choices: "left"
    "right" "up" "down"
    s (int): the size of the seating block
    seatingArea (list): the table storing seating
    arrangements
    reps (int): the number of times to try filling
    the seating area; as reps increases, so should
    the number of seats filled in the seatingArea
    returned, to a point: the optimal solution

Returns:
    A list of seatingArea arrangements of length
    reps to be decided upon by pickBestArrangement
    function
"""
def automateWhile(xBuffer,yBuffer,diagonalBuffer,aisleBuffer,aisleDirection,s,seatingArea,reps):
    choices = []
    while reps > 0:
        resetMap(seatingArea) # resets the seating Table by settting every seat back to 0
        sizeTrackDict = fillRectangle(xBuffer,yBuffer,diagonalBuffer,aisleBuffer,aisleDirection,s,seatingArea,False)
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
    proportionNotS (int): the share of blocks in the
    seating arrangement that aren't of size s

Returns:
    A score between 0 and 1 (good score ~ 0.85, needs
    research) that represents how good a certain seating
    arrangement is; basis of seating arrangement choice
    for pickBestArrangement
"""
def goodnessFunction(degreeFilled, weightDegreeFilled, proportionNotS):
    weightPropNotS = 1 - weightDegreeFilled # to ensure two proportions sum to 1
    return (degreeFilled * weightDegreeFilled) + (proportionNotS * weightPropNotS)

"""
Args:
    s (int): the size of the seating block
    seatingList (list): a list of randomly generated
    seating arrangements created by automateWhile

Returns:
    A tuple with the first element being the seating
    table with the highest goodness score, the second
    being the goodness score of that arrangement, and
    the third being the highest number of seats that
    were able to be filled amongst all arrangements
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
    return (seatingList[maxList.index(max(maxList, key = lambda x : x[0]))],max(maxList, key = lambda x : x[0])[0],maxSeats)

"""
Args:
    s (int): the size of the seating block
    seatingDistributionDict (dict): A dictionary storing
    the number of sizes of all seating blocks in
    the seatingList
    totalSeats (int): the total number of seats filled
    in the seatingList specified by seatingDistributionDict

Returns:
    A float value representing the proportion of blocks in
    the seatingList specified by seatingDistributionDict of
    size s
"""
def propNotS(s,seatingDistributionDict,totalSeats):
    totalSeatsNotS = 0
    for key in seatingDistributionDict.keys(): # for all block sizes present
        if key != s: # as long as the block size does not equal s
            totalSeatsNotS += seatingDistributionDict[key] # add to tally
    return totalSeatsNotS/totalSeats # return the ratio

"""
Args:
    xBuffer (int): the number of seats to block
    within a row to ensure proper distancing
    yBuffer (int): the number of seats to block
    across rows to ensure proper distancing
    diagonalBuffer (int): the number of seats
    diagonal from the filled seat to block to
    ensure proper distancing
    aisleBuffer (int): the number of seats to leave
    empty in the aisle
    aisleDirection (string): categorical string designating
    which side of the figure is the aisle; choices: "left"
    "right" "up" "down"
    s (int): the size of the seating block
    seatingArea (list): the table storing seating
    arrangements
    masterDict (dict): The dictionary from the original filling
    of the seatingArea storing block sizes and amounts

Returns:
    Creates a new seatingArea after attempting to squeeze in
    as many smaller blocks of sizes less than s, returns
    an updated dictionary of all block sizes
"""
def squeezeBlocksIn(xBuffer,yBuffer,diagonalBuffer,aisleBuffer,aisleDirection,s,seatingArea,masterDict):
    s -= 1
    while s != 0: # iterating through all possible block sizes to squeeze in
        sizeTrackDict = fillRectangle(xBuffer,yBuffer,diagonalBuffer,aisleBuffer,aisleDirection,s,seatingArea,True)
        for key in sizeTrackDict.keys():
            if key not in masterDict.keys(): # if we haven't seen this block size before
                masterDict[key] = 0 # initialize it
            masterDict[key] += sizeTrackDict[key] # regardless, add the number of seats added (if any) of this block size to it
        s -= 1
    return masterDict

"""
Args:
    filename (string): string containing entire filepath 
    
Returns:
    Filename without the rest of its path or
    extension
"""
def removeExtension(filename):
    i = filename.index("/")
    f = filename.index(".")
    return filename[i+1:f]

def run(filename):
    h = open(filename, "r", encoding="utf-8")

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

    choices = automateWhile(2,2,1,2,"left",12,seatingTable.copy(),100)
    seatingDoubleTuple = pickBestArrangement(12, choices)
    seatingTuple = seatingDoubleTuple[0]
    goodnessScore = seatingDoubleTuple[1]
    maxSeats = seatingDoubleTuple[2]
    seatingTable = seatingTuple[0]
    currentDict = seatingTuple[1]
    sizeTrackDict = squeezeBlocksIn(2,2,1,2,"left",12,seatingTable,currentDict)

    """
    Convert int 0s back into strings for printing
    and count the number of seats that can be sold
    """
    numSeats = 0
    totalSeats = 0
    for line in seatingTable:
        for i in range(len(line)):
            numSeats += line[i]
            totalSeats += 1
            line[i] = str(line[i])

    seatingEfficiency = (numSeats/totalSeats) * 100

    """
    Handles file output from table into output
    text document
    """

    filename = removeExtension(filename)
    filename2 = filename + "out.txt"
    filepath = "output/" + filename2
    #print(filepath)

    outputFile = open(filepath, "w", encoding = "utf-8")
    outputFile.writelines("    Sellable Seats: %d\n" % numSeats)
    outputFile.writelines("  Section Capacity: %d\n" % totalSeats)
    outputFile.writelines("Seating Efficiency: %.2f%%\n\n" % round(seatingEfficiency,2))
    outputFile.writelines("Goodness Score: %.3f\n\n" % round(goodnessScore,3))
    for key in sorted(sizeTrackDict.keys(),reverse = True):
        if sizeTrackDict[key] != 0:
            outputFile.writelines("Sellable %d Blocks: %d\n" % (key,sizeTrackDict[key]/key))
    outputFile.writelines("\n")
    outputFile.writelines("%s\n" % "".join(line) for line in seatingTable)
    return [goodnessScore,numSeats,totalSeats,sizeTrackDict,maxSeats]