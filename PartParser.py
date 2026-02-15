def parseLine(line):
    key = line.split("=")[0].strip()
    value = line.split("=")[1].strip()
    value = value.split("//")[0].strip()
    return key, value

def getKeyName(keyName, partDict):
    if keyName not in partDict:
        return keyName
    keyCount = len([key for key in partDict.keys() if key.startswith(keyName)]) + 1
    return f"{keyName}_{keyCount}"

def getPartDictRecursively(lines):
    partDict = {}
    lastPotentialNodeName = ""
    for line in lines:
        if line.startswith("//") or line.strip() == "":
            continue
        elif "{" in line:
            node = getPartDictRecursively(lines)
            nodeName = getKeyName(lastPotentialNodeName, partDict)
            partDict[nodeName] = node
        elif "}" in line:
            break
        elif "=" in line:
            key, value = parseLine(line)
            key = getKeyName(key, partDict)
            partDict[key] = value
        else:
            lastPotentialNodeName = line.strip()
    return partDict

def getPartDictGenerator(lines):
    linesGenerator = (line for line in lines)
    return getPartDictRecursively(linesGenerator)

def getPartDict(lines):
    partDict = getPartDictGenerator(lines)
    return partDict['PART']

import Kemu

testFile = "testPart.cfg"
partDict = getPartDict(Kemu.getLines(testFile))
print(partDict)
