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
    return partDict['PART']

import Kemu

testFile = "testPart.cfg"
partDict = getPartDict(Kemu.getLines(testFile))
test = list(partDict.values())
for item in test:
    print(type(item))

### SAMPLE TREE CODE ###
# root = {'name': 'Alice', 'children': [{'name': 'Bob', 'children':
# [{'name': 'Darya', 'children': []}]}, {'name': 'Caroline',
# 'children': [{'name': 'Eve', 'children': [{'name': 'Gonzalo',
# 'children': []}, {'name': 'Hadassah', 'children': []}]}, {'name': 'Fred', 'children': []}]}]}

# def findEightLetterName(node):
#     print(f" Visiting node {node['name']}...")

#     print(f" Checking if {node['name']} has eight letters...")
#     if len(node['name']) == 8:
#         return node['name']
    
#     if len(node['children']) > 0:
#         for child in node['children']:
#             result = findEightLetterName(child)
#             if result is not None:
#                 return result
#     return None

# print(f"Found an eight-letter name: {findEightLetterName(root)}")
