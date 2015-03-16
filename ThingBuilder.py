import os
import sys

print 'Building the client...'

#toontown
modules = ['toontown', 'otp', 'direct', 'pandac']
output = 'TTHREngine.exe'
main_module = 'toontown.toonbase.ToontownStart'
"""
#otp
modules = ['otp']
output = 'otp.dll'
main_module = 'otp.main'
#p3d
modules = ['direct', 'pandac']
output = 'panda3d.dll'
"""


#os.system('../')

cmd = sys.executable + ' -m direct.showutil.pfreeze'
#modules.extend(['direct', 'pandac'])
for module in modules:
    cmd += ' -i %s.*.*' % module
cmd += ' -i encodings.*'
cmd += ' -i base64'
cmd += ' -i site'
cmd += ' -o ' + output
cmd += ' ' + main_module
os.system(cmd)
#print cmd
