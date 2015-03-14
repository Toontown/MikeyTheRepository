from direct.directnotify import DirectNotifyGlobal
from toontown.estate.DistributedLawnDecorAI import DistributedLawnDecorAI
import GardenGlobals

class DistributedPlantBaseAI(DistributedLawnDecorAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedPlantBaseAI")

    def __init__(self, air):
        DistributedLawnDecorAI.__init__(self, air)
        self.typeIndex = GardenGlobals.FLOWER_TYPE
        self.waterLevel = -1
        self.growthLevel = -1
    
    def setTypeIndex(self, typeIndex):
        self.typeIndex = typeIndex
        
    def d_setTypeIndex(self, typeIndex):
        self.sendUpdate("setTypeIndex", [typeIndex])
        
    def b_setTypeIndex(self, typeIndex):
        self.setTypeIndex(typeIndex)
        self.d_setTypeIndex(typeIndex)
        
    def getTypeIndex(self):
        return self.typeIndex

    def setWaterLevel(self, waterLevel):
        self.waterLevel = waterLevel
       
    def d_setWaterLevel(self, waterLevel):
        self.sendUpdate("setWaterLevel", [waterLevel])
        
    def b_setWaterLevel(self, waterLevel):
        self.setWaterLevel(waterLevel)
        self.d_setWaterLevel(waterLevel)
        
    def getWaterLevel(self):
        return self.waterLevel

    def setGrowthLevel(self, growthLevel):
        self.growthLevel = growthLevel
        
    def d_setGrowthLevel(self, growthLevel):
        self.sendUpdate("setGrowthLevel", [growthLevel])
        
    def b_setGrowthLevel(self, growthLevel):
        self.setGrowthLevel(growthLevel)
        self.d_setGrowthLevel(growthLevel)
        
    def getGrowthLevel(self):
        return self.growthLevel

    def waterPlant(self):
        pass

    def waterPlantDone(self):
        pass

