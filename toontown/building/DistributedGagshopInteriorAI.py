# File: D (Python 2.4)

from direct.distributed import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from toontown.toon import NPCToons

class DistributedGagshopInteriorAI(DistributedObjectAI.DistributedObjectAI):
    
    def __init__(self, block, air, zoneId):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        self.block = block
        self.zoneId = zoneId
        
    def announceGenerate(self):
        DistributedObjectAI.DistributedObjectAI.announceGenerate(self)
        self.npcs = NPCToons.createNpcsInZone(self.air, self.zoneId)
        
    def delete(self):
        for npc in self.npcs:
            npc.requestDelete()
        DistributedObjectAI.DistributedObjectAI.delete(self)

    def getZoneIdAndBlock(self):
        r = [
            self.zoneId,
            self.block]
        return r


