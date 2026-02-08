import io

from Kemu_CsvReader import CsvReader
from Kemu_CsvWriter import CsvWriter

class TechTreeModding:

    techTierData = CsvReader.getCsvData("kttTechTiers.csv")

    @classmethod
    def lookupTechTreeTier(cls, techNode):
        for row in cls.techTierData:
            if row[0] == techNode:
                return row[1]
        return "TECH NODE NOT FOUND"
    
    @classmethod
    def createCsvForTechTreePatches(cls, parts):
        modName = parts[0].mod
        csvFileName = f"ForTechTreePatches_{modName}.csv"
        columnNames = ["Part Title", "Category", "Part Code Name", "KTT Location", "KTT Tier"]
        csvEntries = []
        for part in parts:
            techTier = cls.lookupTechTreeTier(part.tech)
            csvEntries.append([part.title, part.category, part.name, part.tech, techTier])
        CsvWriter.createCsv(csvFileName, columnNames, csvEntries)
    
    @classmethod
    def createTechTreePatch(cls, parts):
        modName = parts[0].mod
        with io.open(f"TechTreePatch_{modName}.cfg", 'w', encoding="UTF-8") as file:
            for part in parts:
                techTier = cls.lookupTechTreeTier(part.tech)
                file.write(f"@PART[{part.name}]:FINAL // {part.title}\n")
                file.write("{\n")
                file.write(f"\t@techRequired = {part.tech} // Tier {techTier}\n")
                file.write("}\n")

    @staticmethod
    def updatePartsForCommunityTechTree(parts, communityTechTreePatchFilepath):
        for part in parts:
            part.updateForCommunityTechTree(communityTechTreePatchFilepath)