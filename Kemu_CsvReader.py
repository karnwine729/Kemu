import csv

class CsvReader:

    @staticmethod
    def getTechTreeTierData():
        techTierData = []
        with open("kttTechTiers.csv") as csvFile:
            reader = csv.reader(csvFile)
            for row in reader:
                techTierData.append(row)
        return techTierData