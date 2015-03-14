import setup

from pandac.PandaModules import *
from direct.showbase import PythonUtil

import argparse, __builtin__

parser = argparse.ArgumentParser()
parser.add_argument('--base-channel', help='The base channel that the server may use.')
parser.add_argument('--max-channels', help='The number of channels the server may use.')
parser.add_argument('--stateserver', help="The control channel of this AI's designated State Server.")
parser.add_argument('--district-name', help="What this AI Server's district will be named.")
parser.add_argument('--allow-boss-cheat', default="t", help="Enable/Disable boss cheats.")
parser.add_argument('--astron-ip', help="The IP address of the Astron Message Director to connect to.")
parser.add_argument('--eventlogger-ip', default='localhost:7197', help="The IP address of the Astron Event Logger to log to.")
parser.add_argument('--config', default='dev.prc', help="PRC file(s) to load.")
args = parser.parse_args()

loadPrcFileData('', 'allow-boss-cheat #' + args.allow_boss_cheat)
print 'Boss cheats are allowed?', getConfigExpress().GetBool('allow-boss-cheat')

if args.config:
    prc = args.config
    loadPrcFile(prc)

localconfig = ''
if args.base_channel: localconfig += 'air-base-channel %s\n' % args.base_channel
if args.max_channels: localconfig += 'air-channel-allocation %s\n' % args.max_channels
if args.stateserver: localconfig += 'air-stateserver %s\n' % args.stateserver
if args.district_name: localconfig += 'district-name %s\n' % args.district_name
if args.astron_ip: localconfig += 'air-connect %s\n' % args.astron_ip
if args.eventlogger_ip: localconfig += 'eventlog-host %s\n' % args.eventlogger_ip
loadPrcFileData('cmd', localconfig)

class game:
    name = 'toontown'
    process = 'server'
__builtin__.game = game

from otp.ai.AIBaseGlobal import *

from toontown.ai.ToontownAIRepository import ToontownAIRepository
simbase.air = ToontownAIRepository(config.GetInt('air-base-channel', 401000000),
                                   config.GetInt('air-stateserver', 10000),
                                   config.GetString('district-name', 'Devhaven'))
host = config.GetString('air-connect', '127.0.0.1')
port = 7199
if ':' in host:
    host, port = host.split(':', 1)
    port = int(port)
simbase.air.connect(host, port)

try:
    run()
except SystemExit:
    raise
except Exception:
    info = PythonUtil.describeException()
    simbase.air.writeServerEvent('ai-exception', simbase.air.getAvatarIdFromSender(), simbase.air.getAccountIdFromSender(), info)
    raise