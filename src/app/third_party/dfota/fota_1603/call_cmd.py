import os
import sys
import traceback
import subprocess


DFOTA_DIR = '/airm2m_data/airm2m/projects/giant-rat/third_party/dfota/'
FIRMWARE_DIR = '/airm2m_data/airm2m/files/firmware/'

print('gg')
#print(sys.argv[0])
#print(sys.argv[1])

dfota_file_name = '123'

if True:
	with open(DFOTA_DIR + 'fota_1603/dfota_file_name', 'r') as f:
		#if True:
		dfota_file_name = f.read()
		print('dfota_file_name = %s' % dfota_file_name)
		#dfota_file_name = 'gg.bbb'

print('dfota_file_name = %s' % dfota_file_name)

#cmd = "%s -p %s %s %s" % (DFOTA_DIR + 'fota_1603/adiff_lnx', DFOTA_DIR + 'a/system.img', DFOTA_DIR + 'b/system.img', FIRMWARE_DIR + dfota_file_name)

#cmd = "%s -p %s %s %s" % (DFOTA_DIR + 'fota_1603/adiff_lnx', DFOTA_DIR + 'a/system.img', DFOTA_DIR + 'b/system.img', DFOTA_DIR + 'fota_1603/' + dfota_file_name)

cmd = "%s -p %s %s %s" % (DFOTA_DIR + 'fota_1603/adiff_lnx', DFOTA_DIR + 'a/system.img', DFOTA_DIR + 'b/system.img', 'ggg')

#print(cmd)
print(cmd.split())
result = subprocess.call(cmd.split())
print(result)









