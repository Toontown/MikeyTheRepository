from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.toonbase import ToontownGlobals

BuildingFloorPoints = {
    1: 2,
    2: 3,
    3: 5,
    4: 6,
    5: 7,
    'HACK': 50
}

class DistributedTrophyMgrAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedTrophyMgrAI")
    
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.publicLeaderInfo = [[], [], []]
        self.aiLeaderInfo = {}
        self.points = ToontownGlobals.TrophyStarLevels
        
    def addTrophy(self, avId, name, numFloors):
        if not self.aiLeaderInfo.has_key(avId):
            self.aiLeaderInfo[avId] = [name, 0]
        self.aiLeaderInfo[avId][1] += BuildingFloorPoints[numFloors]
        
        info = self.aiLeaderInfo[avId]
        score = info[1]
        star = 5
        for i in range(5):
            lvl = self.points[star]
            if score >= lvl:
                star = lvl
                break
            star -= 1
                
        if star > 0:
            if not self.publicLeaderInfo[0].__contains__(avId):
                self.publicLeaderInfo[0].append(avId)
                self.publicLeaderInfo[1].append(name)
                self.publicLeaderInfo[2].append(score)
            else:
                myIndex = self.publicLeaderInfo[0].index(avId)
                self.publicLeaderInfo[2][myIndex] += score
                
            self.giveStar(avId, score)
            messenger.send('leaderboardChanged')
            messenger.send('leaderboardFlush')
        
    def giveStar(self, avId, score):
        av = self.air.doId2do.get(avId)
        if av:
            av.d_setTrophyScore(score)
    
    def getLeaderInfo(self):
        return self.publicLeaderInfo

    def requestTrophyScore(self):
        avId = self.air.getAvatarIdFromSender()
        score = 0
        if self.aiLeaderInfo.has_key(avId):
            score = self.aiLeaderInfo[avId][1]
        self.giveStar(avId, score)

from otp.ai.MagicWordGlobal import *
@magicWord(category=CATEGORY_CHARACTERSTATS2)
def star():
    toon = spellbook.getTarget()
    if toon:
        doId = toon.doId
        name = toon.getName()
        for i in range(2):
            simbase.air.trophyMgr.addTrophy(doId, name, 'HACK')
            