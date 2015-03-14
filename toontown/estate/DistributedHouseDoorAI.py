from direct.directnotify import DirectNotifyGlobal
from toontown.building.DistributedDoorAI import DistributedDoorAI
from direct.distributed import DistributedObjectAI

class DistributedHouseDoorAI(DistributedDoorAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedHouseDoorAI")
    
    def __init__(self, air, blockNumber, doorType, doorIndex = 0, lockValue = 0, swing = 3):
        DistributedDoorAI.__init__(self, air, blockNumber, doorType, doorIndex, lockValue, swing)