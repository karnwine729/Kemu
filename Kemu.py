from fileinput import filename
import csv, sys
from pathlib import Path

from CttData import CttData
from PartParsing import PartParsing
from Filepaths import Filepaths

def getLines(filepath):
    lines = []
    try:
        with open(filepath, "r", encoding="UTF-8") as currentFile:
            for line in currentFile.readlines():
                lines.append(line)
    except FileNotFoundError:
        print(f"\033[93m[{filepath}] not found.\033[0m")
    except UnicodeDecodeError:
        print(f"\033[93mInvalid file format.\033[0m")
    return lines

def createCsv(filename, columnNames, rows):
    with open(filename, 'w', encoding="UTF-8", newline="") as csvfile:
        csvWriter = csv.writer(csvfile)
        csvWriter.writerow(columnNames)
        csvWriter.writerows(rows)

def getCsvData(filepath):
    if not Path(filepath).exists():
        print(f"ERROR: File \"{filepath}\" does not exist.")
        sys.exit()
    csvData = []
    with open(filepath) as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            csvData.append(row)
    return csvData

# gamedataPath = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Kerbal Space Program\\GameData"
gamedataPath = "C:\\Keith Testing\\common\\Kerbal Space Program\\GameData"
# gamedataPath = "/home/keith/kspTestingTmp/GameData"

# directoryName = "NearFutureAeronautics"
# directoryName = "FarFutureTechnologies"
directoryName = "Squad/Parts"
# directoryName = "SquadExpansion/MakingHistory/Parts"
# directoryName = "SquadExpansion/Serenity/Parts"

techTierData = getCsvData("kttTechTiers.csv")

filepaths = Filepaths(gamedataPath, directoryName)
cttPatchLines = getLines(filepaths.cttPatchFilepath)
cttPatchData = CttData(cttPatchLines)
cfgFilepaths = filepaths.cfgFilepaths
partCfgFilepaths = filepaths.partCfgFilepaths
print(partCfgFilepaths[150])
part150Dict = PartParsing.getPartDict(getLines(partCfgFilepaths[150]))

def printPartDict(partDict):
    for key, value in partDict.items():
        print(f"{key}: {value}")

printPartDict(part150Dict)





