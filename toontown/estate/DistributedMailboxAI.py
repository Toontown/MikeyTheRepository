from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.toonbase import ToontownGlobals
from toontown.catalog import CatalogItem
from MailboxGlobals import *

class DistributedMailboxAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedMailboxAI")

    def __init__(self, air, house):
        DistributedObjectAI.__init__(self, air)
        self.house = house
        self.curAv = None
        self.full = 0

    def getHouseId(self):
        return self.house.doId

    def getHousePos(self):
        return self.house.housePos

    def getName(self):
        return self.house.name

    def setFullIndicator(self, flag):
        self.full = flag
        
    def b_setFullIndicator(self, flag):
        self.setFullIndicator(flag)
        self.sendUpdate("setFullIndicator", [flag])

    def avatarEnter(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        if not av:
            return
            
        if self.curAv:
            # busy
            return
            
        if avId != self.house.avatarId:
            self.d_setMovie(MAILBOX_MOVIE_NOT_OWNER, avId)
            return
            
        elif not av.mailboxContents:
            movie = MAILBOX_MOVIE_EMPTY
            
            if av.onOrder:
                movie = MAILBOX_MOVIE_WAITING
                
            self.d_setMovie(movie, avId)
            return
        
        self.d_setMovie(MAILBOX_MOVIE_READY, avId)
        self.curAv = avId
        self.accept(self.air.getAvatarExitEvent(avId), self.d_freeAvatar)
        
    def avatarExit(self):
        self.d_freeAvatar()

    def d_freeAvatar(self):
        if not self.curAv:
            return
            
        self.ignore(self.air.getAvatarExitEvent(self.curAv))
        self.d_setMovie(MAILBOX_MOVIE_EXIT, self.curAv)
        self.sendUpdateToAvatarId(self.curAv, 'freeAvatar', [])
        self.curAv = None
        
    def d_setMovie(self, mode, avId):
        self.sendUpdate('setMovie', [mode, avId])

    def acceptItemMessage(self, context, blob, _, optional):
        avId = self.air.getAvatarIdFromSender()
            
        if avId != self.curAv:
            return
            
        av = self.air.doId2do.get(avId)
        if not av:
            return
            
        retcode = 0
        item = CatalogItem.getItem(blob, CatalogItem.Customization)
        if not item in av.mailboxContents:
            retcode = ToontownGlobals.P_NotAtMailbox
            
        else:
            retcode = item.recordPurchase(av, optional)
            
        av.mailboxContents.remove(item)
        av.d_setMailboxContents(av.mailboxContents)
        
        self.sendUpdateToAvatarId(avId, 'acceptItemResponse', [context, retcode])

    def discardItemMessage(self, context, blob, optional):
        avId = self.air.getAvatarIdFromSender()
            
        if avId != self.curAv:
            return
            
        av = self.air.doId2do.get(avId)
        if not av:
            return
            
        retcode = 1
        item = CatalogItem.getItem(blob, CatalogItem.Customization)
        if not item in av.mailboxContents:
            retcode = ToontownGlobals.P_NotAtMailbox
            
        av.mailboxContents.remove(item)
        av.d_setMailboxContents(av.mailboxContents)
        
        self.sendUpdateToAvatarId(avId, 'discardItemResponse', [context, retcode])

    def acceptInviteMessage(self, todo0, todo1):
        pass

    def rejectInviteMessage(self, todo0, todo1):
        pass

    def markInviteReadButNotReplied(self, todo0):
        pass

