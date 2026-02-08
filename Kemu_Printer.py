import sys
from Kemu_Part import Part
from Kemu_Engine import Engine
from Kemu_FuelTank import FuelTank

class Printer:

    @staticmethod
    def printAllPartTitles(parts):
        i = 0
        for part in parts:
            print(f"{[i]} {part}")
            i += 1

    @staticmethod
    def printResources(part):
        if isinstance(part.resources, str):
            print(f"Base Volume:\t{part.resources}")
        else:
            for x in range(0, len(part.resources), 2):
                if part.resources[x] == "Ore":
                    part.resources[x] = "Ore Capacity"
                print(f"{part.resources[x]}:\t\t{part.resources[x+1]}")

    @staticmethod
    def printBasicPartSpecs(part):
        print(part.filePath)
        print(f"Title:\t\t\t{part.title}")
        print(f"Mod:\t\t\t{part.mod}")
        print(f"Category:\t\t{part.category}")
        print(f"Code Name:\t\t{part.name}")
        print(f"Cost:\t\t\t{part.cost}")
        print(f"Size:\t\t\t{part.size}")
        print(f"Tech:\t\t\t{part.tech}")
        if not part.resources == None:
            Printer.printResources(part)

    @staticmethod
    def printEngineSpecsForSingleModeEngine(part):
        print(f"Max Thrust:\t\t{part.engineSpecs[0]} kN")
        print(f"Vac Isp:\t\t{part.engineSpecs[1]} s")

    @staticmethod
    def printEngineSpecsForMultiModeEngine(part):
        num = 1
        index = 0
        while num < len(part.engineSpecs) - 1:
            print(f"Max Thrust {num}:\t{part.engineSpecs[index]} kN")
            index += 1
            print(f"Vac Isp {num}:\t\t{part.engineSpecs[index]} s")
            index += 1
            num += 1

    @staticmethod
    def printEngineSpecs(part):
        Printer.printBasicPartSpecs(part)
        print(f"Gimbal Range:\t\t{part.gimbal} deg")
        if len(part.engineSpecs) == 2:
            Printer.printEngineSpecsForSingleModeEngine(part)
        else:
            Printer.printEngineSpecsForMultiModeEngine(part)

    @staticmethod
    def printFuelTankSpecs(part):
        Printer.printBasicPartSpecs(part)

    @staticmethod
    def printPartSpecs(part):
        if type(part) is Part:
            Printer.printBasicPartSpecs(part)
        elif type(part) is Engine:
            Printer.printEngineSpecs(part)
        elif type(part) is FuelTank:
            Printer.printFuelTankSpecs(part)

    @staticmethod
    def printPartSpecsRange(parts, startingPartNum, endingPartNum):
        if startingPartNum > endingPartNum:
            swap = startingPartNum
            startingPartNum = endingPartNum
            endingPartNum = swap
        if startingPartNum >= len(parts):
            print("Starting Part Number is out of range.")
            sys.exit()
        if endingPartNum >= len(parts):
            print("Ending Part Number is out of range.")
            sys.exit()
        for x in range(startingPartNum, endingPartNum + 1):
            Printer.printPartSpecs(parts[x])
            print()
