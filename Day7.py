import itertools
from pathlib import Path
from collections import deque

data_folder = Path("./PuzzleData/")
file_to_open = data_folder / "Day7.txt"
with open(file_to_open) as instructionInput:
    opCodes = [int(code) for code in instructionInput.read().split(',')]

originalProgram = [code for code in opCodes]


def compute(instructions, setting, signal):
    index = 0
    outputCode = 0
    programStatus = 'CONTINUE'
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
            inputValue = setting if setting != -1 else signal
            instructions[parameter1] = inputValue
            index += 2
            setting = -1
        if opCode == 4:
            outputCode = instructions[parameter1]
            programStatus = 'OUTPUT'
            index += 2
            break
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
    return outputCode


possibleSettings = list(itertools.permutations([0, 1, 2, 3, 4]))

bestSetting = (0, 0)
for possibleSetting in possibleSettings:
    inputSignal = 0
    for setting in possibleSetting:
        opCodes = originalProgram
        inputSignal = compute(opCodes, setting, inputSignal)
    if inputSignal > bestSetting[1]:
        bestSetting = (possibleSetting, inputSignal)

print('Part 1: ', bestSetting[1])
