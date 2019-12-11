from pathlib import Path
data_folder = Path("./PuzzleData/")

file_to_open = data_folder / "Day2.txt"


with open(file_to_open) as input:
    opCodes = [int(code) for code in input.read().split(',')]
# print(opCodes)


def compute(instructions):
    for index in range(0, len(instructions) - 4, 4):
        if instructions[index] == 99 or opCodes[index] > len(opCodes) - 3:
            break
        if instructions[index] == 1:
            instructions[opCodes[index + 3]] = instructions[instructions[index + 1]] + instructions[instructions[index + 2]]
        if instructions[index] == 2:
            instructions[instructions[index + 3]] = instructions[instructions[index + 1]] * instructions[instructions[index + 2]]

# compute(opCodes)

nouns = [i for i in range(99)]
verbs = [i for i in range(99)]

baseMemory = [code for code in opCodes]
for noun in nouns:
    for verb in verbs:
        opCodes = [code for code in baseMemory]
        opCodes[1] = noun
        opCodes[2] = verb
        compute(opCodes)
        if opCodes[0] == 19690720:
            print(noun, verb)
for verb in verbs:
    for noun in nouns:
        opCodes = [code for code in baseMemory]
        opCodes[1] = noun
        opCodes[2] = verb
        compute(opCodes)
        if opCodes[0] == 19690720:
            print(noun, verb)
print('done')


