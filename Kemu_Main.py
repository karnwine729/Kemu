from Kemu_CfgReader import CfgReader
from Kemu_CsvWriter import CsvWriter
from Kemu_CsvReader import CsvReader
from Kemu_Part import Part
from Kemu_Engine import Engine
from Kemu_FuelTank import FuelTank
from Kemu_TechTreeModding import TechTreeModding

def getParts(partCfgFilepaths):
    parts = []
    for filepath in partCfgFilepaths:
        partCfgFileLines = CfgReader.getLines(filepath)
        if CfgReader.isEngine(partCfgFileLines):
            parts.append(Engine(filepath, partCfgFileLines))
            continue
        if CfgReader.isFuelTank(partCfgFileLines):
            parts.append(FuelTank(filepath, partCfgFileLines))
            continue
        parts.append(Part(filepath, partCfgFileLines))
    return parts

def createTechTreeCsv(directoryName):
    partFilepaths = CfgReader.getPartCfgFilepaths(directoryName)
    cttPatchFilepath = CfgReader.getCommunityTechTreePatchFilepath(directoryName)
    parts = getParts(partFilepaths)
    TechTreeModding.updatePartsForCommunityTechTree(parts, cttPatchFilepath)
    TechTreeModding.createCsvForTechTreePatches(parts)
    print(f"Created {directoryName} CSV for Tech Tree Patches")

createTechTreeCsv("NearFutureAeronautics")

# CfgWriter.createTechTreePatch(nfaParts, techTierData)


# fftPartFilepaths = CfgReader.getPartCfgFilepaths("FarFutureTechnologies")
# fftCttPatchFilepath = CfgReader.getCommunityTechTreePatchFilepath("FarFutureTechnologies")
# fftParts = getParts(fftPartFilepaths)
# updatePartsForCommunityTechTree(fftParts, fftCttPatchFilepath)
# # CsvWriter.createCsvForTechTreePatches(fftParts, techTierData)
# CfgWriter.createTechTreePatch(fftParts, techTierData)

# stockPartFilepaths = CfgReader.getPartCfgFilepaths("Squad/Parts")
# stockParts = getParts(stockPartFilepaths)
# CsvWriter.createCsvForTechTreePatches(stockParts, techTierData)

# makingHistoryPartFilepaths = CfgReader.getPartCfgFilepaths("SquadExpansion/MakingHistory/Parts")
# expansionParts = getParts(makingHistoryPartFilepaths)
# CsvWriter.createCsvForTechTreePatches(expansionParts, techTierData)

# breakingGroundPartFilepaths = CfgReader.getPartCfgFilepaths("SquadExpansion/Serenity/Parts")
# breakingGroundParts = getParts(breakingGroundPartFilepaths)
# CsvWriter.createCsvForTechTreePatches(breakingGroundParts, techTierData)
