from pandac.PandaModules import *
from direct.directnotify.DirectNotifyGlobal import *
from direct.showbase import Loader
from toontown.toontowngui import ToontownLoadingScreen

if config.GetBool('use-libpandadna', False):
    if config.GetBool('libpandadna-pyreader', True):
        from libpandadna.DNALoader import DNALoader
        C2 = DNALoader
        
    else:
        import libpandadna
        C2 = libpandadna.DNALoader
    
class ToontownLoader(Loader.Loader, C2):
    TickPeriod = 0.2

    def __init__(self, base):
        Loader.Loader.__init__(self, base)
        C2.__init__(self)
        self.inBulkBlock = None
        self.blockName = None
        self.loadingScreen = ToontownLoadingScreen.ToontownLoadingScreen()
        
        self.loadModelNode = self.loadModel

    def destroy(self):
        self.loadingScreen.destroy()
        del self.loadingScreen
        Loader.Loader.destroy(self)

    def loadDNAFile(self, dnastore, file):
        self.notify.info('Loading DNA file %s' % file)
        self.tick()
        
        if config.GetBool('use-libpandadna', False):
            f = Filename(str(file))
            f.setExtension('pdna')
            f = localizerAgent.findDNA(f)
            ret = C2.loadDNAFile(self, dnastore, f)
            
            if ret.getChild(0).getNumChildren() > 0:
                ret = ret.getChild(0).getChild(0).getNode(0)
                
            else:
                ret = None
            
        else:
            f = Filename(filename)
            f = Filename('etc/dnabkp/' + f.getBasename())
            ret = loadDNAFile(dnastore, f)
            
        self.notify.info('DNA file loaded')
        return ret
        
    def loadDNAFileAI(self, dnastore, filename):
        self.tick()
        
        f = Filename('resources/' + str(filename))
        f.setExtension('pdna')
        return C2.loadDNAFileAI(self, dnastore, f)

    def beginBulkLoad(self, name, label, range, gui, tipCategory):
        self._loadStartT = globalClock.getRealTime()
        Loader.Loader.notify.info("starting bulk load of block '%s'" % name)
        if self.inBulkBlock:
            Loader.Loader.notify.warning("Tried to start a block ('%s'), but am already in a block ('%s')" % (name, self.blockName))
            return None
        self.inBulkBlock = 1
        self._lastTickT = globalClock.getRealTime()
        self.blockName = name
        
        if name == "hood":
            range *= 40
            
        self.loadingScreen.begin(range, label, gui, tipCategory)

    def endBulkLoad(self, name):
        if not self.inBulkBlock:
            Loader.Loader.notify.warning("Tried to end a block ('%s'), but not in one" % name)
            return None
        if name != self.blockName:
            Loader.Loader.notify.warning("Tried to end a block ('%s'), other then the current one ('%s')" % (name, self.blockName))
            return None
        self.inBulkBlock = None
        expectedCount, loadedCount = self.loadingScreen.end()
        now = globalClock.getRealTime()
        Loader.Loader.notify.info("At end of block '%s', expected %s, loaded %s, duration=%s" % (self.blockName,
         expectedCount,
         loadedCount,
         now - self._loadStartT))
        return

    def abortBulkLoad(self):
        if self.inBulkBlock:
            Loader.Loader.notify.info("Aborting block ('%s')" % self.blockName)
            self.inBulkBlock = None
            self.loadingScreen.abort()
        return

    def tick(self):
        if self.inBulkBlock:
            now = globalClock.getRealTime()
            if now - self._lastTickT > self.TickPeriod:
                self._lastTickT += self.TickPeriod
                self.loadingScreen.tick()
                try:
                    base.cr.considerHeartbeat()
                except:
                    pass

    def loadModel(self, *args, **kw):
        ret = Loader.Loader.loadModel(self, *args, **kw)
        self.tick()
        return ret

    def loadFont(self, *args, **kw):
        ret = Loader.Loader.loadFont(self, *args, **kw)
        self.tick()
        return ret

    def loadTexture(self, texturePath, alphaPath = None, okMissing = False):
        ret = Loader.Loader.loadTexture(self, texturePath, alphaPath, okMissing=okMissing)
        self.tick()
        if alphaPath:
            self.tick()
        return ret

    def loadSfx(self, soundPath):
        ret = Loader.Loader.loadSfx(self, soundPath)
        self.tick()
        return ret

    def loadMusic(self, soundPath):
        ret = Loader.Loader.loadMusic(self, soundPath)
        self.tick()
        return ret
