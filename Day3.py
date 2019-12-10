from pathlib import Path
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
    stepsPerPoint = {}
    steps = 0
    currentPosition = [0, 0]
    for move in wire:
        nextPosition = getNextPositions(move, currentPosition)
        wirePositions.append(nextPosition)
        currentPosition = nextPosition[-1]
        steps = updateSteps(nextPosition, stepsPerPoint,steps)
        
    return wirePositions, stepsPerPoint

def updateSteps(nextPositions, stepsPerPoint, steps):
    for position in nextPositions:
        steps += 1
        if((position[0], position[1]) not in stepsPerPoint):
                stepsPerPoint[(position[0], position[1])] = steps
    return steps

def getManhattanDistance(a, b):
    return abs(a[0] - b[0]) + abs(b[1] - a[1])

# def getMinTotalSteps()

wireOnePositions, steps1 = getWirePositions(wireMoves[0])
wireOnePositions = list(itertools.chain(*wireOnePositions))

wireTwoPositions, steps2 = getWirePositions(wireMoves[1])
wireTwoPositions = list(itertools.chain(*wireTwoPositions))

# Graph it for fun :)
# plt.scatter(*zip(*wireOnePositions))
# plt.scatter(*zip(*wireTwoPositions))
# plt.show()

intersections =  set([(point[0], point[1]) for point in wireOnePositions ]).intersection(set([(point[0], point[1]) for point in wireTwoPositions ]))

distances = [getManhattanDistance([0, 0], point) for point in intersections]
totalSteps = [steps1[point] + steps2[point] for point in intersections]

print('Part 1: ', min(distances))
print('Part 2: ', min(totalSteps))