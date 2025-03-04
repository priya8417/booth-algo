import pdb

multiplicand = []  # List to store binary of multiplicand
multiplier = []  # List to store binary of multiplier
cycleCount = 0  # variable to maintain cycle count
Acc = []  # accumalator
lastBit = 0  # Last extra bit


# function to set the number of cycles equal to number of bits
def setCycleCount():
    global cycleCount, multiplicand
    cycleCount = len(multiplicand)


# function to initialize accumalator with 0's
def setAccumalator():
    i = 0
    while (i < len(multiplicand)):
        Acc.append(0)
        i += 1


# function to add 2 binary bits
def addBin(a, b):
    if (a == 0 and b == 0):
        return 0, 0
    if (a == 0 and b == 1):
        return 1, 0
    if (a == 1 and b == 0):
        return 1, 0
    if (a == 1 and b == 1):
        return 0, 1


# function to add 3 binary bits
def add3bin(a, b, c):
    if (a == 0 and b == 0 and c == 0):
        return 0, 0
    if (a == 0 and b == 1 and c == 0):
        return 1, 0
    if (a == 1 and b == 0 and c == 0):
        return 1, 0
    if (a == 1 and b == 1 and c == 0):
        return 0, 1

    if (a == 0 and b == 0 and c == 1):
        return 1, 0
    if (a == 0 and b == 1 and c == 1):
        return 0, 1
    if (a == 1 and b == 0 and c == 1):
        return 0, 1
    if (a == 1 and b == 1 and c == 1):
        return 1, 1


# function to perform 2's complement of a number
def get2Complement(numArr):
    tmpLen = len(numArr)
    i = 0
    while (i < tmpLen):
        if (numArr[i] == 0):
            numArr[i] = 1
        else:
            numArr[i] = 0
        i += 1

    numArr.reverse()
    i = 0
    tmp = 1
    while (i < tmpLen):
        bit, tmp = addBin(numArr[i], tmp)
        numArr[i] = bit
        if (tmp == 0):
            break
        i += 1

    numArr.reverse()
    return numArr


# function to get binary of a number
def getBinary(num, found):
    signedBin = []

    while (int(num) > 0):
        signedBin.append(int(num % 2))
        num = int(num / 2)

    signedBin.reverse()

    return signedBin


# function to add 2 binary numbers as lists
def addTwoBinaryList(numList1, numList2):
    carry = 0
    result = []
    ans = 0
    tmpNumList1 = numList1[::-1]
    tmpNumList2 = numList2[::-1]

    i = 0
    # pdb.set_trace()
    while (i < len(numList1)):
        ans, carry = add3bin(tmpNumList1[i], tmpNumList2[i], carry)
        result.append(ans)
        i += 1

    result.reverse()
    return result


# utility function to get input and convert it into form on which booth's algorithm can be applied
# take input of numbers
# convert them to binary numbers
# make the bits equal
# if any number is negative thend take its 2's complement
# insert an extra bit at begaining of the list
def getNumbers():
    global multiplier, multiplicand, checkMultiplicant, checkMultiplier

    print("enter the multiplicand")
    a = int(input())
    print("enter the multiplier")
    b = int(input())

    foundMultiplicant = False
    foundMultiplier = False

    if (a < 0):
        foundMultiplicant = True

    if (b < 0):
        foundMultiplier = True

    if (foundMultiplicant == True):
        a = a * -1

    if (foundMultiplier == True):
        b = b * -1

    multiplicand = getBinary(a, False)
    multiplier = getBinary(b, False)

    if (len(multiplier) > len(multiplicand)):
        i = 0
        tmp = len(multiplier) - len(multiplicand)
        while (i < tmp):
            multiplicand.insert(0, 0)
            i += 1

    elif (len(multiplicand) > len(multiplier)):
        i = 0
        tmp = len(multiplicand) - len(multiplier)
        while (i < tmp):
            multiplier.insert(0, 0)
            i += 1

    multiplicand.insert(0, 0)
    multiplier.insert(0, 0)

    if (foundMultiplicant == True):
        multiplicand = get2Complement(multiplicand)
    if (foundMultiplier == True):
        multiplier = get2Complement(multiplier)


# utility function to perform arithmetic right shift
def arithmeticShiftRight():
    global multiplier, Acc, lastBit
    lastBit = multiplier[-1]

    tmpBit = Acc[-1]

    tmpMultiplier = []
    tmpAcc = []

    for val in multiplier:
        tmpMultiplier.append(val)

    for val in Acc:
        tmpAcc.append(val)

    i = 0
    j = 0
    while (i < len(Acc)):

        if (i == 0):
            i += 1
            continue

        Acc[i] = tmpAcc[j]
        i += 1
        j += 1

    i = 0
    j = 0

    while (i < len(multiplier)):
        if (i == 0):
            multiplier[i] = tmpBit
            i += 1
            continue
        multiplier[i] = tmpMultiplier[j]
        i += 1
        j += 1


# function to convert binary number to decimal
def getNumberFromBinaryList(answer):
    intAnswer = 0;
    tmpAnswer = []
    for val in answer:
        tmpAnswer.append(val)

    tmpAnswer.reverse()
    i = 0
    while (i <= (len(answer) - 2)):
        tmp = tmpAnswer[i] * int(pow(2, i))
        intAnswer = intAnswer + tmp
        i += 1

    intAnswer = intAnswer - (tmpAnswer[-1] * (int(pow(2, i))))
    return intAnswer


# helper function to convert list to string
def convertToStr(lst):
    string = ""

    for val in lst:
        string += str(val)

    return string


# Main Booth's algorithm
def BoothAlgorithm():
    global multiplicand, multiplier, Acc, cycleCount, lastBit
    fileString = "result.txt"  # file in which the result will be stored

    fileObj = open(fileString, 'w')  # file operation to open the file

    getNumbers()  # calling getNumber() method
    setCycleCount()  # setting number of cycles
    setAccumalator()  # setting accumalator contents to 0

    multiplicandComplement = multiplicand[::1]
    multiplicandComplement = get2Complement(multiplicandComplement)
    count = 1
    print()
    print()

    # Loop to keep the cycle count
    while (cycleCount != 0):
        secondLastBit = multiplier[-1]
        print(count)
        count += 1

        # CASE-1: when the last bit of the multiplier is 1 and the extra bit is 0 (1 0 case)
        # add the accumalator contents to 2's complement of multiplicant and store the result in accumalator
        # perform a right shift after that
        if (secondLastBit == 1 and lastBit == 0):
            Acc = addTwoBinaryList(Acc, multiplicandComplement)
            tmpStr = convertToStr(Acc) + "			" + convertToStr(multiplier) + "			" + str(lastBit)
            print(tmpStr)
            fileObj.write(tmpStr)
            fileObj.write('\n')

        # CASE-2: when the last bit of the multiplier is 0 and the extra bit is 1 (0 1 case)
        # add the accumalator contents to multiplicant and store the result in accumalator
        # perform a right shift after that
        if (secondLastBit == 0 and lastBit == 1):
            Acc = addTwoBinaryList(Acc, multiplicand)
            tmpStr = convertToStr(Acc) + "			" + convertToStr(multiplier) + "			" + str(lastBit)
            print(tmpStr)
            fileObj.write(tmpStr)
            fileObj.write('\n')

        # CASE-3: when the last bit of the multiplier is 0 and the extra bit is 0 (0 0 case)
        # or the last bit of the multiplier is 1 and the extra bit is 1 (1 1 case)
        # perform a right shift
        arithmeticShiftRight()

        tmpStr = convertToStr(Acc) + "			" + convertToStr(multiplier) + "			" + str(lastBit)
        print(tmpStr)
        fileObj.write(tmpStr)
        fileObj.write('\n')
        fileObj.write('\n')
        print()

        cycleCount = cycleCount - 1

    # Answer is the combined list of Accumalator and multiplier
    answer = []
    answer = Acc + multiplier
    fileObj.write('\n')
    fileObj.write('\n')
    print()
    print()

    print("product with signed magnitude is:   ")
    print(*answer, sep="")

    fileObj.write("product with signed magnitude is:   ")
    fileObj.write(convertToStr(answer))
    fileObj.write('\n')

    print("answer in integer format")
    num = getNumberFromBinaryList(answer)
    print(num)

    fileObj.write("answer in integer format:     ")
    fileObj.write(str(num))
    fileObj.write('\n')
    fileObj.close()


BoothAlgorithm()