class CttData:

    def __init__(self, cttPatchLines):
        self.cttPatchData = self.getCttPatchData(cttPatchLines)

    def __str__(self):
        cttDataPrint = ""
        for part, tech in self.cttPatchData.items():
            cttDataPrint += f"{part}: {tech}\n"
        return cttDataPrint

    def getPartInCttPatch(self, lines, startingLine):
        for line in lines[startingLine:]:
            if "@PART" in line:
                line = line.split(":")[0]
                line = line.split("]")[0]
                line = line.split("[")[1]
                return line

    def getTechInCttPatch(self, lines, startingLine):
        for line in lines[startingLine:]:
            if "@TechRequired" in line:
                line = line.split("=")[1]
                line = line.split("//")[0].strip()
                return line

    def getCttPatchData(self, cttPatchLines):
        if cttPatchLines == None:
            return None
        cttPatchData = {}
        lineNumber = 0
        for line in cttPatchLines:
            if "@PART" in line:
                part = self.getPartInCttPatch(cttPatchLines, lineNumber)
                tech = self.getTechInCttPatch(cttPatchLines, lineNumber)
                cttPatchData[part] = tech
            lineNumber += 1
        return cttPatchData
