import itertools
from pathlib import Path

data_folder = Path("./PuzzleData/")
file_to_open = data_folder / "Day9.txt"
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
    return parameterValue

def compute(instructions, inputSignal, currentIndex, outputSignals):
    index = currentIndex
    programStatus = 'CONTINUE'
    relativeBase = 0
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
    return (instructions, index, programStatus)

inputSignals = [2]
outputSignals = []
compute(opCodes, inputSignals, 0, outputSignals)
print(outputSignals)