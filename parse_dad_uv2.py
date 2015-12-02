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
import sys

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

# Get starting addresses of each scan
for scan in range(scans):
  vals = struct.unpack('<IHI', f.read(10))
  startAddresses += [vals[2]]
  current_position = f.tell()

  if initial == True: # first value gives size of file? so ignore it
    initial = False
    continue

  f.seek(current_position)

# temporary variables
currTime = None
timeSlice = None
first = True
second = True
intensity = 0

count = 0
workingSet = 226 # how many wavelengths to output

mainList = [] # list of all scans
tempList = [] # temporary list contains data for all wavelengths during one scan
timeList = [] # list of times

for start in startAddresses:
  # get time
  f.seek(start)
  val = struct.unpack('<hhHh', f.read(8))
  if first:
    currTime = val[2]
    first = False
  elif not first and second:
    timeSlice = val[2] - currTime
    currTime += timeSlice
    second = False
  else:
    currTime += timeSlice
  timeList.append(currTime/60000.0)

  f.seek(start + 22) # seek to start of scan data (go past initial header)
  tempList = []

  # get value
  for i in range(workingSet): 
    delta = struct.unpack('<h', f.read(2))[0]
    if delta == -32768:
      delta = struct.unpack('<i', f.read(4))[0]
      intensity = delta
    else:
      intensity += delta
    tempList.append(intensity)
  mainList.append(tempList)

# print header
print "time,",
for i in range(workingSet):
  sys.stdout.write(str(190 + i*2))
  if not i == workingSet - 1:
    print ",",
print

# print comma-separated values
for i in range(len(mainList)):
  print str(timeList[i]) + ",", # print time
  for j in range(workingSet):
    sys.stdout.write(str(mainList[i][j])) # print values for all wavelengths
    if not j == workingSet - 1:
      print ",",
  print