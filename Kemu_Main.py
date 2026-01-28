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

cr = CfgReader(directoryName)
partFiles = cr.getPartCfgFiles()
partFile = partFiles[149]
partData = cr.getLines(partFile)
part = Engine(partFile, partData)
part.printSpecs()
