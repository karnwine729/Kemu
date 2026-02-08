import sys, os
from pathlib import Path

class CfgReader:

    # gamedataPath = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Kerbal Space Program\\GameData"
    # gamedataPath = "C:\\Keith Testing\\common\\Kerbal Space Program\\GameData"
    gamedataPath = "/home/keith/kspTestingTmp/GameData"

    localizationPath = Path()

    @classmethod
    def getLocalizationPath(cls, fullPath, directoryName):
        if directoryName == "Squad/Parts" or directoryName == "SquadExpansion/MakingHistory/Parts":
            cls.localizationPath = Path(cls.gamedataPath) / Path("Squad/Localization/dictionary.cfg")
        elif directoryName == "SquadExpansion/Serenity/Parts":
            cls.localizationPath = Path(cls.gamedataPath) / Path("SquadExpansion/Serenity/Localization/dictionary.cfg")
        else:
            cls.localizationPath = fullPath / Path("Localization/en-us.cfg")

    @classmethod
    def validatePaths(cls, directoryName):
        fullPath = Path(cls.gamedataPath) / Path(directoryName)
        if not fullPath.exists():
            print("File path does not exist.")
            sys.exit()
        cls.getLocalizationPath(fullPath, directoryName)
        if cls.localizationPath == Path():
            print("Could not find localization file.")
            sys.exit()
        return fullPath

    @classmethod
    def getCfgFilepaths(cls, directoryName):
        fullPath = cls.validatePaths(directoryName)
        cfgFilepaths = []
        for root, dirs, files in os.walk(fullPath):
            for file in files:
                if ".cfg" in file:
                    cfgFilepaths.append(os.path.join(root,file))
        if not cfgFilepaths:
            print("No .cfg files found in directory.")
            sys.exit()
        return cfgFilepaths

    @staticmethod
    def getLines(filepath):
        lines = []
        with open(filepath, 'r', encoding="UTF-8") as currentFile:
            for line in currentFile.readlines():
                lines.append(line.strip())
        return lines

    @classmethod
    def getPartCfgFilepaths(cls, directoryName):
        partCfgFilepaths = []
        cfgFilepaths = cls.getCfgFilepaths(directoryName)
        for filepath in cfgFilepaths:
            lines = CfgReader.getLines(filepath)
            if not CfgReader.isPart(lines):
                continue
            if CfgReader.isHidden(lines):
                continue
            partCfgFilepaths.append(filepath)
        return partCfgFilepaths

    @classmethod
    def getCommunityTechTreePatchFilepath(cls, directoryName):
        cfgFilepaths = cls.getCfgFilepaths(directoryName)
        for filepath in cfgFilepaths:
            lines = CfgReader.getLines(filepath)
            if CfgReader.checkForSearchTerm(lines, "NEEDS[CommunityTechTree]"):
                return filepath
        return ""

    @staticmethod
    def locateTextLine(lines, startingLine, searchTerm):
        for lineNumber, lineText in enumerate(lines[startingLine:], startingLine):
            if searchTerm in lineText:
                return lineNumber + 1
        return -1

    @staticmethod
    def locateTextBlock(lines, startingLine, startingSearchTerm, endingSearchTerm):
        searchTermFound = False
        nextStartingLine = 0
        endingLine = 0
        for lineNumber, lineText in enumerate(lines[startingLine:], startingLine):
            if startingSearchTerm in lineText:
                nextStartingLine = lineNumber + 1
                searchTermFound = True
                continue
            if searchTermFound:
                if endingSearchTerm in lineText:
                    endingLine = lineNumber + 1
                    break
        return [nextStartingLine, endingLine]

    @staticmethod
    def locateTextBlockLoop(lines, startingLine, startingSearchTerm, endingSearchTerm):
        nextStartingLine = startingLine
        lineNumbers = []
        while nextStartingLine < len(lines):
            numbers = CfgReader.locateTextBlock(lines, nextStartingLine, startingSearchTerm, endingSearchTerm)
            if numbers == [0,0]:
                break
            lineNumbers.append(numbers)
            nextStartingLine = numbers[1]
        return lineNumbers

    @staticmethod
    def lookupLocalization(localizationText):
        lines = CfgReader.getLines(CfgReader.localizationPath)
        for line in lines:
            if localizationText in line:
                line = line.split("=")[1]
                return line.split("//")[0].strip()
        return "LOCALIZATION DATA NOT FOUND"

    ### PART CHECKS ###

    @staticmethod
    def checkForSearchTerm(lines, searchTerm):
        searchTerm = searchTerm.lower()
        for line in lines:
            line = "".join(line.split())
            line = line.lower()
            if searchTerm in line:
                return True
        return False

    @staticmethod
    def isPart(lines):
        return CfgReader.checkForSearchTerm(lines, "module=Part")

    @staticmethod
    def isHidden(lines):
        return CfgReader.checkForSearchTerm(lines, "TechHidden=True") or CfgReader.checkForSearchTerm(lines, "TechRequired=Unresearcheable")

    @staticmethod
    def isJetEngine(lines):
        return CfgReader.checkForSearchTerm(lines, "velCurve")

    @staticmethod
    def isEngine(lines):
        return CfgReader.checkForSearchTerm(lines, "maxThrust")

    @staticmethod
    def isFuelTank(lines):
        return CfgReader.checkForSearchTerm(lines, "category=FuelTank") or CfgReader.checkForSearchTerm(lines, "category=Propulsion")

    ### GET VALUES ###

    @staticmethod
    def getValuesFromSearchTerm(lines, searchTerm):
        for line in lines:
            if searchTerm in line:
                line = line.split("=")[1]
                line = line.split("//")[0].strip()
                line = line.split(",")
                if len(line) == 1:
                    return line[0]
                return line
        return searchTerm.upper() + " NOT FOUND"

    @staticmethod
    def getValuesFromLineNumber(lines, lineNumber):
        line = lines[lineNumber - 1].split("=")[1]
        line = line.split("//")[0].strip()
        line = line.split(",")
        if len(line) == 1:
            return line[0]
        return line

    @staticmethod
    def getValuesFromTextBlock(lines, searchTerm, startingLine, endingLine):
        for x in range(startingLine, endingLine):
            if searchTerm in lines[x]:
                line = lines[x].split("=")[1]
                line = line.split("//")[0].strip()
                return line
        return searchTerm.upper() + " NOT FOUND"
