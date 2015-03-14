from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.task.Task import Task
import random

TOONUP = 2
INITIAL_TOONUP_WAIT = 45
MIN_HEAL_TIME_INTERVAL = 20
MAX_HEAL_TIME_INTERVAL = 60

delta = MAX_HEAL_TIME_INTERVAL - MIN_HEAL_TIME_INTERVAL

def getNextHealTime():
    return MIN_HEAL_TIME_INTERVAL + delta * random.random()

class SafeZoneManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("SafeZoneManagerAI")
        
    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)

    def enterSafeZone(self):
        avId = self.air.getAvatarIdFromSender()
        self.doMethodLater(INITIAL_TOONUP_WAIT, SafeZoneManagerAI.__doHeal, self.uniqueName('sz-toonup-%d' % avId), [self, avId])

    def exitSafeZone(self):
        avId = self.air.getAvatarIdFromSender()
        taskMgr.remove(self.uniqueName('sz-toonup-%d' % avId))

    def __doHeal(self, avId):
        if avId not in self.air.doId2do:
            return Task.done
            
        av = self.air.doId2do[avId]
        av.toonUp(TOONUP)
        
        self.doMethodLater(getNextHealTime(), SafeZoneManagerAI.__doHeal, self.uniqueName('sz-toonup-%d' % avId), [self, avId])
        return Task.done
    