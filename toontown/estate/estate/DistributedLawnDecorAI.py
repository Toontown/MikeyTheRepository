from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedNodeAI import DistributedNodeAI

class DistributedLawnDecorAI(DistributedNodeAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedLawnDecorAI")

    def __init__(self, air):
        DistributedNodeAI.__init__(self, air)
        self.plot = 0
        self.ownerIndex = 0
          
    def setPlot(self, todo0):
        self.plot = plot
          
    def getPlot(self):
        return self.plot

    def getHeading(self):
        return self.getH()

    def getPosition(self):
        return self.getPos()

    def setOwnerIndex(self, ownerIndex):
        self.ownerIndex = ownerIndex
        
    def getOwnerIndex(self):
        return self.ownerIndex

    def plotEntered(self):
        pass

    def removeItem(self):
        pass

    def d_setMovie(self, todo0, todo1):
        pass

    def movieDone(self):
        pass

    def d_interactionDenied(self, todo0):
        pass

