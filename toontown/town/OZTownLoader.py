import TownLoader
import OZStreet
from toontown.suit import Suit

class OZTownLoader(TownLoader.TownLoader):

    def __init__(self, hood, parentFSM, doneEvent):
        TownLoader.TownLoader.__init__(self, hood, parentFSM, doneEvent)
        self.streetClass = OZStreet.OZStreet
        self.musicFile = 'phase_6/audio/bgm/OZ_nbrhood.ogg'
        self.activityMusicFile = self.musicFile
        self.townStorageDNAFile = 'phase_14/dna/storage_OZ_town.dna'

    def load(self, zoneId):
        TownLoader.TownLoader.load(self, zoneId)
        Suit.loadSuits(3)
        dnaFile = 'phase_14/dna/outdoor_zone_' + str(self.canonicalBranchZone) + '.dna'
        self.createHood(dnaFile)

    def unload(self):
        Suit.unloadSuits(3)
        TownLoader.TownLoader.unload(self)
