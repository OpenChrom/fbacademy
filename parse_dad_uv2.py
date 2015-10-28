#*******************************************************************************
# Copyright (c) 2015 Dr. Philip Wenig
#
# All rights reserved.
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License v1.0 which accompanies this distribution,
# and is available at http://www.eclipse.org/legal/epl-v10.html
# 
# Contributors:
#	Dr. Philip Wenig
#*******************************************************************************/
import struct
import math

f = open("DAD1.UV", "rb")
#
#
#
data_offset=0x1000
f.seek(0x104)
header_offset = struct.unpack('>I', f.read(4))[0]

f.seek(0x116)
scans = struct.unpack('>I', f.read(4))[0]
print "-----------------------"
print "DATA OFFSET: ", data_offset
print "HEADER OFFSET: ", header_offset
print "SCANS: ", scans
bytes_per_scan = ((header_offset - data_offset) / scans)
print "BYTES PER SCANS: ", bytes_per_scan
wavelengths = (bytes_per_scan / 2)
print "WAVELENGTHS?: ",  wavelengths
print "-----------------------"

f.seek(header_offset)
for scan in range(scans):
	vals = struct.unpack('<IHI', f.read(10))
	print scan, '{:.2f}'.format(vals[0]/60000.0), vals[1], vals[2] 

print "-----------------------"

f.seek(data_offset)
for scan in range(scans):
	vals = struct.unpack('<' + wavelengths * 'h', f.read(wavelengths * 2))		
	print vals
		

