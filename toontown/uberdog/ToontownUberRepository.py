import toontown.minigame.MinigameCreatorAI
from toontown.distributed.ToontownInternalRepository import ToontownInternalRepository
from direct.distributed.PyDatagram import *
from otp.distributed.DistributedDirectoryAI import DistributedDirectoryAI
from otp.distributed.OtpDoGlobals import *

from ShardAPIManagerUD import ShardAPIManagerUD
import ShardAPIWebServer

from toontown.hood import ZoneUtil
from toontown.toonbase import ToontownGlobals
from libpandadna import DNALoader, DNAStorage

from BanManagerUD import BanManagerUD

class ToontownUberRepository(ToontownInternalRepository):
    def __init__(self, baseChannel, serverId):
        ToontownInternalRepository.__init__(self, baseChannel, serverId, dcSuffix = 'UD')
        self.__loader = DNALoader.DNALoader()
        self.__dnaMap = {}
        
    def getDnaStore(self, zoneId):
        if zoneId in self.__dnaMap:
            return self.__dnaMap[zoneId]
            
        x = DNAStorage.DNAStorage()
        filename = self.genDNAFileName(zoneId)
        
        print 'Loading dna file', self.genDNAFileName(zoneId)
        self.loadDNAFileAI(x, filename)
        
        self.__dnaMap[zoneId] = x
        
        return x
        
    def handleConnected(self):
        rootObj = DistributedDirectoryAI(self)
        rootObj.generateWithRequiredAndId(self.getGameDoId(), 0, 0)
        
        self.apiMgr = ShardAPIManagerUD(self)
        self.apiMgr.generateWithRequiredAndId(100001, 0, 0)
        
        self.banMgr = BanManagerUD(self)
        self.banMgr.generateWithRequiredAndId(100002, 0, 0)

        self.createGlobals()
        
        self.apiWS = ShardAPIWebServer.start(self.apiMgr)

    def createGlobals(self):
        self.csm = simbase.air.generateGlobalObject(OTP_DO_ID_CLIENT_SERVICES_MANAGER,
                                                    'ClientServicesManager')

        self.chatAgent = simbase.air.generateGlobalObject(OTP_DO_ID_CHAT_MANAGER,
                                                          'ChatAgent')
        
        self.friendsManager = simbase.air.generateGlobalObject(OTP_DO_ID_TT_FRIENDS_MANAGER,
                                                               'TTFriendsManager')

        self.globalPartyMgr = simbase.air.generateGlobalObject(OTP_DO_ID_GLOBAL_PARTY_MANAGER, 'GlobalPartyManager')
        
    def genDNAFileName(self, zoneId):
        zoneId = ZoneUtil.getCanonicalZoneId(zoneId)
        hoodId = ZoneUtil.getCanonicalHoodId(zoneId)
        hood = ToontownGlobals.dnaMap[hoodId]
        if hoodId == zoneId:
            zoneId = 'sz'
            phase = ToontownGlobals.phaseMap[hoodId]
        else:
            phase = ToontownGlobals.streetPhaseMap[hoodId]

        return 'phase_%s/dna/%s_%s.dna' % (phase, hood, zoneId)

    def loadDNAFileAI(self, dnastore, filename):
        f = Filename('resources/' + str(filename))
        f.setExtension('pdna')            
        x = self.__loader.loadDNAFileAI(dnastore, f)
        