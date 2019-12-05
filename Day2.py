from pathlib import Path
from math import floor
data_folder = Path("./PuzzleData/")

file_to_open = data_folder / "Day2.txt"


with open(file_to_open) as input:
    opCodes = [int(code) for code in input.read().split(',')]
print(opCodes)

for index in range(0, len(opCodes) - 4, 4):
    print(index)
    if opCodes[index] == 99:
        break
    if opCodes[index] == 1:
        opCodes[opCodes[index + 3]] = opCodes[opCodes[index + 1]] + opCodes[opCodes[index + 2]]
    if opCodes[index] == 2:
        opCodes[opCodes[index + 3]] = opCodes[opCodes[index + 1]] * opCodes[opCodes[index + 2]]

print(opCodes[0])


