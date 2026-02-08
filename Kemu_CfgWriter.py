import io

class CfgWriter:

    @staticmethod
    def lookupTechTreeTier(techNode, techTierData):
        for row in techTierData:
            if row[0] == techNode:
                return row[1]
        return "TECH NODE NOT FOUND"
    
    @staticmethod
    def createTechTreePatch(parts, techTierData):
        modName = parts[0].mod
        with io.open(f"TechTreePatch_{modName}.cfg", 'w', encoding="UTF-8") as file:
            for part in parts:
                techTier = CfgWriter.lookupTechTreeTier(part.tech, techTierData)
                file.write(f"@PART[{part.name}]:FINAL // {part.title}\n")
                file.write("{\n")
                file.write(f"\t@techRequired = {part.tech} // Tier {techTier}\n")
                file.write("}\n")