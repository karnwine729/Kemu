from Kemu_CfgReader import CfgReader


class Part:
    def __init__(self, filePath, lines):
        self.filePath = filePath
        self.lines = lines
        self.title = ""
        self.mod = ""
        self.category = ""
        self.name = ""
        self.cost = ""
        self.size = ""
        self.tech = ""
        self.resources = None
        self.getResources()
        self.getPartData()
        self.shortenFilePath()

    def __str__(self):
        return f"Part: {self.title}"

    @staticmethod
    def convertBulkheadProfile(bulkheadProfile):
        bulkheadProfile = bulkheadProfile.strip()
        match bulkheadProfile:
            case "size0":
                return "0.625m"
            case "size1":
                return "1.25m"
            case "size1p5":
                return "1.875m"
            case "size2":
                return "2.5m"
            case "size3":
                return "3.75m"
            case "size4":
                return "5m"
            case "size5":
                return "7.5m"
            case _:
                return bulkheadProfile

    def getTitle(self):
        title = CfgReader.getValuesFromSearchTerm(self.lines, "title")
        self.title = CfgReader.lookupLocalization(title)

    def getMod(self):
        leftString = self.filePath.find("GameData")
        leftString = leftString + len("GameData") + 1
        mod = self.filePath[leftString:]
        rightString = mod.find("\\")
        if rightString == -1:
            rightString = mod.find("/")
        if rightString != -1:
            mod = mod[:rightString]
        self.mod = mod

    def getCategory(self):
        self.category = CfgReader.getValuesFromSearchTerm(self.lines, "category")

    def getName(self):
        self.name = CfgReader.getValuesFromSearchTerm(self.lines, "name")

    def getCost(self):
        self.cost = CfgReader.getValuesFromSearchTerm(self.lines, "cost")

    def getSize(self):
        size = CfgReader.getValuesFromSearchTerm(self.lines, "bulkheadProfiles")
        if isinstance(size, str):
            convertedSize = Part.convertBulkheadProfile(size)
            self.size = convertedSize
            return
        convertedSize = []
        for s in size:
            convertedSize.append(Part.convertBulkheadProfile(s))
        self.size = convertedSize

    def getTech(self):
        self.tech = CfgReader.getValuesFromSearchTerm(self.lines, "TechRequired")

    def updateForCommunityTechTree(self, communityTechTreePatchPath):
        cttPatch = CfgReader.getLines(communityTechTreePatchPath)
        nameFound = False
        for line in cttPatch:
            if self.name in line:
                nameFound = True
                continue
            if nameFound and "TechRequired" in line:
                line = line.split("=")[1]
                line = line.split("//")[0].strip()
                self.tech = line
                break

    def updateTech(self, newTechData):
        for tech in newTechData:
            if tech[0] == self.name:
                self.tech = tech[1]
                break

    def getPartData(self):
        self.getTitle()
        self.getMod()
        self.getCategory()
        self.getName()
        self.getCost()
        self.getSize()
        self.getTech()

    def getResourceLineNumbers(self):
        return CfgReader.locateTextBlockLoop(self.lines, 0, "RESOURCE", "}")

    def getResources(self):
        resources = []
        resourceLineNumbers = self.getResourceLineNumbers()
        for numbers in resourceLineNumbers:
            name = CfgReader.getValuesFromTextBlock(
                self.lines, "name", numbers[0], numbers[1]
            )
            amount = CfgReader.getValuesFromTextBlock(
                self.lines, "amount", numbers[0], numbers[1]
            )
            if amount == "AMOUNT NOT FOUND":
                continue
            if amount == str(0):
                amount = CfgReader.getValuesFromTextBlock(
                    self.lines, "maxAmount", numbers[0], numbers[1]
                )
            resources.append(name)
            resources.append(amount)
        self.resources = resources

    def shortenFilePath(self):
        leftString = self.filePath.find("Parts")
        leftString = leftString + len("Parts") + 1
        self.filePath = self.filePath[leftString:]
