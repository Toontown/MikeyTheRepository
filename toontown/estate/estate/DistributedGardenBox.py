import DistributedLawnDecor
from direct.directnotify import DirectNotifyGlobal
from direct.showbase.ShowBase import *
import GardenGlobals
from toontown.toonbase import TTLocalizer
from toontown.estate import PlantingGUI
from toontown.estate import PlantTreeGUI
from direct.distributed import DistributedNode
from pandac.PandaModules import NodePath
from pandac.PandaModules import Vec3

from DistributedFlower import DistributedFlower

FLOWER_POS = (None, (0,), (1.5, -1.5), (-3.5, 0, 3.5))

class DistributedGardenBox(DistributedLawnDecor.DistributedLawnDecor):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedGardenPlot')

    def __init__(self, cr):
        DistributedLawnDecor.DistributedLawnDecor.__init__(self, cr)
        self.plantPath = NodePath('plantPath')
        self.plantPath.reparentTo(self)
        self.plotScale = 1.0
        self.plantingGuiDoneEvent = 'plantingGuiDone'
        self.defaultModel = 'phase_5.5/models/estate/planterC'
        self.flowers = []
        self.flowersData = []

    def announceGenerate(self):
        self.notify.debug('announceGenerate')
        DistributedLawnDecor.DistributedLawnDecor.announceGenerate(self)

    def doModelSetup(self):
        if self.typeIndex == GardenGlobals.BOX_THREE:
            self.defaultModel = 'phase_5.5/models/estate/planterA'
        elif self.typeIndex == GardenGlobals.BOX_TWO:
            self.defaultModel = 'phase_5.5/models/estate/planterC'
        else:
            self.defaultModel = 'phase_5.5/models/estate/planterB'
            self.collSphereOffset = 0.0
            self.collSphereRadius = self.collSphereRadius * 1.41
            self.plotScale = Vec3(1.0, 1.0, 1.0)
            
        self.flowersData = [[0, -1, 0, 1, (49, 0)]] * self.typeIndex
        self.loadFlowers()
        
    def loadFlowers(self):
        for index, flower in enumerate(self.flowersData):
            f = DistributedFlower(self.cr)
            f.doId = index + 500
            f.gardenBox = self
            f.generate()
            f.setWaterLevel(flower[1])
            f.setGrowthLevel(flower[3])
            f.setTypeIndex(flower[-1][0])
            f.setSpecies(flower[-1][0])
            f.setVariety(flower[-1][1])
            f.announceGenerate()
            f.sendUpdate = self.hackedSendUpdate(f)
            f.reparentTo(self)
            f.setZ(self, 1.5)
            f.setX(FLOWER_POS[len(self.flowersData)][index])
            self.flowers.append(f)

    def setupShadow(self):
        pass

    def loadModel(self):
        self.rotateNode = self.plantPath.attachNewNode('rotate')
        self.model = None
        self.model = loader.loadModel(self.defaultModel)
        self.model.setScale(self.plotScale)
        self.model.reparentTo(self.rotateNode)
        self.stick2Ground()
        return

    def handleEnterPlot(self, entry = None):
        pass

    def handleExitPlot(self, entry = None):
        DistributedLawnDecor.DistributedLawnDecor.handleExitPlot(self, entry)

    def setTypeIndex(self, typeIndex):
        self.typeIndex = typeIndex

    def delete(self):
        DistributedLawnDecor.DistributedLawnDecor.delete(self)
        for flower in self.flowers:
            flower.disable()
            flower.delete()
            
        self.flowers = []
        
    def hackedSendUpdate(self, obj):
        def f(fieldName, args):
            doId = obj.doId
            dclass = obj.dclass.getName()
            
            if fieldName.endswith('Plot'):
                return
            
            print 'UPDATE FOR', doId, dclass, fieldName, args
            
        return f
        