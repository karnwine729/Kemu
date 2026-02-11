from CttData import CttData
from Filepaths import Filepaths

def getLines(filepath):
    if filepath == None:
        return None
    lines = []
    with open(filepath, 'r', encoding="UTF-8") as currentFile:
        for line in currentFile.readlines():
            lines.append(line.strip())
    return lines

# gamedataPath = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Kerbal Space Program\\GameData"
gamedataPath = "C:\\Keith Testing\\common\\Kerbal Space Program\\GameData"
# gamedataPath = "/home/keith/kspTestingTmp/GameData"

# directoryName = "NearFutureAeronautics"
directoryName = "FarFutureTechnologies"
# directoryName = "Squad/Parts"
# directoryName = "SquadExpansion/MakingHistory/Parts"
# directoryName = "SquadExpansion/Serenity/Parts"

nfaFilepaths = Filepaths(gamedataPath, directoryName)
nfaCttPatchLines = getLines(nfaFilepaths.cttPatchFilepath)
nfaCttPatchData = CttData(nfaCttPatchLines)
print(nfaCttPatchData)