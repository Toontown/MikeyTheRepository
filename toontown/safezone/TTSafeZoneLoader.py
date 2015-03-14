from pandac.PandaModules import *
import SafeZoneLoader
import TTPlayground
import random
from toontown.launcher import DownloadForceAcknowledge
from otp.nametag.NametagConstants import *
from toontown.toonbase import ToontownGlobals

class TTSafeZoneLoader(SafeZoneLoader.SafeZoneLoader):

    def __init__(self, hood, parentFSM, doneEvent):
        SafeZoneLoader.SafeZoneLoader.__init__(self, hood, parentFSM, doneEvent)
        self.playgroundClass = TTPlayground.TTPlayground
        self.musicFile = 'phase_4/audio/bgm/TC_nbrhood.ogg'
        self.activityMusicFile = 'phase_3.5/audio/bgm/TC_SZ_activity.ogg'
        self.dnaFile = 'phase_4/dna/toontown_central_sz.dna'
        self.safeZoneStorageDNAFile = 'phase_4/dna/storage_TT_sz.dna'
        self.sillyMeterSign1 = loader.loadModel('phase_4/models/props/tt_m_ara_ttc_sillyMeterSign_groupA')
        self.sillyMeterSign2 = loader.loadModel('phase_4/models/props/tt_m_ara_ttc_sillyMeterSign_groupB')

    def load(self):
        SafeZoneLoader.SafeZoneLoader.load(self)
        self.birdSound = map(base.loadSfx, ['phase_4/audio/sfx/SZ_TC_bird1.ogg', 'phase_4/audio/sfx/SZ_TC_bird2.ogg', 'phase_4/audio/sfx/SZ_TC_bird3.ogg'])
        safeZone = base.cr.playGame.hood.loader.geom
        if base.config.GetBool('want-silly-meter', True):
            self.sillyMeterSign1.reparentTo(safeZone)
            self.sillyMeterSign2.reparentTo(safeZone)
            self.sillyMeterSign1.setPos(100, 9, 4)
            self.sillyMeterSign2.setPos(100, -8.2, 4)
            self.sillyMeterSign1.setH(-90)
            self.sillyMeterSign2.setH(-90)

    def unload(self):
        del self.birdSound
        del self.sillyMeterSign1
        del self.sillyMeterSign2
        SafeZoneLoader.SafeZoneLoader.unload(self)

    def enter(self, requestStatus):
        SafeZoneLoader.SafeZoneLoader.enter(self, requestStatus)

    def exit(self):
        SafeZoneLoader.SafeZoneLoader.exit(self)
