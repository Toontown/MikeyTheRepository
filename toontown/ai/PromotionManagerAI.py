from toontown.coghq import CogDisguiseGlobals
from toontown.suit import SuitDNA

class PromotionManagerAI:
    def __init__(self, air):
        self.air = air
        
    def recoverMerits(self, toon, suitsKilled, zoneId, mult = 1, extraMerits = None):
        if 1: #extraMerits is None:
            extraMerits = [0, 0, 0, 0]
            
        #else:
            # extraMerits = [0, extraMerits, 0, 0]
        
        # to do: figure out which track we should add extra merits to (check zoneId?)
            
        amounts = {x: y for x, y in zip(SuitDNA.suitDepts, extraMerits)}
        parts = toon.getCogParts()
        
        # calc
        for suit in suitsKilled:
            if suit['isVirtual']:
                continue
                
            track, level = suit['track'], suit['level']
            deptIdx = SuitDNA.suitDepts.index(track)
            if not CogDisguiseGlobals.isSuitComplete(parts, deptIdx):
                continue
            
            mult = (2 if self.air.suitInvasionManager.hasInvading() else 1)
            mult *= int(suit['hasRevives']) + 1
                
            amount = int((level + 1) / 2 * mult) * mult
            amounts[track] += amount
            
        merits = toon.getCogMerits()
        am2 = [0, 0, 0, 0]
        
        for dept, value in amounts.items():
            dept = SuitDNA.suitDepts.index(dept)
            needed = max(0, CogDisguiseGlobals.getTotalMerits(toon, dept) - merits[dept])
            am2[dept] = min(needed, value)
            
        # apply
        toon.b_setCogMerits([x + y for x, y in zip(merits, am2)])
        
        return am2
        