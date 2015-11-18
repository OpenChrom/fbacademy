#*******************************************************************************
# Copyright (c) 2015 Dr. Philip Wenig
#
# All rights reserved.
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License v1.0 which accompanies this distribution,
# and is available at http://www.eclipse.org/legal/epl-v10.html
#
# Contributors:
# Dr. Philip Wenig
#*******************************************************************************/
import struct
import math

f = open("DAD1.UV", "rb")
#
# The data seems to start at position 0x1000
#
data_offset=0x1000
#
# A look at the file shows, that there seems
# to be a header part at the end of the file.
# A comparison of the files let me assume, that
# the header position start is encoded at
# position 0x104
#
f.seek(0x104)
header_offset = struct.unpack('>I', f.read(4))[0]
#
# This could be the field where the number of scans
# is encoded.
#
f.seek(0x116)
scans = struct.unpack('>I', f.read(4))[0]
#
# Try to make some basic calculations.
#
bytes_per_scan = ((header_offset - data_offset) / scans)
wavelengths = (bytes_per_scan / 2)
#
print "-----------------------"
print "DATA OFFSET: ", data_offset
print "HEADER OFFSET: ", header_offset
print "NUMBER OF SCANS: ", scans
print "BYTES PER SCANS: ", bytes_per_scan
print "NUMBER OF WAVELENGTHS: ",  wavelengths
print "-----------------------"
#
# The retention time for each scan
# seems to be encoded in the header.
#
initial = True
startAddresses = []
f.seek(header_offset)

for scan in range(scans):
  vals = struct.unpack('<IHI', f.read(10))
  startAddresses += [vals[2]]
  current_position = f.tell()

  if initial == True: # first value gives size of file? so ignore it
    initial = False
    continue

  # print vals
  f.seek(current_position)
  # print scan, '{:.2f}'.format(vals[0]/60000.0)
  # print scan, '{:.2f}'.format(vals[0]/60000.0), vals[1], vals[2]

currTime = None
timeSlice = None
first = True
second = True
count = 0
for start in startAddresses:
  # go to start of scan data
  f.seek(start + 24)

  val = struct.unpack('<i', f.read(4))
  print val[0]
  # size of current section?, current second?
  # print val[1], val[3],
  # if first:
  #   currTime = val[2]
  #   print currTime/60000.0
  #   first = False
  # elif not first and second:
  #   timeSlice = val[2] - currTime
  #   currTime += timeSlice
  #   print currTime/60000.0
  #   second = False
  # else:
  #   currTime += timeSlice
  #   print currTime/60000.0

#
# Try to read the scans.
#
# f.seek(data_offset)
# for scan in range(scans):
#   vals = struct.unpack('<' + wavelengths * 'h', f.read(wavelengths * 2))


