from direct.directnotify import DirectNotifyGlobal
from toontown.suit.DistributedSuitBaseAI import DistributedSuitBaseAI
from toontown.tutorial.DistributedBattleTutorialAI import DistributedBattleTutorialAI
from toontown.battle.BattleManagerAI import BattleManagerAI
from panda3d.core import *

class DistributedTutorialSuitAI(DistributedSuitBaseAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedTutorialSuitAI")
    
    def __init__(self, air, tutMgr):
        DistributedSuitBaseAI.__init__(self, air, None)

        self.battleMgr = BattleManagerAI(self.air)
        self.battleMgr.battleConstructor = DistributedBattleTutorialAI
        self.tutMgr = tutMgr
        
    def requestBattle(self, x, y, z, h, p, r):
        avId = self.air.getAvatarIdFromSender()
        
        if not self.air.doId2do.get(avId):
            return
            
        self.confrontPos = Point3(x, y, z)
        self.confrontHpr = Vec3(h, p, r)

        self.battleMgr.newBattle(self.zoneId, self.zoneId, Point3(35, 20, -0.5), self, avId, self._battleDone)

    def _battleDone(self, zoneId):        
        self.tutMgr.cogDefeated()
        del self.tutMgr

    def getConfrontPosHpr(self):
        return self.confrontPos, self.confrontHpr
        