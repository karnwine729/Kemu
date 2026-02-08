from Kemu_CfgReader import CfgReader
from Kemu_Part import Part

class Engine(Part):
    def __init__(self, filePath, lines):
        super().__init__(filePath, lines)
        self.gimbal = ""
        self.engineSpecs = None
        self.jetSpecs = None
        self.getGimbal()
        self.getEngineSpecs()

    def __str__(self):
        return f"Engine: {self.title}"

    def getGimbal(self):
        gimbal = CfgReader.getValuesFromSearchTerm(self.lines, "gimbalRange")
        if gimbal == "GIMBALRANGE NOT FOUND":
            gimbal = 0
        self.gimbal = gimbal

    def getCurveLines(self, lineNumber, curveName):
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
        ispCurveLines = self.getCurveLines(lineNumber, "atmosphereCurve")
        ispCurveKeys = self.getCurveKeys(ispCurveLines)
        for line in ispCurveKeys:
            if line.startswith("0"):
                return line.split(" ")[1]
        return -1

    def getVelCurveMaxThrustMultiplierFromKeys(self, velCurveKeys):
        maxThrustMultiplier = 0
        for key in velCurveKeys:
            key = key.split(" ")
            key[1] = float(key[1])
            if key[1] > maxThrustMultiplier:
                maxThrustMultiplier = key[1]
        return maxThrustMultiplier

    def getVelCurveMaxThrustMultiplier(self, lineNumber):
        velCurveLines = self.getCurveLines(lineNumber-1, "velCurve")
        velCurveKeys = self.getCurveKeys(velCurveLines)
        return self.getVelCurveMaxThrustMultiplierFromKeys(velCurveKeys)

    def getJetMaxThrust(self, maxThrust, lineNumber):
        maxThrust = float(maxThrust)
        return maxThrust * self.getVelCurveMaxThrustMultiplier(lineNumber)

    def hasVelCurveInCurrentEngineModule(self, lineNumber):
        for line in self.lines[lineNumber:]:
            if "velCurve" in line:
                return True
        return False

    def getEngineSpecs(self):
        engineSpecs = []
        isJetEngine = CfgReader.isJetEngine(self.lines)
        lineNumber = CfgReader.locateTextLine(self.lines, 0, "maxThrust")
        nextLine = lineNumber
        while not nextLine == -1:
            maxThrust = CfgReader.getValuesFromLineNumber(self.lines, lineNumber)
            if isJetEngine:
                if self.hasVelCurveInCurrentEngineModule(lineNumber):
                    maxThrust = self.getJetMaxThrust(maxThrust, lineNumber)
            engineSpecs.append(maxThrust)
            vacIsp = self.getVacIsp(lineNumber)
            engineSpecs.append(vacIsp)
            nextLine = CfgReader.locateTextLine(self.lines, lineNumber, "maxThrust")
            lineNumber = nextLine
        self.engineSpecs = engineSpecs
