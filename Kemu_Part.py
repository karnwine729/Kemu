from Kemu_CfgReader import CfgReader

class Part:
    def __init__(self, filePath, lines):
        self.filePath = filePath
        self.lines = lines
        self.title = ""
        self.name = ""
        self.cost = ""
        self.size = ""
        self.tech = ""
        self.getPartData(self.lines)
        
    def printSpecs(self):
        print(self.filePath)
        print("Title: ", end="\t\t")
        print(self.title)
        print("CodeName: ", end="\t")
        print(self.name)
        print("Cost: ", end="\t\t")
        print(self.cost)
        print("Size: ", end="\t\t")
        print(self.size)
        print("Tech: ", end="\t\t")
        print(self.tech)
    
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
        title = CfgReader.lookupLocalization(title)
        self.title = title
    
    def getName(self):
        name = CfgReader.getValuesFromSearchTerm(self.lines, "name")
        self.name = name
    
    def getCost(self):
        cost = CfgReader.getValuesFromSearchTerm(self.lines, "cost")
        self.cost = cost
    
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
    
    def getPartData(self, lines):
        self.getTitle()
        self.getName()
        self.getCost()
        self.getSize()
        self.getTech()
