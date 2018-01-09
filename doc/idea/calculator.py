from random import randint

class calculator:
    __sourcePaths = []
    __rngTuples = [()]

    def __init__(self):
        print("This is a constructor\n")

    def __del__(self):
        print("This is a destructor\n")

    def calcTuples(self):
        amountTuples = randint(2, 6)
        rngFrame = 0

        for cnt in range(0, amountTuples):
            rngClip = randint(0, amountTuples)
            rngFrame += randint(30, 150)
            self.__rngTuples.append((rngClip, rngFrame))

        for cnt in range(1, amountTuples):
            print(self.__rngTuples[cnt])

Test = calculator()
Test.calcTuples()