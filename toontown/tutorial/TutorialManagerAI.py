from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

from toontown.quest.Quests import TT_TIER

from toontown.building import DistributedDoorAI, DistributedHQInteriorAI, DistributedTutorialInteriorAI, DoorTypes, FADoorCodes
from toontown.suit import DistributedTutorialSuitAI
from toontown.toon import NPCToons, Experience

class TutorialHandler:
    def __init__(self, mgr, avId):
        self.mgr = mgr
        self.air = self.mgr.air
        self.avId = avId
        
        self.zones = (-1, -1, -1, -1)
        
        self.event = self.air.getAvatarExitEvent(avId)
        self.mgr.acceptOnce(self.event, self.abort)
        
        self.doorEvents = []
        
    def create(self):
        self.branchZone = self.air.zoneAllocator.allocate()
        self.interiorZone = self.air.zoneAllocator.allocate()
        self.hqZone = self.air.zoneAllocator.allocate()
        
        self.streetInteriorDoor = DistributedDoorAI.DistributedDoorAI(self.air, 2, DoorTypes.EXT_STANDARD, lockValue = FADoorCodes.DEFEAT_FLUNKY_TOM)
        self.interiorDoor = DistributedDoorAI.DistributedDoorAI(self.air, 2, DoorTypes.INT_STANDARD, lockValue = FADoorCodes.TALK_TO_TOM)
        
        self.streetInteriorDoor.setOtherDoor(self.interiorDoor)
        self.interiorDoor.setOtherDoor(self.streetInteriorDoor)
        
        self.acceptDoorEvent(1, {self.interiorDoor: FADoorCodes.UNLOCKED}) # after tom

        self.streetInteriorDoor.generateWithRequired(self.branchZone)
        self.streetInteriorDoor.sendUpdate('setDoorIndex', [self.streetInteriorDoor.getDoorIndex()])
        
        self.interiorDoor.generateWithRequired(self.interiorZone)
        self.interiorDoor.sendUpdate('setDoorIndex', [self.interiorDoor.getDoorIndex()])

        self.tom = NPCToons.createNPC(self.air, 20000, NPCToons.NPCToonDict[20000], self.interiorZone)
        self.tom.setTutorial(1)
        self.tom.b_setParent(1)
        
        self.tomInterior = DistributedTutorialInteriorAI.DistributedTutorialInteriorAI(2, self.air, self.interiorZone)
        self.tomInterior.setTutorialNpcId(self.tom.doId)
        self.tomInterior.generateWithRequired(self.interiorZone)
        
        self.cog = DistributedTutorialSuitAI.DistributedTutorialSuitAI(self.air, self)
        self.cog.setupSuitDNA(1, 0, 'c')
        self.cog.generateWithRequired(self.branchZone)

        self.streetNpc = None
        
        self.hqInterior = DistributedHQInteriorAI.DistributedHQInteriorAI(1, self.air, self.hqZone)
        self.hqInterior.generateWithRequired(self.hqZone)
        self.hqInterior.setTutorial(1)

        self.hqNpc = NPCToons.createNPC(self.air, 20002, NPCToons.NPCToonDict[20002], self.hqZone)
        self.hqNpc.setTutorial(1)
        self.hqNpc.setHq(1)

        self.streetHqDoor = DistributedDoorAI.DistributedDoorAI(self.air, 1, DoorTypes.EXT_HQ, doorIndex = 0, lockValue = FADoorCodes.DEFEAT_FLUNKY_HQ)
        self.streetHqDoor2 = DistributedDoorAI.DistributedDoorAI(self.air, 1, DoorTypes.EXT_HQ, doorIndex = 1, lockValue = FADoorCodes.DEFEAT_FLUNKY_HQ)

        self.hqInsideDoor = DistributedDoorAI.DistributedDoorAI(self.air, 1, DoorTypes.INT_HQ, doorIndex = 0, lockValue = FADoorCodes.TALK_TO_HQ)
        self.hqInsideDoor2 = DistributedDoorAI.DistributedDoorAI(self.air, 1, DoorTypes.INT_HQ, doorIndex = 1, lockValue = FADoorCodes.TALK_TO_HQ)
        
        self.acceptDoorEvent(2, {
                                 self.streetHqDoor: FADoorCodes.GO_TO_PLAYGROUND,
                                 self.streetHqDoor2: FADoorCodes.GO_TO_PLAYGROUND,
                                 self.hqInsideDoor2: FADoorCodes.UNLOCKED,
                                }
                            )
        
        self.streetHqDoor.setOtherDoor(self.hqInsideDoor)
        self.hqInsideDoor.setOtherDoor(self.streetHqDoor)
        
        self.streetHqDoor2.setOtherDoor(self.hqInsideDoor2)
        self.hqInsideDoor2.setOtherDoor(self.streetHqDoor2)

        self.streetHqDoor.generateWithRequired(self.branchZone)
        self.streetHqDoor2.generateWithRequired(self.branchZone)
        
        self.streetHqDoor.sendUpdate('setDoorIndex', [self.streetHqDoor.getDoorIndex()])
        self.streetHqDoor2.sendUpdate('setDoorIndex', [self.streetHqDoor2.getDoorIndex()])
        
        self.hqInsideDoor.generateWithRequired(self.hqZone)
        self.hqInsideDoor2.generateWithRequired(self.hqZone)
        
        self.hqInsideDoor.sendUpdate('setDoorIndex', [self.hqInsideDoor.getDoorIndex()])
        self.hqInsideDoor2.sendUpdate('setDoorIndex', [self.hqInsideDoor2.getDoorIndex()])
        
        self.zones = (20000, self.branchZone, self.interiorZone, self.hqZone)
        
    def deletes(self, object):
        if object:
            if object.air is not None:
                object.requestDelete()
        
    def destroy(self):
        for ev in self.doorEvents:
            self.mgr.ignore(ev)
            
        self.mgr.ignore(self.event)
        self.zones = (-1, -1, -1, -1)
        
        return # broken (crashes)
        
        self.deletes(self.streetInteriorDoor)
        self.deletes(self.interiorDoor)

        self.deletes(self.tom)    
        self.deletes(self.tomInterior)
        
        self.deletes(self.cog)
        self.deletes(self.streetNpc)
        
        self.deletes(self.hqInterior)
        self.deletes(self.hqNpc)
        
        self.deletes(self.streetHqDoor)
        self.deletes(self.streetHqDoor2)        
        self.deletes(self.hqInsideDoor)
        self.deletes(self.hqInsideDoor2)
        
        self.air.zoneAllocator.free(self.branchZone)
        self.air.zoneAllocator.free(self.interiorZone)
        self.air.zoneAllocator.free(self.hqZone)
        
    def getZones(self):
        return self.zones
        
    def cogDefeated(self):
        self.streetInteriorDoor.setDoorLock(FADoorCodes.TALK_TO_HQ)
        self.streetHqDoor.setDoorLock(FADoorCodes.UNLOCKED)
        self.streetHqDoor2.setDoorLock(FADoorCodes.UNLOCKED)
        
    def abort(self):
        self.destroy()
        self.mgr.cleanup(self.avId, abort = True)
        self.mgr = None
        self.air = None
        
    def finish(self):
        self.destroy()
        self.mgr = None
        self.air = None
        
    def acceptDoorEvent(self, index, map):
        def x():
            for door, code in map.items():
                door.setDoorLock(code)
                
            if index == 2 and self.streetNpc is None:
                self.streetNpc = NPCToons.createNPC(self.air, 20001, NPCToons.NPCToonDict[20001], self.branchZone)
                self.streetNpc.setTutorial(1)
                self.streetNpc.d_setPos(207, 19, -0.48)
                self.streetNpc.d_setHpr(90, 0, 0)
                
        ev = "tutorial-door-event-%d-%d" % (self.avId, index)
        self.mgr.accept(ev, x)
        self.doorEvents.append(x)
        
class TutorialManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("TutorialManagerAI")
    
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.av2tut = {}
        
    def requestTutorial(self):
        sender = self.air.getAvatarIdFromSender()
            
        if sender in self.av2tut:
            self.notify.warning("Got second requestTutorial from avatar %d" % sender)
            self.air.writeServerEvent('suspicious', sender, 'requested tutorial but already in one')
            return
            
        tut = TutorialHandler(self, sender)
        self.av2tut[sender] = tut
        
        tut.create()

        self.d_enterTutorial(sender, *tut.getZones())        
        
    def rejectTutorial(self):
        self.requestSkipTutorial()

    def requestSkipTutorial(self):
        sender = self.air.getAvatarIdFromSender()
        if not sender in self.air.doId2do:
            self.air.writeServerEvent('suspicious', sender, 'requested skip tutorial outside shard')
            return
            
        self.callOrWait(sender, self.__doSkip)
        
    def callOrWait(self, sender, func):
        if sender in self.air.doId2do:
            func(sender)
            return
            
        self.acceptOnce('toon-generate-%d' % sender, self.__doSkip, [sender])
            
    def __doSkip(self, sender):
        av = self.air.doId2do.get(sender)
        av.b_setRewardHistory(TT_TIER, [])
        av.b_setTutorialAck(1)
        av.b_setQuests([[163, 1000, 1000, 100, 3]])
        self.air.writeServerEvent('skipTutorial', sender, self.air.districtId)
        
        self.sendUpdateToChannel(sender, "skipTutorialResponse", [1])

    def d_enterTutorial(self, av, *zones):
        self.sendUpdateToAvatarId(av, "enterTutorial", zones)

    def allDone(self):
        sender = self.air.getAvatarIdFromSender()
        if sender not in self.av2tut:
            self.notify.warning("Got allDone from unknown avatar %d" % sender)
            self.air.writeServerEvent('suspicious', sender, 'sent allDone but not doing tutorial')
            return
            
        av = self.air.doId2do[sender]
        av.b_setTutorialAck(1)
        
        self.cleanup(sender)

    def toonArrived(self):
        sender = self.air.getAvatarIdFromSender()
        if sender not in self.av2tut:
            self.notify.warning("Got toonArrived from unknown avatar %d" % sender)
            self.air.writeServerEvent('suspicious', sender, 'sent toonArrived but not doing tutorial')
            return
            
        self.callOrWait(sender, self.__doEnter)
        
    def __doEnter(self, sender):
        av = self.air.doId2do[sender]
        
        inventory = av.inventory
        inventory.zeroInv(True)
        inventory.addItem(4, 0)
        inventory.addItem(5, 0)
        av.b_setInventory(inventory.makeNetString())
        
        av.b_setHp(15)
        av.b_setMaxHp(15)

        exp = Experience.Experience(av.getExperience(), av)
        for i in xrange(7):
            exp.experience[i] = 0
            
        av.b_setExperience(exp.makeNetString())
        
        av.b_setQuests([])
        av.b_setQuestHistory([])
        av.b_setRewardHistory(0, [])

    def cleanup(self, avId, abort = False):
        if not abort:
            self.av2tut[avId].finish()
            
        del self.av2tut[avId]
        