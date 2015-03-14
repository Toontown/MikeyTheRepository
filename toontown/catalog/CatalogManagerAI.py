from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from CatalogGenerator import CatalogGenerator
from toontown.toonbase import ToontownGlobals
import time

MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR
WEEK = 7 * DAY

class CatalogManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("CatalogManagerAI")

    def startCatalog(self):
        pass

    def deliverCatalogFor(self, toon):
        if not toon.air:
            return
            
        week = toon.getCatalogSchedule()[0] + 1
        
        gen = CatalogGenerator()
        
        mc = gen.generateMonthlyCatalog(toon, week // 4)
        wc = gen.generateWeeklyCatalog(toon, week, mc)
        bc = gen.generateBackCatalog(toon, week, week - 1, wc)
        
        toon.b_setCatalog(mc, wc, bc)
        toon.b_setCatalogSchedule(week, time.time() / 60.0 + WEEK / 60.0)
        toon.b_setCatalogNotify(ToontownGlobals.NewItems, toon.mailboxNotify)
        