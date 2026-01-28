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

def printAllPartStats(parts):
    for part in parts:
        part.printSpecs()    

cr = CfgReader(directoryName)
partFiles = cr.getPartCfgFiles()
##partFile = partFiles[149]
##partData = cr.getLines(partFile)
##part = Engine(partFile, partData)
##part.printSpecs()
parts = getParts(partFiles)
printAllPartStats(parts)
