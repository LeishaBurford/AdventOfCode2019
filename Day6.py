from pathlib import Path
data_folder = Path("./PuzzleData/")

file_to_open = data_folder / "Day6.txt"
with open(file_to_open) as orbitData:
    orbits = [orbit.strip().split(')') for orbit in orbitData.readlines()]

orbits = {orbit[1]: orbit[0] for orbit in orbits}

def getOrbitCount(startingOrbit, recordedOrbits):
    count = 0
    while startingOrbit != 'COM':
        count += 1
        startingOrbit = orbits[startingOrbit]
    return count

def getPathToCOM(startingOrbit, recordedOrbits):
    orbitPath = []
    while startingOrbit != 'COM':
        orbitPath.append(startingOrbit)
        startingOrbit = orbits[startingOrbit]
    return orbitPath

orbitCount = 0
for orbit in orbits.keys():
    currentOrbit = orbit
    orbitCount += getOrbitCount(currentOrbit, orbits)

print('Part 1: ', orbitCount)

myPath = getPathToCOM(orbits['YOU'], orbits)
santaPath = getPathToCOM(orbits['SAN'], orbits)
intersection = [me for me in myPath if me in santaPath]
minimumOrbitCount = len(myPath) + len(santaPath) - 2 * len(intersection)

print('Part 2: ',minimumOrbitCount)

