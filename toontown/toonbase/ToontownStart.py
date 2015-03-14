from pandac.PandaModules import *
import __builtin__

# NOTE: In the future, we'll provide tools to make content packs.
# These tools will carefully check if only textures and audios were edited.

#Content Packs.
#EXPERIMENTAL!!!!
import os
wantPacks = 0 #ConfigVariableBool('want-packs', 1)

if wantPacks:
 if os.path.isdir("res/"):
  if os.access('res/phase_3.mf', os.R_OK) and os.access('res/phase_3.5.mf', os.R_OK) and os.access('res/phase_4.mf', os.R_OK) and os.access('res/phase_5.mf', os.R_OK) and os.access('res/phase_5.5.mf', os.R_OK) and os.access('res/phase_6.mf', os.R_OK) and os.access('res/phase_7.mf', os.R_OK) and os.access('res/phase_8.mf', os.R_OK) and os.access('res/phase_9.mf', os.R_OK) and os.access('res/phase_10.mf', os.R_OK) and os.access('res/phase_11.mf', os.R_OK) and os.access('res/phase_12.mf', os.R_OK):
   loadPrcFileData('', 'model-path res/')
   loadPrcFileData('', 'vfs-mount phase_3.mf /')
   loadPrcFileData('', 'vfs-mount phase_3.5.mf /')
   loadPrcFileData('', 'vfs-mount phase_4.mf /')
   loadPrcFileData('', 'vfs-mount phase_5.mf /')
   loadPrcFileData('', 'vfs-mount phase_5.5.mf /')
   loadPrcFileData('', 'vfs-mount phase_6.mf /')
   loadPrcFileData('', 'vfs-mount phase_7.mf /')
   loadPrcFileData('', 'vfs-mount phase_8.mf /')
   loadPrcFileData('', 'vfs-mount phase_9.mf /')
   loadPrcFileData('', 'vfs-mount phase_10.mf /')
   loadPrcFileData('', 'vfs-mount phase_11.mf /')
   loadPrcFileData('', 'vfs-mount phase_12.mf /')
   loadPrcFileData('', 'vfs-mount phase_13.mf /')
   print 'ToontownStart: Pack Found.'
 else:
   print 'ToontownStart: No pack found. Using default.'
   getModelPath().appendDirectory("resources")
   if not __debug__:
    loadPrcFileData('', 'model-path /')
    loadPrcFileData('', 'vfs-mount phase_3.mf /')
    loadPrcFileData('', 'vfs-mount phase_3.5.mf /')
    loadPrcFileData('', 'vfs-mount phase_4.mf /')
    loadPrcFileData('', 'vfs-mount phase_5.mf /')
    loadPrcFileData('', 'vfs-mount phase_5.5.mf /')
    loadPrcFileData('', 'vfs-mount phase_6.mf /')
    loadPrcFileData('', 'vfs-mount phase_7.mf /')
    loadPrcFileData('', 'vfs-mount phase_8.mf /')
    loadPrcFileData('', 'vfs-mount phase_9.mf /')
    loadPrcFileData('', 'vfs-mount phase_10.mf /')
    loadPrcFileData('', 'vfs-mount phase_11.mf /')
    loadPrcFileData('', 'vfs-mount phase_12.mf /')
    loadPrcFileData('', 'vfs-mount phase_13.mf /')
else:
 print 'ToontownStart: Content Packs Disabled.'
 getModelPath().appendDirectory("resources")
 if not __debug__:
   loadPrcFileData('', 'model-path /')
   loadPrcFileData('', 'vfs-mount phase_3.mf /')
   loadPrcFileData('', 'vfs-mount phase_3.5.mf /')
   loadPrcFileData('', 'vfs-mount phase_4.mf /')
   loadPrcFileData('', 'vfs-mount phase_5.mf /')
   loadPrcFileData('', 'vfs-mount phase_5.5.mf /')
   loadPrcFileData('', 'vfs-mount phase_6.mf /')
   loadPrcFileData('', 'vfs-mount phase_7.mf /')
   loadPrcFileData('', 'vfs-mount phase_8.mf /')
   loadPrcFileData('', 'vfs-mount phase_9.mf /')
   loadPrcFileData('', 'vfs-mount phase_10.mf /')
   loadPrcFileData('', 'vfs-mount phase_11.mf /')
   loadPrcFileData('', 'vfs-mount phase_12.mf /')
   loadPrcFileData('', 'vfs-mount phase_13.mf /')

if __debug__:
    loadPrcFile('dev.prc')
    
    # let's check if they edited the prc server stuff
    config = getConfigExpress()
    defaultServer = '127.0.0.1'
    if config.GetString('game-server', defaultServer) != defaultServer:
        print 'YOU EDITED THE PRC SERVER!!!'
        print 'DO NOT DO THIS!!'
        print 'USE "-s IP" INSTEAD!'
        
    defaultToken = 'dev'
    if config.GetString('fake-playtoken', defaultToken) != defaultToken:
        print 'YOU EDITED THE PRC TOKEN!!!'
        print 'DO NOT DO THIS!!'
        print 'USE "-t TOKEN" INSTEAD!'

class game:
    name = 'toontown'
    process = 'client'

__builtin__.game = game()

import time, os, sys, random

customServer = False
if '-s' in sys.argv:
    server = sys.argv[sys.argv.index('-s') + 1]
    
    if __debug__:
        if server == "lc":
            server = "173.237.116.184"

    customServer = True
    loadPrcFileData('', 'game-server ' + server)

if '-t' in sys.argv:
	token = sys.argv[sys.argv.index('-t') + 1]
	loadPrcFileData('', 'fake-playtoken ' + token)

else:
    if customServer:
        print 'You must use a token (-t) with -s!'
        exit()
    
if '-l' in sys.argv:
    langMap = {'pt': 'portuguese', 'en': 'english', 'fr': 'french'}
    lang = sys.argv[sys.argv.index('-l') + 1]
    
    if lang == "en":
        print 'WARNING: default language is already English!'
       
    elif lang not in langMap:
        print 'ERROR: invalid lang', lang
        print 'THE LANGUAGES ARE:'
        for l in langMap:
            print '\t', l
          
        print

    loadPrcFileData('', 'language ' + langMap[lang])

from toontown.launcher.TTLauncher import TTLauncher
__builtin__.launcher = TTLauncher()

print 'ToontownStart: Starting the game.'
    
tempLoader = Loader()
backgroundNode = tempLoader.loadSync(Filename('phase_3/models/gui/loading-background'))

from direct.gui import DirectGuiGlobals
import ToontownGlobals
DirectGuiGlobals.setDefaultFontFunc(ToontownGlobals.getInterfaceFont)

launcher.setPandaErrorCode(7)

# base
import ToonBase
ToonBase.ToonBase()

if base.win == None:
    print 'Unable to open window; aborting.'
    sys.exit()
    
launcher.setPandaErrorCode(0)
launcher.setPandaWindowOpen()

ConfigVariableDouble('decompressor-step-time').setValue(0.01)
ConfigVariableDouble('extractor-step-time').setValue(0.01)

# loading screen
backgroundNodePath = aspect2d.attachNewNode(backgroundNode, 0)
backgroundNodePath.setPos(0.0, 0.0, 0.0)
backgroundNodePath.setScale(render2d, VBase3(1))
backgroundNodePath.find('**/bg').setBin('fixed', 10)

# change the logo
backgroundNodePath.find('**/fg').stash()

from direct.gui.DirectGui import OnscreenImage
logo = OnscreenImage('phase_3/maps/toontown-logo-new.png')
logo.reparentTo(backgroundNodePath)
logo.setBin('fixed', 20)
logo.setTransparency(TransparencyAttrib.MAlpha)

base.graphicsEngine.renderFrame()

# default DGG stuff
DirectGuiGlobals.setDefaultRolloverSound(base.loadSfx('phase_3/audio/sfx/GUI_rollover.ogg'))
DirectGuiGlobals.setDefaultClickSound(base.loadSfx('phase_3/audio/sfx/GUI_create_toon_fwd.ogg'))
DirectGuiGlobals.setDefaultDialogGeom(loader.loadModel('phase_3/models/gui/dialog_box_gui'))

# localizer
import TTLocalizer
from otp.otpbase import OTPGlobals
OTPGlobals.setDefaultProductPrefix(TTLocalizer.ProductPrefix)

wantSpecial = base.config.GetBool('wantSpecialTheme', 0)

# loading music
music = None
if base.musicManagerIsValid:
    music = base.musicManager.getSound('phase_3/audio/bgm/tt_theme.ogg')
    if wantSpecial:
     music = base.musicManager.getSound('phase_5/audio/bgm/TT_Theme.ogg')
    if music:
        music.setLoop(1)
        music.setVolume(0.9)
        music.play()

# loader
import ToontownLoader
from direct.gui.DirectGui import *
serverVersion = base.config.GetString('server-version', 'no_version_set')
version = OnscreenText(serverVersion, pos=(-1.3, -0.975), scale=0.06, fg=Vec4(0, 0, 1, 0.6), align=TextNode.ALeft)
loader.beginBulkLoad('init', TTLocalizer.LoaderLabel, 50, 0, TTLocalizer.TIP_NONE)
from ToonBaseGlobal import *
from direct.showbase.MessengerGlobal import *

# cr
from toontown.distributed import ToontownClientRepository
cr = ToontownClientRepository.ToontownClientRepository(serverVersion, launcher)
cr.setDeferInterval(1)
cr.music = music
del music
base.initNametagGlobals()
base.cr = cr
loader.endBulkLoad('init')

# friend mgr
from otp.friends import FriendManager
from otp.distributed.OtpDoGlobals import *
cr.generateGlobalObject(OTP_DO_ID_FRIEND_MANAGER, 'FriendManager')

# start
base.startShow(cr)

# cleanup
backgroundNodePath.reparentTo(hidden)
backgroundNodePath.removeNode()
del backgroundNodePath
del backgroundNode
del tempLoader
del logo
version.cleanup()
del version

try:
    run()
    
except SystemExit:
    try:
        __nirai__
    
    except:
        raise SystemExit
    
except KeyboardInterrupt:
    raise
    
except:
    try:
        base.cr.timeManager.setDisconnectReason(3)
    
    except:
        pass
        
    raise
    