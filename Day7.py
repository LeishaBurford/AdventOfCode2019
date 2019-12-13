import itertools
from pathlib import Path
from collections import deque

data_folder = Path("./PuzzleData/")
file_to_open = data_folder / "Day7.txt"
with open(file_to_open) as instructionInput:
    opCodes = [int(code) for code in instructionInput.read().split(',')]

originalProgram = [code for code in opCodes]


class Amplifier:
    def __init__(self, instructions, name):
        self.instructions = instructions
        self.inputs = []
        self.instructionPointer = 0
        self.programStatus = ''
        self.outputs = []
        self.name = name

    def runAmplifier(self):
        programResponse = compute(
            self.instructions, self.inputs, self.instructionPointer, self.outputs)
        self.instructions = programResponse[0]
        self.instructionPointer = programResponse[1]
        self.programStatus = programResponse[2]

    def waitingForInput(self):
        return self.programStatus == 'WAITING'

    def halted(self):
        return self.programStatus == 'HALT'
    
    def __str__(self):
        return f'{self.name}\n{self.programStatus}\n{self.instructions}\n{self.inputs}\n{self.outputs}\n{self.instructionPointer}'


def compute(instructions, inputSignal, currentIndex, outputSignals):
    index = currentIndex
    # outputCode = 0
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
            # inputValue = setting if setting != -1 else signal
            if len(inputSignal) == 0:
                programStatus = 'WAITING'
                break
            instructions[parameter1] = inputSignal.pop(0)
            index += 2
            # setting = -1
        if opCode == 4:
            # outputCode = instructions[parameter1]
            # programStatus = 'OUTPUT'
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
    return (instructions, index, programStatus)


possibleSettings = list(itertools.permutations([0, 1, 2, 3, 4]))

bestSetting = (0, 0)
for possibleSetting in possibleSettings:
    inputSignal = [0]
    outputSignals = []
    for setting in possibleSetting:
        inputSignal.insert(0, setting)
        opCodes = originalProgram
        # inputSignal.append(compute(opCodes, inputSignal))
        compute(opCodes, inputSignal, 0, outputSignals)
        for output in outputSignals:
            inputSignal.append(output)
        outputSignals = []
    if inputSignal[-1] > bestSetting[1]:
        bestSetting = (possibleSetting, inputSignal[-1])

print('Part 1: ', bestSetting[1])

# Could not get part 2 :(
possibleSettings = list(itertools.permutations([5, 6, 7, 8, 9]))
possibleSetting = [9, 8, 7, 6, 5]
opCodes = originalProgram

feedbackLoop = []
completedAmps = []
for setting in possibleSetting:
    feedbackLoop.append(Amplifier(opCodes, setting))
    feedbackLoop[-1].inputs.append(setting)

feedbackLoop[0].inputs.append(0)
while len(feedbackLoop) > 0:
    currentAmp = feedbackLoop.pop(0)
    currentAmp.runAmplifier()
    for output in currentAmp.outputs:
        feedbackLoop[0].inputs.append(output)
    if currentAmp.halted():
        completedAmps.append(currentAmp)
    currentAmp.outputs = []  # this will probably mess with the one we are storing
    if currentAmp.waitingForInput():
        feedbackLoop.append(currentAmp)
    if len(completedAmps) == len(possibleSetting):
        break
print(completedAmps)
