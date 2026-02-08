from Kemu_CfgReader import CfgReader
from Kemu_CfgWriter import CfgWriter
from Kemu_CsvWriter import CsvWriter
from Kemu_CsvReader import CsvReader
from Kemu_Part import Part
from Kemu_Engine import Engine
from Kemu_FuelTank import FuelTank

techTierData = CsvReader.getTechTreeTierData()


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


def updatePartsForCommunityTechTree(parts, communityTechTreeCfgFilepath):
    for part in parts:
        part.updateForCommunityTechTree(communityTechTreeCfgFilepath)


nfaPartFilepaths = CfgReader.getPartCfgFilepaths("NearFutureAeronautics")
nfaCttPatchFilepath = CfgReader.getCommunityTechTreePatchFilepath(
    "NearFutureAeronautics"
)
nfaParts = getParts(nfaPartFilepaths)
updatePartsForCommunityTechTree(nfaParts, nfaCttPatchFilepath)
CsvWriter.createDataDumpCsv(nfaParts)
# CsvWriter.createCsvForTechTreePatches(nfaParts, techTierData)
CfgWriter.createTechTreePatch(nfaParts, techTierData)


fftPartFilepaths = CfgReader.getPartCfgFilepaths("FarFutureTechnologies")
fftCttPatchFilepath = CfgReader.getCommunityTechTreePatchFilepath(
    "FarFutureTechnologies"
)
fftParts = getParts(fftPartFilepaths)
updatePartsForCommunityTechTree(fftParts, fftCttPatchFilepath)
# CsvWriter.createCsvForTechTreePatches(fftParts, techTierData)
CfgWriter.createTechTreePatch(fftParts, techTierData)

# stockPartFilepaths = CfgReader.getPartCfgFilepaths("Squad/Parts")
# stockParts = getParts(stockPartFilepaths)
# CsvWriter.createCsvForTechTreePatches(stockParts, techTierData)

# makingHistoryPartFilepaths = CfgReader.getPartCfgFilepaths("SquadExpansion/MakingHistory/Parts")
# expansionParts = getParts(makingHistoryPartFilepaths)
# CsvWriter.createCsvForTechTreePatches(expansionParts, techTierData)

# breakingGroundPartFilepaths = CfgReader.getPartCfgFilepaths("SquadExpansion/Serenity/Parts")
# breakingGroundParts = getParts(breakingGroundPartFilepaths)
# CsvWriter.createCsvForTechTreePatches(breakingGroundParts, techTierData)
