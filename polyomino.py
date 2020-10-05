# -*- coding: utf-8 -*-
#!/usr/bin/env python\

# Disclaimer: This code came from https://gist.github.com/passcod/6473452
# and was created by Félix Saparelli.
# I made edits to suit my seatingArrangement needs (namely instead of printing
# storing coordinates), but all credit goes to him for the algorithm.

import sys
import pickle

class Polyomino(object):

    def __init__(self, iterable):
        self.squares = tuple(sorted(iterable))

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, repr(self.squares))

    def __iter__(self):
        return iter(self.squares)

    def __len__(self):
        return len(self.squares)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        """Determine the one-sided key for this Poylomino"""
        p = self.translate()
        k = p.key()
        for _ in range(3):
            p = p.rotate().translate()
            k = min(k, p.key())
        return k

    def key(self):
        return hash(self.squares)

    def rotate(self):
        """Return a Polyomino rotated clockwise"""
        return Polyomino((-y, x) for x, y in self)

    def translate(self):
        """Return a Polyomino Translated to 0,0"""
        minX = min(s[0] for s in self)
        minY = min(s[1] for s in self)
        return Polyomino((x-minX, y-minY) for x, y in self)

    def raise_order(self):
        """Return a list of higher order Polyonominos evolved from self"""
        polyominoes = []
        for square in self:
            adjacents = (adjacent for adjacent in (
                (square[0] + 1, square[1]),
                (square[0] - 1, square[1]),
                (square[0], square[1] + 1),
                (square[0], square[1] - 1),
            ) if adjacent not in self)
            for adjacent in adjacents:
                polyominoes.append(
                    Polyomino(list(self) + [adjacent])
                )
        return polyominoes

    def render(self):
        """
        Returns a string map representation of the Polyomino
        """
        p = self.translate().rotate()
        order = len(p)
        return ''.join(
            ["\n %s" % (''.join(
                ["X" if (x, y) in p.squares else "-" for x in range(order)]
            )) for y in range(order)]
        )


def seatingBlocks(target):
    retList = []

    order = 1
    polyominoes = set([Polyomino(((0,0),))])

    while order < target:
        order += 1
        next_order_polyominoes = set()
        for polyomino in polyominoes:
            next_order_polyominoes.update(polyomino.raise_order())
        polyominoes = next_order_polyominoes

    for polyomino in polyominoes:
        newList = []
        for square in polyomino:
            x = square[0]
            y = square[1]
            newList.append([x,y])
        retList.append(newList)
    filteredPolys = filterPolys(retList)
    return filteredPolys

def filterPolys(polyominoes):
    suitablePolys = []
    for polyomino in polyominoes:
        if len(polyomino) == 1:
            return polyominoes
        polyGood = True
        polyDict = {}
        for seat in polyomino:
            x = seat[0]
            y = seat[1]
            if y not in polyDict.keys():
                polyDict[y] = []
            polyDict[y].append(x)
        for entry in polyDict.keys():
            if not(goodPoly(polyDict[entry])):
                polyGood = False
                break
            polyGood = True
        if polyGood:
            suitablePolys.append(polyomino)
    return suitablePolys

def goodPoly(listOfX):
    listOfX.sort()
    if len(listOfX) == 0:
        return False
    prev = listOfX[0]
    for i in range(len(listOfX)):
        if i == 0:
            continue
        cur = listOfX[i]
        if (cur - prev) == 1:
            return True
        prev = cur
    return False

print(len(seatingBlocks(12)))
"""
n = 12
arrangementDict = {}
while n > 0:
    arrangementDict[n] = seatingBlocks(n)
    print("Done with %d" % n)
    n -= 1

dictFile = open("seatinglib.pkl", "wb")
pickle.dump(arrangementDict, dictFile)
dictFile.close()


dictFile = open("seatinglib.pkl", "rb")
output = pickle.load(dictFile)
print(output)
"""
