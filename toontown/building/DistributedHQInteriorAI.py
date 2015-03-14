# File: D (Python 2.4)

from direct.distributed import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
import cPickle

from toontown.toon.DistributedNPCSpecialQuestGiverAI import *

class DistributedHQInteriorAI(DistributedObjectAI.DistributedObjectAI):
    
    def __init__(self, block, air, zoneId):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        self.block = block
        self.zoneId = zoneId
        self.tutorial = 0
        self.isDirty = False
        self.accept('leaderboardChanged', self.leaderboardChanged)
        self.accept('leaderboardFlush', self.leaderboardFlush)

    
    def delete(self):
        self.ignore('leaderboardChanged')
        self.ignore('leaderboardFlush')
        self.ignore('setLeaderBoard')
        self.ignore('AIStarted')
        for npc in self.npcs:
            npc.requestDelete()
            
        DistributedObjectAI.DistributedObjectAI.delete(self)
        
    def generate(self):
        DistributedObjectAI.DistributedObjectAI.generate(self)
        
    def announceGenerate(self):
        DistributedObjectAI.DistributedObjectAI.announceGenerate(self)
        self.npcs = NPCToons.createNpcsInZone(self.air, self.zoneId)
    
    def getZoneIdAndBlock(self):
        r = [
            self.zoneId,
            self.block]
        return r

    
    def leaderboardChanged(self):
        self.isDirty = True

    
    def leaderboardFlush(self):
        if self.isDirty:
            self.sendNewLeaderBoard()
        

    
    def sendNewLeaderBoard(self):
        if self.air:
            self.isDirty = False
            self.sendUpdate('setLeaderBoard', [
                cPickle.dumps(self.air.trophyMgr.getLeaderInfo(), 1)])
        

    
    def getLeaderBoard(self):
        return cPickle.dumps(self.air.trophyMgr.getLeaderInfo(), 1)

    
    def getTutorial(self):
        return self.tutorial

    
    def setTutorial(self, flag):
        if self.tutorial != flag:
            self.tutorial = flag
            self.sendUpdate('setTutorial', [
                self.tutorial])
        


