import itertools
from pathlib import Path

data_folder = Path("./PuzzleData/")
file_to_open = data_folder / "Day11.txt"
with open(file_to_open) as instructionInput:
    opCodes = [int(code) for code in instructionInput.read().split(',')]

originalProgram = [code for code in opCodes]

def getParameter(instructions, index, parameterCode, relativeBase):
    parameterValue = 0
    if parameterCode == 0:
        parameterValue = instructions[index]
    if parameterCode == 1:
        return index
    if parameterCode == 2:
        parameterValue = relativeBase + instructions[index]
    for i in range(len(instructions), parameterValue + 1):
        instructions.append(0)
    if parameterValue == -1:
        print('ahhhhh')
    return parameterValue

def compute(instructions, inputSignal, currentIndex, outputSignals, relativeBase):
    index = currentIndex
    programStatus = 'CONTINUE'
    # relativeBase = 0
    needSecondParam = [1, 2, 5, 6, 7, 8]
    needThirdParam = [1, 2, 7, 8]
    while index < len(instructions):
        opCode = instructions[index] % 100
        if opCode == 99:
            programStatus = 'HALT'
            break
        fullCode = [int(digit) for digit in str(instructions[index]).zfill(5)]
        parameter1 = getParameter(instructions, index + 1, fullCode[2], relativeBase)
        parameter2 = getParameter(instructions, index + 2, fullCode[1], relativeBase) if opCode in needSecondParam else 0       
        parameter3 = getParameter(instructions, index + 3, fullCode[0], relativeBase) if opCode in needThirdParam else 0      
        if opCode == 1:
            instructions[parameter3] = instructions[parameter1] + \
                instructions[parameter2]
            index += 4
        if opCode == 2:
            instructions[parameter3] = instructions[parameter1] * \
                instructions[parameter2]
            index += 4
        if opCode == 3:
            if len(inputSignal) == 0:
                programStatus = 'WAITING'
                break
            instructions[parameter1] = inputSignal.pop(0)
            index += 2
        if opCode == 4:
            outputSignals.append(instructions[parameter1])
            index += 2
        if opCode == 5:
            index = instructions[parameter2] if instructions[parameter1] != 0 else index + 3
        if opCode == 6:
            index = instructions[parameter2] if instructions[parameter1] == 0 else index + 3
        if opCode == 7:
            instructions[parameter3] = 1 if instructions[parameter1] < instructions[parameter2] else 0
            index += 4
        if opCode == 8:
            instructions[parameter3] = 1 if instructions[parameter1] == instructions[parameter2] else 0
            index += 4
        if opCode == 9:
            relativeBase += instructions[parameter1]
            index += 2
    return (instructions, index, programStatus, relativeBase)

def move(position, moveCode):
    if moveCode == 0:
        return (position[0], position[1] + 1)
    if moveCode == 1:
        return (position[0] + 1, position[1])
    if moveCode == 2:
        return (position[0], position[1] - 1)
    if moveCode == 3:
        return (position[0] - 1, position[1])


def getRobotDirection(moveRight, currentDirection):
    if currentDirection == 0:
        return 1 if moveRight else 3
    if currentDirection == 1:
        return 2 if moveRight else 0
    if currentDirection == 2:
        return 3 if moveRight else 1
    if currentDirection == 3:
        return 0 if moveRight else 2


def paint(startingColour, program):
    halted = False
    robotPosition = (0, 0)
    positions = {robotPosition: startingColour}
    robotDirection = 0
    programPosition = 0
    relativeBase = 0
    while not halted:
        outputSignals = []
        if robotPosition in positions:
            intputSignal = [positions[robotPosition]]
        else:
            intputSignal = [0]
        computerResponse = compute(
            program, intputSignal, programPosition, outputSignals, relativeBase)
        programPosition = computerResponse[1]
        relativeBase = computerResponse[3]
        if computerResponse[2] == 'HALT':
            halted = True
        if outputSignals != []:
            positions[robotPosition] = outputSignals[0]
            robotDirection = getRobotDirection(outputSignals[1], robotDirection)
            robotPosition = move(robotPosition, robotDirection)
            if robotPosition == (1, 0):
                print('ahhhhh')
    return positions


# print('Part 1:', len(paint(0, opCodes)))

# reset computer for part 2
opCodes = originalProgram

paintedPositions = paint(1, opCodes)
paintedWhite = [position for position in paintedPositions if paintedPositions[position] == 1 ]

invalidPoint = [point for point in paintedPositions if paintedPositions[point] != 1 and paintedPositions[point] != 0]

# xSorted = sorted(paintedWhite, key=lambda x: x[0])
xSorted = sorted(paintedPositions.keys(), key=lambda x: x[0])

# ySorted = sorted(paintedWhite, key=lambda x: x[1])
ySorted = sorted(paintedPositions.keys(), key=lambda x: x[1])

for y in range(ySorted[-1][1], ySorted[0][1] - 1, -1):
    for x in range(xSorted[0][0], xSorted[-1][0] + 1):
        if (x, y) in paintedWhite:
            print('#', end='')
        else:
            print(' ', end='')
    print()

# for y in range(-50, 50):
#     for x in range(-40,40):
#         if (x, y) in paintedWhite:
#             print('#', end='')
#         else:
#             print(' ', end='')
#     print()
