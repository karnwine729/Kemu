import os, sys
from pathlib import Path
from Kemu_CfgReader import CfgReader
from Kemu_Part import Part
from Kemu_Engine import Engine

#directoryName = "FarFutureTechnologies"
#directoryName = "NearFutureAeronautics"
directoryName = "Squad/Parts"
#directoryName = "SquadExpansion/MakingHistory/Parts"
#directoryName = "SquadExpansion/Serenity/Parts"

def getParts(partFiles):
    parts = []
    for file in partFiles:
        partData = cr.getLines(file)
        if CfgReader.isEngine(partData):
            parts.append(Engine(file, partData))
    return parts

def printPartTitles(parts):
    i = 0
    for part in parts:
        print("[" + str(i) + "]", end=" ")
        print(part)
        i += 1
        
def printFullPartSpecs(parts, startingPartNum, endingPartNum):
    for x in range(startingPartNum, endingPartNum + 1):
        parts[x].printSpecs()
        print()

cr = CfgReader(directoryName)
partFiles = cr.getPartCfgFiles()
engines = getParts(partFiles)
printPartTitles(engines)



