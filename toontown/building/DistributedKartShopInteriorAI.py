# File: D (Python 2.4)

from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.toon import NPCToons

class DistributedKartShopInteriorAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedKartShopInteriorAI')
    
    def __init__(self, block, air, zoneId):
        DistributedObjectAI.__init__(self, air)
        self.block = block
        self.zoneId = zoneId

    
    def generate(self):
        DistributedObjectAI.generate(self)
        
    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)
        self.npcs = NPCToons.createNpcsInZone(self.air, self.zoneId)
        
    def delete(self):
        for npc in self.npcs:
            npc.requestDelete()

    
    def getZoneIdAndBlock(self):
        return [
            self.zoneId,
            self.block]


