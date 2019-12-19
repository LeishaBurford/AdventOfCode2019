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

    return [secondQuadrant, fourthQuadrant, thirdQuadrant, firstQuadrant]


def getDirectAsteroids(asteroidLocations, stationLocation):
    total = 0
    a = stationLocation[0]
    b = stationLocation[1]
    if asteroidLocations[b][:a].count('#') > 0:
        total += 1
    if asteroidLocations[b][a + 1:].count('#') > 0:
        total += 1

    verticalLineOfSight = [location[b] for location in asteroids]
    if verticalLineOfSight[:b].count('#') > 0:
        total += 1
    if verticalLineOfSight[b + 1:].count('#') > 0:
        total += 1
    return total


def vaporizeDirectAsteroids(asteroidLocations, stationLocation, directionOfVaporizer):
    a = stationLocation[0]
    b = stationLocation[1]
    verticalLineOfSight = [location[b] for location in asteroids]
    toBeVaporized = False
    if directionOfVaporizer == 3 and '#' in asteroidLocations[a][:b]:
        thing = asteroidLocations[a][:b]
        toBeVaporized = (a, asteroidLocations[a][:b][::-1].index('#') + b - 1)
    if directionOfVaporizer == 1 and '#' in asteroidLocations[a][b + 1:]:
        thing = asteroidLocations[a][b + 1:]
        toBeVaporized = (a, asteroidLocations[a][b + 1:].index('#') + 1)
    if directionOfVaporizer == 0 and '#' in verticalLineOfSight[:a]:
        thing = verticalLineOfSight[:a]
        toBeVaporized = (a - verticalLineOfSight[:a][::-1].index('#') - 1, b)
    if directionOfVaporizer == 2 and '#' in verticalLineOfSight[a + 1:]:
        thing = verticalLineOfSight[a + 1:]
        toBeVaporized = (verticalLineOfSight[a + 1:].index('#') + a + 1, b)
    if toBeVaporized != False:
        asteroidLocations[toBeVaporized[0]][toBeVaporized[1]] = 'x'
        print((toBeVaporized[0], toBeVaporized[1]))
        prettyPrintMatrix(asteroidLocations)


def sortSlopesForQuadrant(slopes, quadrant):
    if quadrant == 0:
        return sorted(slopes)[::-1]
    if quadrant == 1:
        return sorted(slopes)
    if quadrant == 2:
        return sorted(slopes[::-1])
    if quadrant == 3:
        return sorted(slopes)


def getSlope(a, b):
    return abs((a[0] - b[0]) / (a[1] - b[1]))


def getManhattanDistance(a, b):
    return abs(a[0] - b[0]) + abs(b[1] - a[1])


# possibleStationLocations = []
# for x, row in enumerate(asteroids):
#     for y, col in enumerate(row):
#         if asteroids[x][y] == '#':
#             possibleStationLocations.append((x, y))

# bestAsteroidVisibility = ((0, 0), 0)
# for position in possibleStationLocations:
#     asteroidCount = getDirectAsteroids(asteroids, position)
#     for quad in getQuadrants(asteroids, position):
#         slopes = []
#         for location in quad:
#             if location != position:
#                 slope = getSlope(position, location)
#                 if slope not in slopes:
#                     slopes.append(slope)
#         asteroidCount += len(slopes)
#     # print((position, asteroidCount))
#     if asteroidCount > bestAsteroidVisibility[1]:
#         bestAsteroidVisibility = (position, asteroidCount)

# print('Part 1: ', bestAsteroidVisibility)

lastVaporized = (0, 0)
station = (3, 8)

asteroidsBySlopeForAllQuadrants = []
for quad in getQuadrants(asteroids, station):
    # prettyPrintMatrix(quad)
    slopes = {}
    for location in quad:
        if location != station:
            slope = getSlope(location, station)
            if slope in slopes:
                slopes[slope].append(location)
            if slope not in slopes:
                slopes[slope] = [location]
    for slope in slopes.keys():
        slopes[slope] = sorted(
            slopes[slope], key=lambda x: getManhattanDistance(station, x))
    asteroidsBySlopeForAllQuadrants.append(slopes)
    # for slope in slopes:
    #     location = slope[1]
    #     asteroids[location[0]][location[1]] = 'x'
    #     lastVaporized = location
    #     print(lastVaporized)

for vaporizedAsteroid in range(0, 200):
    # prettyPrintMatrix(asteroids)
    for i, quad in enumerate(asteroidsBySlopeForAllQuadrants):
        vaporizeDirectAsteroids(
            asteroids, station, i % 4)

        slopes = sortSlopesForQuadrant(list(quad.keys()), i)
        for slope in slopes:
            location = quad[slope].pop(0)
            asteroids[location[0]][location[1]] = 'x'
            print(location)
            prettyPrintMatrix(asteroids)
            lastVaporized = location
            if quad[slope] == []:
                quad.pop(slope, None)

print('Part 2: ', lastVaporized, (lastVaporized[1] * 100) + lastVaporized[0])
