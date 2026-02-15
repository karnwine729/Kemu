def parseLine(line):
    key = line.split("=")[0].strip()
    value = line.split("=")[1].strip()
    value = value.split("//")[0].strip()
    return key, value

def getNodeName(lastPotentialNodeName, partDict):
    nodeName = ""
    if lastPotentialNodeName not in partDict:
        return lastPotentialNodeName
    nodeNameCount = len([nodeName for nodeName in partDict.keys() if nodeName.startswith(lastPotentialNodeName)])
    return f"{lastPotentialNodeName}_{nodeNameCount}"

def getPartDictRecursively(lines):
    partDict = {}
    lastPotentialNodeName = ""
    for line in lines:
        if line.startswith("//"):
            continue
        elif "{" in line:
            node = getPartDictRecursively(lines)
            nodeName = getNodeName(lastPotentialNodeName, partDict)
            partDict[nodeName] = node
        elif "}" in line:
            break
        elif "=" in line:
            key, value = parseLine(line)
            partDict[key] = value
        else:
            lastPotentialNodeName = line.strip()
    return partDict

def getPartDict(lines):
    linesGenerator = (line for line in lines)
    return getPartDictRecursively(linesGenerator)

import Kemu

testFile = "testPart.cfg"
partDict = getPartDict(Kemu.getLines(testFile))
for key, value in partDict.items():
    for subKey, subValue in value.items():
        print(f"{subKey}: {subValue}")

