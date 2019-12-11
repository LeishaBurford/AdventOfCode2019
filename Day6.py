from pathlib import Path
data_folder = Path("./PuzzleData/")

file_to_open = data_folder / "Day6.txt"
with open(file_to_open) as orbitData:
    orbits = [orbit.strip().split(')') for orbit in orbitData.readlines()]

orbits = [[orbit[1], orbit[0]] for orbit in orbits]
# make into chain of dict
# print(orbits)

orbitCount = 0
currentOrbit = orbits[-1][1]
while currentOrbit != 'COM':
    # use dict key lookup to find current orbit
    # update count and current orbit
    # https://dbader.org/blog/python-dictionaries-maps-and-hashtables
