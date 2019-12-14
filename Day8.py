from pathlib import Path

data_folder = Path("./PuzzleData/")
file_to_open = data_folder / "Day8.txt"
with open(file_to_open) as input:
    pixels = [int(pixel.strip()) for pixel in input.read()]

def getLayers(pixels, width, height):
    layerSize = width * height
    return [pixels[x:x+layerSize] for x in range(0, len(pixels), layerSize)]

width = 25
height = 6

layers = getLayers(pixels, width, height)
zeroCount = (layers[0].count(0),layers[0])
for layer in layers:
    zeros = layer.count(0)
    if zeros < zeroCount[0]:
        zeroCount = (zeros, layer)

print('Part 1: ',zeroCount[1].count(1) * zeroCount[1].count(2))

finalImage = layers.pop(0)

for index, pixel in enumerate(finalImage):
    currentPixel = pixel
    while currentPixel == 2:
        for layer in layers:
            currentPixel = layer[index]
            if currentPixel != 2:
                break
            
    finalImage[index] = currentPixel
    
a = [finalImage[x:x+25] for x in range(0, int(len(finalImage)), 25)]

print('Part 2:')
for row in a:
    print(' '.join([str('*' if pixel == 1 else ' ') for pixel in row]))

