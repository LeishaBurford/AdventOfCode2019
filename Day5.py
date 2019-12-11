from pathlib import Path
data_folder = Path("./PuzzleData/")

file_to_open = data_folder / "Day5.txt"
with open(file_to_open) as instructionInput:
    opCodes = [int(code) for code in instructionInput.read().split(',')]

originalProgram = [code for code in opCodes]

def compute(instructions, inputValue):
    index = 0
    outputCodes = []
    while index < len(instructions):
        opCode = instructions[index] % 100
        if opCode == 99:
            break
        fullCode = [int(digit) for digit in str(instructions[index]).zfill(5)]            
        parameter1 = instructions[index + 1] if fullCode[2] == 0 else index + 1
        parameter2 = instructions[index + 2] if fullCode[1] == 0 else index + 2
        parameter3 = instructions[index + 3] if fullCode[0] == 0 else index + 3
        if opCode == 1:
            instructions[parameter3] = instructions[parameter1] + instructions[parameter2]
            index += 4
        if opCode == 2:
            instructions[parameter3] = instructions[parameter1] * instructions[parameter2]
            index += 4
        if opCode == 3:
            instructions[parameter1] = inputValue
            index += 2
        if opCode == 4:
            outputCodes.append(instructions[parameter1])
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
    return outputCodes

print('Part 1: ', compute(opCodes, 1))
opCodes = originalProgram
print('Part 2: ', compute(opCodes, 5))


