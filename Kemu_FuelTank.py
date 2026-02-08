from Kemu_CfgReader import CfgReader
from Kemu_Part import Part

class FuelTank(Part):
    def __init__(self, filePath, lines):
        super().__init__(filePath, lines)

    def __str__(self):
        return f"FuelTank: {self.title}"

    def getB9TankVolume(self):
        self.resources = CfgReader.getValuesFromSearchTerm(self.lines, "baseVolume")

    def getResources(self):
        if not CfgReader.locateTextLine(self.lines, 0, "baseVolume") == -1:
            self.getB9TankVolume()
            return
        super().getResources()
