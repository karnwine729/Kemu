import csv
from Kemu_CsvReader import CsvReader

class CsvWriter:

    @staticmethod
    def createCsv(filename, columnNames, rows):
        with open(filename, 'w', encoding="UTF-8", newline="") as csvfile:
            csvWriter = csv.writer(csvfile)
            csvWriter.writerow(columnNames)
            csvWriter.writerows(rows)

    @staticmethod
    def createDataDumpCsv(parts):
        modName = parts[0].mod
        csvFileName = f"PartDataDump_{modName}.csv"
        columnNames = ["Filepath", "Part Title", "Category", "Part Code Name", "Cost", "Size", "Tech"]
        csvEntries = []
        for part in parts:
            csvEntries.append([part.filePath, part.title, part.category, part.name, part.cost, part.size, part.tech])
        CsvWriter.createCsv(csvFileName, columnNames, csvEntries)


    @staticmethod
    def createCsvForTechTreePatches(parts, techTierData):
        modName = parts[0].mod
        csvFileName = f"ForTechTreePatches_{modName}.csv"
        columnNames = ["Part Title", "Category", "Part Code Name", "KTT Location", "KTT Tier"]
        csvEntries = []
        for part in parts:
            techTier = CsvReader.lookupTechTreeTier(part.tech, techTierData)
            csvEntries.append([part.title, part.category, part.name, part.tech, techTier])
        CsvWriter.createCsv(csvFileName, columnNames, csvEntries)