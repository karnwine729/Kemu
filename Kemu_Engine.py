from Kemu_CfgReader import CfgReader
from Kemu_Part import Part

class Engine(Part):
    def __init__(self, filePath, lines):
        super().__init__(filePath, lines)
        self.gimbal = ""
        self.engineStats = None
        self.jetStats = None
        self.getGimbal()
        self.getEngineStats()

    def __str__(self):
        return f"Engine: {self.title}"

    def printStatsSingle(self, statName01, statName02, stat01, stat02):
        print(f"{statName01}: ", end="\t")
        print(stat01)
        print(f"{statName02}: ", end="\t")
        print(stat02)

    def printStatsMulti(self, statName01, statName02, stats):
        num = 1
        index = 0
        while num < len(stats) - 1:
            print(f"{statName01} {num}: ", end="\t")
            print(stats[index])
            index += 1
            print(f"{statName02} {num}: ", end="\t")
            print(stats[index])
            index += 1
            num += 1

    def printEngineStatsSingle(self):
        self.printStatsSingle("Max Thrust", "Vac Isp", self.engineStats[0], self.engineStats[1])

    def printEngineStatsMulti(self):
        self.printStatsMulti("Max Thrust", "Vac Isp", self.engineStats)

    def printJetStatsSingle(self):
        self.printStatsSingle("velcurve", "atmCurve", self.jetStats[0], self.jetStats[1])

    def printJetStatsMulti(self):
        self.printStatsMulti("velcurve", "atmCurve", self.jetStats)

    def printEngineStats(self):
        if len(self.engineStats) == 2:
            self.printEngineStatsSingle()
        else:
            self.printEngineStatsMulti()

    def printJetStats(self):
        if len(self.jetStats) == 2:
            self.printJetStatsSingle()
        else:
            self.printJetStatsMulti()

    def printSpecs(self):
        super().printSpecs()
        print("Gimbal Range: ", end="\t")
        print(self.gimbal)
        self.printEngineStats()
        if self.jetStats == None:
            return
        self.printJetStats()


    def getCurveLines(self, curveName, lineNumber):
        lineNumbers = CfgReader.locateTextBlock(self.lines, lineNumber, curveName, "}")
        return self.lines[lineNumbers[0]:lineNumbers[1]]

    def getCurveKeys(self, curveLines):
        keys = []
        for line in curveLines:
            if "key" in line:
                line = line.split("=")[1].strip()
                keys.append(line)
        return keys

    def getVacIsp(self, lineNumber):
        ispCurveLines = self.getCurveLines("atmosphereCurve", lineNumber)
        ispCurveKeys = self.getCurveKeys(ispCurveLines)
        for line in ispCurveKeys:
            if line.startswith("0"):
                return line.split(" ")[1]
        return -1

    def getVelCurve(self, lineNumber):
        velCurveLines = self.getCurveLines("velCurve", lineNumber)
        velCurveKeys = self.getCurveKeys(velCurveLines)
        velCurve = []
        for line in velCurveKeys:
            line.split(" ")
            velCurve.append(line)
        return velCurve

    def getAtmCurve(self, lineNumber):
        atmCurveLines = self.getCurveLines("atmCurve", lineNumber)
        atmCurveKeys = self.getCurveKeys(atmCurveLines)
        atmCurve = []
        for line in atmCurveKeys:
            line.split(" ")
            atmCurve.append(line)
        return atmCurve

    def getGimbal(self):
        gimbal = CfgReader.getValuesFromSearchTerm(self.lines, "gimbalRange")
        if gimbal == "GIMBALRANGE NOT FOUND":
            gimbal = 0
        self.gimbal = gimbal

    def getJetStats(self):
        jetStats = []
        lineNumber = CfgReader.locateTextLine(self.lines, 0, "velCurve") - 1
        nextLine = lineNumber
        while not nextLine == -1:
            velCurve = self.getVelCurve(lineNumber)
            jetStats.append(velCurve)
            atmCurve = self.getAtmCurve(lineNumber)
            jetStats.append(atmCurve)
            nextLine = CfgReader.locateTextLine(self.lines, lineNumber, "velCurve")
            lineNumber = nextLine
        self.jetStats = jetStats

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
        if CfgReader.isJetEngine(self.lines):
            self.getJetStats()
        self.engineStats = engineStats
