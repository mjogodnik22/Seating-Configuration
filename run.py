from engine import run, propNotS, goodnessFunction
import os

folder_path = "input"
input_path = "input/"

directory = os.fsencode(folder_path)

masterDict = {}
seatsFilled = 0
totalSeats = 0
maxSeats = 0

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    filepath = "input/" + filename
    if filename.endswith(".txt"):
        #print(filename)
        returnList = run(filepath)
        goodnessScoreSection = returnList[0]
        seatsFilledSection = returnList[1]
        totalSeatsSection = returnList[2]
        sizeTrackDict = returnList[3]
        maxSeatsSection = returnList[4]
        maxSeats += maxSeatsSection
        seatsFilled += seatsFilledSection
        totalSeats += totalSeatsSection
        for key in sizeTrackDict.keys():
            if key not in masterDict.keys():
                masterDict[key] = 0
            masterDict[key] += sizeTrackDict[key]

def average(lst):
    total = 0
    counter = 0
    for element in lst:
        total += element
        counter += 1
    return total/counter

proportionNotS = propNotS(12,masterDict,seatsFilled) # returns proportion of blocks that aren't of size s
degreeFilled = seatsFilled/maxSeats
goodnessScore = goodnessFunction(degreeFilled, 0.75, proportionNotS)

seatingEfficiency = (seatsFilled/totalSeats) * 100
outputFile = open("output/overallstats.txt", "w", encoding = "utf-8")
outputFile.writelines("    Sellable Seats: %d\n" % seatsFilled)
outputFile.writelines("  Section Capacity: %d\n" % totalSeats)
outputFile.writelines("Seating Efficiency: %.2f%%\n\n" % round(seatingEfficiency,2))
outputFile.writelines("Goodness Score: %.3f\n\n" % round(goodnessScore,3))
for key in sorted(masterDict.keys(),reverse = True):
    if masterDict[key] != 0:
        outputFile.writelines("Sellable %d Blocks: %d\n" % (key,masterDict[key]/key))