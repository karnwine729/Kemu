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

def getPartDict(lines):
    linesGenerator = (line for line in lines)
    partDict = getPartDictRecursively(linesGenerator)
    try:
        return partDict["PART"]
    except KeyError:
        return partDict["\ufeffPART"]

import Kemu

# testFile = "testPart.cfg"
testFile = "/home/keith/kspTestingTmp/GameData/Squad/Parts/Engine/jetEngines/jetEngineTurbo.cfg"
partDict = getPartDict(Kemu.getLines(testFile))

def getValueFromKey(keyName, partDict):
    for key, value in partDict.items():
        if key == keyName:
            return value
        elif isinstance(value, dict):
            result = getValueFromKey(keyName, value)
            if result is not None:
                return result
    return None

value = getValueFromKey("velCurve", partDict)
print(value)
