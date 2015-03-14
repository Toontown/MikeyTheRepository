from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import *
from toontown.estate.DistributedFurnitureItemAI import DistributedFurnitureItemAI
from BankGlobals import *

class DistributedBankAI(DistributedFurnitureItemAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedBankAI")
    
    def __init__(self, air, furnitureMgr, catalogItem):
        DistributedFurnitureItemAI.__init__(self, air, furnitureMgr, catalogItem)
        self.ownerId = furnitureMgr.ownerId
        self.inUse = False

    def avatarEnter(self):
        avId = self.air.getAvatarIdFromSender()
        if self.inUse:
            self.sendUpdateToAvatarId(avId, 'freeAvatar', [])
        elif not self.ownerId:
            # This bank has no owner!
            self.setMovie(BANK_MOVIE_NO_OWNER, avId)
        elif avId != self.ownerId:
            # Avatar isn't bank owner
            self.setMovie(BANK_MOVIE_NOT_OWNER, avId)
        else:
            self.setInUse(avId)
            self.setMovie(BANK_MOVIE_GUI, avId)
            
    def setInUse(self, avId):
        av = self.air.doId2do.get(avId)
        if av:
            self.inUse = True
            event = self.air.getAvatarExitEvent(avId)
            self.accept(event, self.__handleUnexpectedExit, [avId])
            
    def __handleUnexpectedExit(self, avId):
        self.notify.info('Avatar %s unexpected exit! Setting bank free...' %avId)
        self.setFree()
         

    def setMovie(self, mode, avId):
        self.sendUpdate('setMovie', [mode, avId, globalClockDelta.getRealNetworkTime()])

    def transferMoney(self, amount):
        avId = self.air.getAvatarIdFromSender()
        if amount == 0:
            self.setMovie(BANK_MOVIE_WITHDRAW, avId)
            taskMgr.doMethodLater(4.0, self.setFree, 'set-bank-free')
            return
        av = self.air.doId2do.get(avId)
        if av:
            self.air.bankMgr.transferMoney(avId, amount)
            self.setMovie(BANK_MOVIE_DEPOSIT, avId)
            taskMgr.doMethodLater(4.0, self.setFree, 'set-bank-free')
            
    def setFree(self, task = None):
        self.inUse = False
        if task:
            return task.done

