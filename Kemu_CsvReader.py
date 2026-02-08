import csv

class CsvReader:

    @staticmethod
    def getCsvData(filepath):
        csvData = []
        with open(filepath) as csvFile:
            reader = csv.reader(csvFile)
            for row in reader:
                csvData.append(row)
        return csvData
    
    @staticmethod
    def getNewTechData(filepath):
        newTechData = []
        with open(filepath) as csvFile:
            reader = csv.reader(csvFile)
            for row in reader:
                newTechData.append(row[2:3])
        return newTechData