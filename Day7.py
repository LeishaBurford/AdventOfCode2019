import itertools
from pathlib import Path
from collections import deque

data_folder = Path("./PuzzleData/")
file_to_open = data_folder / "Day7.txt"
with open(file_to_open) as instructionInput:
    opCodes = [int(code) for code in instructionInput.read().split(',')]

originalProgram = [code for code in opCodes]


def compute(instructions, inputSignal, currentIndex):
    index = currentIndex
    # outputCode = 0
    programStatus = ''
    while index < len(instructions):
        opCode = instructions[index] % 100
        if opCode == 99:
            programStatus = 'HALT'
            break
        fullCode = [int(digit) for digit in str(instructions[index]).zfill(5)]
        parameter1 = instructions[index + 1] if fullCode[2] == 0 else index + 1
        parameter2 = instructions[index + 2] if fullCode[1] == 0 else index + 2
        parameter3 = instructions[index + 3] if fullCode[0] == 0 else index + 3
        if opCode == 1:
            instructions[parameter3] = instructions[parameter1] + \
                instructions[parameter2]
            index += 4
        if opCode == 2:
            instructions[parameter3] = instructions[parameter1] * \
                instructions[parameter2]
            index += 4
        if opCode == 3:
            # inputValue = setting if setting != -1 else signal
            if len(inputSignal) < 1:
                programStatus = 'WAITING'
                break
            instructions[parameter1] = inputSignal.pop(0)
            index += 2
            # setting = -1
        if opCode == 4:
            # outputCode = instructions[parameter1]
            # programStatus = 'OUTPUT'
            inputSignal.append(instructions[parameter1])
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
    return (instructions, index, programStatus)


# possibleSettings = list(itertools.permutations([0, 1, 2, 3, 4]))

# bestSetting = (0, 0)
# for possibleSetting in possibleSettings:
#     inputSignal = [0]
#     for setting in possibleSetting:
#         inputSignal.insert(0, setting)
#         opCodes = originalProgram
#         # inputSignal.append(compute(opCodes, inputSignal))
#         compute(opCodes, inputSignal, 0)
#     if inputSignal[-1] > bestSetting[1]:
#         bestSetting = (possibleSetting, inputSignal[0])

# print('Part 1: ', bestSetting[1])

# input signal, instructions, pointer to current instruction, 
# bestSetting = (0, 0)


possibleSettings = list(itertools.permutations([5, 6, 7, 8, 9]))
possibleSetting = [9,8,7,6,5]   
# inputSignal = [setting for setting in possibleSetting]
opCodes = originalProgram

feedbackLoop = deque([(opCodes, 0) for setting in possibleSetting])
inputSignals = [0]
setingsToUse = [a for a in possibleSetting]
while len(feedbackLoop) > 0:
    currentAmp = feedbackLoop.popleft()
    if len(setingsToUse) > 0:
        inputSignals.insert(0, setingsToUse.pop(0))
    programResponse = compute(currentAmp[0], inputSignals, currentAmp[1])
    if programResponse[2] == 'WAITING':
        feedbackLoop.append((programResponse[0], programResponse[1]))
        
print(inputSignals)