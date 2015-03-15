from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import *
from direct.task.Timer import *
from toontown.estate.DistributedFurnitureItemAI import DistributedFurnitureItemAI
from toontown.toon.ToonDNA import *
from ClosetGlobals import *

class DistributedClosetAI(DistributedFurnitureItemAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedClosetAI")
    
    def __init__(self, air, furnitureMgr, catalogItem):
        DistributedFurnitureItemAI.__init__(self, air, furnitureMgr, catalogItem)
        self.ownerId = 0
        self.currAvId = 0
        self.currAvDNA = None
        self.inUse = False
        self.timer = Timer('DistributedClosetAITimer')

    def setOwnerId(self, id):
        self.ownerId = id
        
    def getOwnerId(self):
        return self.ownerId
        
    def enterAvatar(self):
        avId = self.air.getAvatarIdFromSender()
        if self.inUse:
            self.sendUpdateToAvatarId(avId, 'freeAvatar', [])
            return
        ownerAv = self.air.doId2do.get(self.ownerId)
        topList,botList = ([],[])
        if ownerAv:
            topList = ownerAv.getClothesTopsList()
            botList = ownerAv.getClothesBottomsList()
        
        av = self.air.doId2do.get(avId)
        if av:
            avDna = ToonDNA(av.getDNAString())
            self.d_setState(OPEN, avId, avDna.gender, topList, botList)
            self.setInUse(avId)
            self.resetTimeout()
            
    def setInUse(self, avId):
        av = self.air.doId2do.get(avId)
        if av:
            self.inUse = True
            self.currAvId = avId
            event = self.air.getAvatarExitEvent(avId)
            self.accept(event, self.__handleUnexpectedExit, [avId])
            self.currAvDNA = av.getDNAString()
            
    def __handleUnexpectedExit(self, avId):
        self.notify.info('Avatar %s unexpected exit! Setting closet free...' %avId)
        self.setFree()
            
    def setFree(self):
        self.inUse = False
        self.currAvId = 0
        self.currAvDNA = None
        
    def d_setState(self, mode, avId, gender = '', topList = [], botList = []):
        self.sendUpdate('setState', [mode, avId, self.ownerId, gender, topList, botList])
        
    def d_setMovie(self, mode, avId):
        self.sendUpdate('setMovie', [mode, avId, globalClockDelta.getRealNetworkTime()])
        
    def resetTimeout(self):
        self.timer.stop()
        self.timer.startCallback(TIMEOUT_TIME + 10, self.handleTimeout)
        
    def handleTimeout(self):
        self.d_setMovie(CLOSET_MOVIE_TIMEOUT, self.currAvId)
        self.d_setState(CLOSED, self.currAvId)
        self.setFree()
        
    def setDNA(self, dnaStr, definitive, which):   
        self.resetTimeout()
        if self.currAvId:
            currAv = self.air.doId2do.get(self.currAvId)
            if currAv:
                if definitive == 2 and which > 0:
                    if which & SHIRT:
                        dna = ToonDNA(self.currAvDNA)
                        newDNA = ToonDNA(dnaStr)
                        if currAv.replaceItemInClothesTopsList(newDNA.topTex, newDNA.topTexColor, newDNA.sleeveTex, newDNA.sleeveTexColor, dna.topTex, dna.topTexColor, dna.sleeveTex, dna.sleeveTexColor) == 1:
                            currAv.b_setClothesTopsList(currAv.getClothesTopsList())
                    if which & SHORTS:
                        if currAv.replaceItemInClothesBottomsList(newDNA.botTex, newDNA.botTexColor, dna.botTex, dna.botTexColor) == 1:
                            currAv.b_setClothesBottomsList(currAv.getClothesBottomsList())
                    currAv.b_setDNAString(dnaStr)
                    self.d_setMovie(CLOSET_MOVIE_COMPLETE, self.currAvId)
                    self.d_setState(CLOSED, self.currAvId)
                    self.setFree()
                    self.timer.stop()
                elif definitive == 1:
                    currAv.b_setDNAString(self.currAvDNA)
                    self.d_setMovie(CLOSET_MOVIE_COMPLETE, self.currAvId)
                    self.d_setState(CLOSED, self.currAvId)
                    self.setFree()
                    self.timer.stop()
                else:
                    self.sendUpdate('setCustomerDNA', [self.currAvId, self.currAvDNA])
        
    def removeItem(self, dna, t_or_b):
        dna = ToonDNA(dna)
        currAv = self.air.doId2do.get(self.currAvId)
        if currAv:
            if t_or_b == SHIRT:
                if currAv.removeItemInClothesTopsList(dna.topTex, dna.topTexColor, dna.sleeveTex, dna.sleeveTexColor) == 1:
                    currAv.b_setClothesTopsList(currAv.getClothesTopsList())
            elif t_or_b == SHORTS:
                if currAv.removeItemInClothesBottomsList(dna.botTex, dna.botTexColor) == 1:
                    currAv.b_setClothesBottomsList(currAv.getClothesBottomsList())
            #self.sendUpdate('resetItemLists')