from pathlib import Path
data_folder = Path("./PuzzleData/")
file_to_open = data_folder / "Day10.txt"
with open(file_to_open) as input:
    asteroids = [[asteroid for asteroid in row.strip()]
                 for row in input.readlines()]


def prettyPrintMatrix(matrix):
    for row in matrix:
        print(row)


def getAsteroidLocations(asteroidLocations, position):
    postions = []
    for x, row in enumerate(asteroidLocations):
        for y, col in enumerate(row):
            if col == '#':
                postions.append((x + position[0], y + position[1]))
    return postions


def getQuadrants(asteroidLocations, stationLocation):
    a = stationLocation[0]
    b = stationLocation[1]
    firstQuadrant = [[location for location in row[:b]]
                     for row in asteroidLocations[:a]]
    firstQuadrant = getAsteroidLocations(firstQuadrant, (0, 0))
    secondQuadrant = [[location for location in row[b + 1:]]
                      for row in asteroidLocations[:a]]
    secondQuadrant = getAsteroidLocations(secondQuadrant, (0, b + 1))
    thirdQuadrant = [[location for location in row[:b]]
                     for row in asteroidLocations[a + 1:]]
    thirdQuadrant = getAsteroidLocations(thirdQuadrant, (a + 1, 0))
    fourthQuadrant = [[location for location in row[b + 1:]]
                      for row in asteroidLocations[a + 1:]]
    fourthQuadrant = getAsteroidLocations(fourthQuadrant, (a + 1, b + 1))

    return [firstQuadrant, secondQuadrant, thirdQuadrant, fourthQuadrant]


def getDirectAsteroids(asteroidLocations, stationLocation):
    total = 0
    a = stationLocation[0]
    b = stationLocation[1]
    if asteroidLocations[b][:a].count('#') > 0:
        total += 1
    if asteroidLocations[b][a + 1:].count('#') > 0:
        total += 1

    verticalLineOfSight = [location[a] for location in asteroids]
    if verticalLineOfSight[:b].count('#') > 0:
        total += 1
    if verticalLineOfSight[b + 1:].count('#') > 0:
        total += 1
    return total


def vaporizeDirectAsteroids(asteroidLocations, stationLocation, directionOfVaporizer):
    a = stationLocation[0]
    b = stationLocation[1]
    verticalLineOfSight = [location[a] for location in asteroids]

    if directionOfVaporizer == 1:
        toBeVaporized = (a, asteroidLocations[b][:a].index('#'))
    if directionOfVaporizer == 3:
        toBeVaporized = (a, asteroidLocations[b][a + 1:].index('#'))
    if directionOfVaporizer == 0:
        toBeVaporized = (verticalLineOfSight[:b].index('#'), b)
    if directionOfVaporizer == 2:
        toBeVaporized = (verticalLineOfSight[b + 1:].index('#'), b)
    asteroidLocations[toBeVaporized[0]][toBeVaporized[1]] = 'x'


def getSlope(a, b):
    return (a[0] - b[0]) / (a[1] - b[1])


possibleStationLocations = []
for x, row in enumerate(asteroids):
    for y, col in enumerate(row):
        if asteroids[x][y] == '#':
            possibleStationLocations.append((x, y))

bestAsteroidVisibility = ((0, 0), 0)
for position in possibleStationLocations:
    asteroidCount = getDirectAsteroids(asteroids, position)
    for quad in getQuadrants(asteroids, position):
        slopes = []
        for location in quad:
            if location != position:
                slope = getSlope(position, location)
                if slope not in slopes:
                    slopes.append(slope)
        asteroidCount += len(slopes)
    # print((position, asteroidCount))
    if asteroidCount > bestAsteroidVisibility[1]:
        bestAsteroidVisibility = (position, asteroidCount)

print('Part 1: ', bestAsteroidVisibility)

lastVaporized = (0, 0)
station = bestAsteroidVisibility[0]
for vaporizedAsteroid in range(0, 200):
    # prettyPrintMatrix(asteroids)
    for quad in getQuadrants(asteroids, station):
        vaporizeDirectAsteroids(
            asteroids, station, vaporizedAsteroid % 4)
        # prettyPrintMatrix(asteroids)
        slopes = []
        for location in quad:
            if location != station:
                slope = getSlope(station, location)
                if slope not in slopes:
                    slopes.append(slope)
                    asteroids[location[0]][location[1]] = 'x'
                    lastVaporized = location
                    # print(lastVaporized)

print('Part 2: ', lastVaporized, (lastVaporized[1] * 100) + lastVaporized[0])
