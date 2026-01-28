import sys, os
from pathlib import Path

class CfgReader:
    #gamedataPath = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Kerbal Space Program\\GameData"
    gamedataPath = "C:\\Keith Testing\\common\\Kerbal Space Program\\GameData"
    #gamedataPath = "/home/keith/kspTestingTmp/GameData"

    #localizationPath = Path(fullPath) / Path("Localization/en-us.cfg")
    localizationPath = Path(gamedataPath) / Path("Squad/Localization/dictionary.cfg")
    #localizationPath = Path(gamedataPath) / Path("SquadExpansion/Serenity/Localization/dictionary.cfg")

    def __init__(self, directoryName):
        self.directoryName = directoryName
        self.fullPath = Path(CfgReader.gamedataPath) / Path(directoryName)

    def validatePaths(self):
        if not self.fullPath.exists():
            print("File path does not exist.")
            sys.exit()
        if not self.localizationPath.exists():
            print("Could not find localization file.")
            sys.exit()

    def getCfgFiles(self):
        self.validatePaths()
        cfgFiles = []
        for root, dirs, files in os.walk(self.fullPath):
            for file in files:
                if ".cfg" in file:
                    cfgFiles.append(os.path.join(root,file))
        if not cfgFiles:
            print("No .cfg files found in directory.")
            sys.exit()
        return cfgFiles

    @staticmethod
    def getLines(file):
        lines = []
        with open(file, 'r', encoding="UTF-8") as currentFile:
            for line in currentFile.readlines():
                lines.append(line.strip())
        return lines

    def getPartCfgFiles(self):
        partCfgFiles = []
        cfgFiles = self.getCfgFiles()
        for file in cfgFiles:
            lines = CfgReader.getLines(file)
            if not CfgReader.isPart(lines):
                continue
            if CfgReader.isDeprecated(lines):
                continue
            partCfgFiles.append(file)
        return partCfgFiles

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
    def lookupLocalization(localizationText):
        lines = CfgReader.getLines(CfgReader.localizationPath)
        for line in lines:
            if localizationText in line:
                line = line.split("=")[1]
                return line.split("//")[0].strip()
        return "LOCALIZATION DATA NOT FOUND"

    ### PART CHECKS ###

    @staticmethod
    def partCheck(lines, searchTerm):
        for line in lines:
            line = "".join(line.split())
            if searchTerm in line:
                return True
        return False

    @staticmethod
    def isPart(lines):
        return CfgReader.partCheck(lines, "module=Part")

    @staticmethod
    def isDeprecated(lines):
        return CfgReader.partCheck(lines, "TechHidden=True")

    @staticmethod
    def isEngine(lines):
        return CfgReader.partCheck(lines, "category=Engine")

    @staticmethod
    def isTank(lines):
        return CfgReader.partCheck(lines, "category=Tank")

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
