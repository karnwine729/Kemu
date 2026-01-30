from Kemu_CfgReader import CfgReader
from Kemu_Part import Part

class Engine(Part):
    def __init__(self, filePath, lines):
        super().__init__(filePath, lines)
        self.gimbal = ""
        self.engineStats = ["", ""]
        self.getGimbal()
        self.getEngineStats()
        

    def __str__(self):
        return f"Engine: {self.title}"

    def printSingleEngineStats(self):
        print("Max Thrust: ", end="\t")
        print(self.engineStats[0])
        print("Vac Isp: ", end="\t")
        print(self.engineStats[1])

    def printMultiEngineStats(self):
        num = 1
        index = 0
        while num < len(self.engineStats) - 1:
            print("Max Thrust " + str(num) + ": ", end="\t")
            print(self.engineStats[index])
            index += 1
            print("Vac Isp " + str(num) + ": ", end="\t")
            print(self.engineStats[index])
            index += 1
            num += 1

    def printSpecs(self):
        super().printSpecs()
        print("Gimbal Range: ", end="\t")
        print(self.gimbal)
        if len(self.engineStats) == 2:
            self.printSingleEngineStats()
        else:
            self.printMultiEngineStats()        

    def getIspCurveLines(self, lineNumber):
        ispLineNumbers = CfgReader.locateTextBlock(self.lines, lineNumber, "atmosphereCurve", "}")
        return self.lines[ispLineNumbers[0]:ispLineNumbers[1]]

    def getIspCurveKeys(self, ispCurve):
        ispCurveKeys = []
        for line in ispCurve:
            if "key" in line:
                line = line.split("=")[1].strip()
                ispCurveKeys.append(line)
        return ispCurveKeys

    def getVacIsp(self, lineNumber):
        ispCurveLines = self.getIspCurveLines(lineNumber)
        ispCurveKeys = self.getIspCurveKeys(ispCurveLines)
        for line in ispCurveKeys:
            if line.startswith("0"):
                return line.split(" ")[1]
        return -1

    def getGimbal(self):
        gimbal = CfgReader.getValuesFromSearchTerm(self.lines, "gimbalRange")
        if gimbal == "GIMBALRANGE NOT FOUND":
            gimbal = 0
        self.gimbal = gimbal

    def getEngineStats(self):
        engineStats = []
        lineNumber = CfgReader.locateTextLine(self.lines, 0, "maxThrust")
        nextLine = lineNumber
        while not nextLine == -1:
            maxThrust = CfgReader.getValuesFromLineNumber(self.lines, lineNumber)
            engineStats.append(maxThrust)
            vacIsp = self.getVacIsp(lineNumber)
            engineStats.append(vacIsp)
            nextLine = CfgReader.locateTextLine(self.lines, lineNumber, "maxThrust")
            lineNumber = nextLine
        self.engineStats = engineStats

