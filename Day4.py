
def isIncreasing(number):
    digits = list(str(number))
    digits.sort()
    numberSorted = int(''.join([num for num in digits]))
    return numberSorted == number


def containsAdjacentDuplicate(number):
    digits = [int(i) for i in list(str(number))]
    if len(set(digits)) == len(digits):
        return False
    lastSeen = (-1, -1)
    for i, digit in enumerate(digits):
        if digit != lastSeen[0]:
            if i - lastSeen[1] == 2:
                return True
            lastSeen = (digit, i)
    if len(digits) - lastSeen[1] == 2:
        return True
    return False


def containsAdjacentDuplicatePart1(number):
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

possiblePasswordsPart1 = [i for i in range(
    minimum, maximum + 1) if isIncreasing(i) and containsAdjacentDuplicatePart1(i)]

print('Part 1: ', len(possiblePasswordsPart1))
print('Part 2: ', len(possiblePasswords))
