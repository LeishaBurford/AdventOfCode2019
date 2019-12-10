
def isIncreasing(number):
    digits = list(str(number))
    digits.sort()
    numberSorted = int(''.join([num for num in digits]))
    return numberSorted == number


def containsAdjacentDuplicate(number):
    digits = list(str(number))
    if len(set(digits)) == len(digits):
        return False
    for i in range(0, len(digits) - 1):
        if digits[i] == digits[i + 1]:
            return True
    return False


minimum = 134792
maximum = 675810

possiblePasswords = [i for i in range(
    minimum, maximum + 1) if isIncreasing(i) and containsAdjacentDuplicate(i)]

print('Part 1: ', len(possiblePasswords))
