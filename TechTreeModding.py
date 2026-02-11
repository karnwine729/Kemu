import csv

class TechTreeModding:

    @staticmethod
    def getCsvData(filepath):
        csvData = []
        with open(filepath) as csvFile:
            reader = csv.reader(csvFile)
            for row in reader:
                csvData.append(row)
        return csvData

    techTierData = getCsvData("kttTechTiers.csv")
