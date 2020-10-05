import math

def seatsSaved(n, seatingBuffer):
    if math.sqrt(n) != int(math.sqrt(n)):
        return "Cannot form cube out of " + str(n) + " seats"
    else:
        seatsNeededLine = 2 * seatingBuffer * n + 2 * seatingBuffer
        seatsNeededCube = 4 * seatingBuffer * math.sqrt(n)
        return "You can save " + str(int(seatsNeededLine - seatsNeededCube)) + " seats by using a cube instead of a line seating arrangement"

print(seatsSaved(9, 3))