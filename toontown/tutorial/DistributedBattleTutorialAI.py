from direct.directnotify import DirectNotifyGlobal
from toontown.battle.DistributedBattleAI import DistributedBattleAI

class DistributedBattleTutorialAI(DistributedBattleAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedBattleTutorialAI")

    def __init__(self, air, battleMgr, pos, suit, toonId, zoneId, finishCallback = None,
                 maxSuits = 4, tutorialFlag = 0, levelFlag = 0, interactivePropTrackBonus = -1):
                 
        DistributedBattleAI.__init__(self, air, battleMgr, pos, suit, toonId, zoneId, finishCallback,
                                     maxSuits = 1, tutorialFlag = 1, levelFlag = 0, interactivePropTrackBonus = -1)