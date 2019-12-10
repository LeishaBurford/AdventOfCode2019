from pathlib import Path
import numpy as np
import itertools
import matplotlib.pyplot as plt

data_folder = Path("./PuzzleData/")
file_to_open = data_folder / "Day3.txt"

with open(file_to_open) as input:
    wireMoves = [wire.strip().split(',') for wire in input.readlines()]

def getNextPositions(move, currentPosition):
    if move[0] =='R':
        lineEnd = [currentPosition[0] + int(move[1:]), currentPosition[1]]
        return [[x, lineEnd[1]] for x in range(currentPosition[0] + 1, lineEnd[0] + 1)]
    if move[0] =='L':
        lineEnd = [currentPosition[0] - int(move[1:]), currentPosition[1]]
        return [[x, lineEnd[1]] for x in range(currentPosition[0] - 1, lineEnd[0] - 1, -1)]
    if move[0] =='U':
        lineEnd = [currentPosition[0], currentPosition[1] + int(move[1:])]  
        return [[lineEnd[0], x] for x in range(currentPosition[1] + 1, lineEnd[1] + 1)]
    if move[0] =='D':
        lineEnd = [currentPosition[0], currentPosition[1] - int(move[1:])]
        return [[lineEnd[0], x] for x in range(currentPosition[1] - 1, lineEnd[1] - 1, -1)]

def getWirePositions(wire):
    wirePositions = []
    currentPosition = [0, 0]
    for move in wire:
        nextPosition = getNextPositions(move, currentPosition)
        wirePositions.append(nextPosition)
        currentPosition = nextPosition[-1]
    return wirePositions

def getManhattanDistance(a, b):
    return abs(a[0] - b[0]) + abs(b[1] - a[1])

wireOnePositions = list(itertools.chain(*getWirePositions(wireMoves[0])))
wireTwoPositions = list(itertools.chain(*getWirePositions(wireMoves[1])))

# Graph it for fun :)
plt.scatter(*zip(*wireOnePositions))
plt.scatter(*zip(*wireTwoPositions))
plt.show()

intersections =  set([(point[0], point[1]) for point in wireOnePositions ]).intersection(set([(point[0], point[1]) for point in wireTwoPositions ]))
distances = [getManhattanDistance([0, 0], point) for point in intersections]

print(min(distances))