import itertools
import re
from pathlib import Path
import numpy as np

class Moon:
    def __init__(self, positions):
        self.positions = [int(position) for position in positions]
        self.initialState = [int(position) for position in positions]
        self.velocities = [0, 0, 0]
        
    def __str__(self):
        return f'Positions: {self.positions} Velocities: {self.velocities}'

    def calculateGravity(self, nearbyMoon):
        for index in range(len(self.positions)):
            # this could definitely be more elegant
            if self.positions[index] == nearbyMoon.positions[index]:
                continue
            if self.positions[index] < nearbyMoon.positions[index]:
                self.velocities[index] += 1
                nearbyMoon.velocities[index] -= 1
            else:
                self.velocities[index] -= 1
                nearbyMoon.velocities[index] += 1
    
    def calculateGravityAtIndex(self, nearbyMoon, index):
        # this could definitely be more elegant
        if self.positions[index] == nearbyMoon.positions[index]:
            return
        if self.positions[index] < nearbyMoon.positions[index]:
            self.velocities[index] += 1
            nearbyMoon.velocities[index] -= 1
        else:
            self.velocities[index] -= 1
            nearbyMoon.velocities[index] += 1
          
    def updatePosition(self):
        self.positions = [position + velocity for position, velocity in zip(self.positions,self.velocities)]      
   
    def updatePositionAtIndex(self, index):
        self.positions[index] = self.positions[index] + self.velocities[index]      
   
    def calculatePotentialEnergy(self):
        return sum([abs(position) for position in self.positions])

    def calculateKineticEnergy(self):
        return sum([abs(velocity) for velocity in self.velocities])
    
    def getTotalEnergy(self):
        return self.calculatePotentialEnergy() * self.calculateKineticEnergy()
    
    def atInitialState(self, axis):
        if self.positions[axis] == self.initialState[axis] and self.velocities[axis] == 0:
            return True
        else:
            return False
        
def printMoons(moons):
    for moon in moons:
        print(f'{moon}')
  
def getMoonPairings(moons):
    moonPermutations = list(itertools.permutations([0, 1, 2, 3], 2))
    moonPairings = []
    for moonPermutation in moonPermutations:
        if (moons[moonPermutation[1]], moons[moonPermutation[0]]) not in moonPairings:
            moonPairings.append((moons[moonPermutation[0]], moons[moonPermutation[1]])) 
    return moonPairings
      
def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)
           
data_folder = Path("./PuzzleData/")
file_to_open = data_folder / "Day12.txt"
with open(file_to_open) as moonData:
    moons = [Moon(re.sub('[<> =xyz]', '' ,planet.strip()).split(','))for planet in moonData.readlines()]

originalMoons = [moon for moon in moons]   

moonPairings = getMoonPairings(moons) 
        
# steps = 1000
# print(f'Step 0:')
# printMoons(moons)

# for i in range(steps):
#     for moonPair in moonPairings:
#         moonPair[0].calculateGravity(moonPair[1]) 
        
#     for moon in moons:
#         moon.updatePosition() 
#     print(f'Step {i + 1}:')
#     printMoons(moons)

# # potential = [moon.calculatePotentialEnergy() for moon in moons]
# # kinetic = [moon.calculateKineticEnergy() for moon in moons]

# totalEnergy = sum([moon.getTotalEnergy() for moon in moons])

# print('Part 1:', totalEnergy)

# reset moons
# get all moons x values to be at start

stepsTillRepeat = [0, 0, 0]
for axis in [0,1, 2]:
    i = 0
    moons = originalMoons
    moonPairings = getMoonPairings(moons)
    while True:
        for moonPair in moonPairings:
            moonPair[0].calculateGravityAtIndex(moonPair[1], axis) 
        for moon in moons:
            moon.updatePositionAtIndex(axis) 
        if all([moon.atInitialState(axis) for moon in moons]):
            stepsTillRepeat[axis] = i + 1
            break
        i += 1
        
print('Part 2:', np.lcm.reduce(stepsTillRepeat))
