from pathlib import Path
import numpy as np
data_folder = Path("./PuzzleData/")

file_to_open = data_folder / "Day3.txt"


with open(file_to_open) as input:
    wireMoves = [wire.strip().split(',') for wire in input.readlines()]
print(wireMoves)

def getNextPositions(move, currentPosition):
    if move[0] =='R':
        lineEnd = [currentPosition[0] + int(move[1:]), currentPosition[1]]
        return np.array([[x, lineEnd[1]] for x in range(currentPosition[0], lineEnd[0] + 1)]).flatten()
    if move[0] =='L':
        lineEnd = [currentPosition[0] - int(move[1:]), currentPosition[1]]
        return np.array([[x, lineEnd[1]] for x in range(currentPosition[0], lineEnd[0] + 1, -1)]).flatten()
    if move[0] =='U':
        lineEnd = [currentPosition[0], currentPosition[1] + int(move[1:])]  
        return np.array([[lineEnd[0], x] for x in range(currentPosition[1], lineEnd[1] + 1)]).flatten()
    if move[0] =='D':
        lineEnd = [currentPosition[0], currentPosition[1] - int(move[1:])]
        return np.array([[lineEnd[0], x] for x in range(currentPosition[1], lineEnd[1] + 1, -1)]).flatten()

def getWirePositions(wire):
    wirePositions = []
    currentPosition = [0, 0]
    for move in wire:
        # print(getNextPositions(move, currentPosition))
        nextPosition = getNextPositions(move, currentPosition)
        wirePositions.append(nextPosition)
        currentPosition = nextPosition[-1]
    print(wirePositions)
    return wirePositions

def getManhattanDistance(a, b):
    return abs(a[0] - b[0]) + abs(b[1] - a[1])

wireOnePositions = getWirePositions(wireMoves[0])
wireTwoPositions = getWirePositions(wireMoves[1])

print(wireOnePositions)
print(wireTwoPositions)

intersections = [point for point in wireOnePositions if [point[0], point[1]] in wireTwoPositions]
print(intersections)
distances = [getManhattanDistance([0, 0], point) for point in intersections]



print(max(distances))