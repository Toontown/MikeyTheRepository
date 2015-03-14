from direct.distributed.AstronInternalRepository import AstronInternalRepository, PyDatagram, CLIENTAGENT_DROP
from otp.distributed.OtpDoGlobals import *
import sys, traceback

class ToontownInternalRepository(AstronInternalRepository):
    GameGlobalsId = OTP_DO_ID_TOONTOWN
    dbId = 4003
    
    def __init__(self, baseChannel, serverId=None, dcFileNames = None,
                 dcSuffix = 'AI', connectMethod = None, threadedNet = None):
        if connectMethod is None:
            connectMethod = self.CM_NATIVE
            
        AstronInternalRepository.__init__(self, baseChannel, serverId, dcFileNames, dcSuffix, connectMethod, threadedNet)
        
    def readerPollOnce(self):
        try:
            return AstronInternalRepository.readerPollOnce(self)
            
        except SystemExit, KeyboardInterrupt:
            raise
            
        except Exception as e:            
            if config.GetBool('want-kick-crasher', True):
                if self.getAvatarIdFromSender() > 100000000:
                    # remove the av that caused the exception
                    # since it could be a harmful hacker
                    # or simply because it could break some logic
                    dg = PyDatagram()
                    dg.addServerHeader(self.getMsgSender(), self.ourChannel, CLIENTAGENT_EJECT)
                    dg.addUint16(166)
                    dg.addString('You were disconnected to prevent a district reset.')
                    self.send(dg)
                
            self.writeServerEvent('INTERNAL-EXCEPTION', self.getAvatarIdFromSender(), self.getAccountIdFromSender(), repr(e), traceback.format_exc())
            self.notify.warning('INTERNAL-EXCEPTION: %s (%s)' % (repr(e), self.getAvatarIdFromSender()))
            print traceback.format_exc()
            sys.exc_clear()
            
        return 1

    def getAvatarIdFromSender(self):
        return self.getMsgSender() & 0xFFFFFFFF

    def getAccountIdFromSender(self):
        return (self.getMsgSender()>>32) & 0xFFFFFFFF

    def _isValidPlayerLocation(self, parentId, zoneId):
        if zoneId < 1000 and zoneId != 1:
            return False

        return True

    def sendSysMsgToAll(self, message):
        msgDg = PyDatagram()
        msgDg.addUint16(6)
        msgDg.addString(message)

        dg = PyDatagram()
        dg.addServerHeader(10, self.ourChannel, CLIENTAGENT_SEND_DATAGRAM)
        dg.addString(msgDg.getMessage())
        self.send(dg)
    