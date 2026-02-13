def parseLine(line):
    key = line.split("=")[0].strip()
    value = line.split("=")[1].strip()
    value = value.split("//")[0].strip()
    return key, value

def getKeyInNest(lastNonEmptyLine, partDict):
    key = ""
    if lastNonEmptyLine in partDict:
        count = len([key for key in partDict.keys() if key.startswith(lastNonEmptyLine)])
        key = f"{lastNonEmptyLine}_{count}"
    else:
        key = lastNonEmptyLine
    return key

def getPartDictRecursively(lines):
    partDict = {}
    lastNonEmptyLine = ""
    for line in lines:
        if "{" in line:
            nest = getPartDictRecursively(lines)
            key = getKeyInNest(lastNonEmptyLine, partDict)
            partDict[key] = nest
        elif "}" in line:
            break
        elif line.startswith("//"):
            continue
        elif "=" in line:
            key, value = parseLine(line)
            partDict[key] = value
        else:
            lastNonEmptyLine = line
    return partDict

def getPartDict(lines):
    generatedLines = (line for line in lines)
    return getPartDictRecursively(generatedLines)

import Kemu

testFile = "testPart.cfg"
partDict = getPartDict(Kemu.getLines(testFile))
