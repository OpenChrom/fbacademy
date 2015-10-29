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
import os

# each index is a different time period
# each index should contain all wavelengths
# need to figure out what 0080 means

filePath1 = 'Rice Data/150319/150319 2015-03-19 17-06-40/3-1.D/DAD1.UV'
for file in [filePath1]:
	f = open(file, 'rb');
	
	readFile = 1;
	f.seek(0x1018);
	times = []; 
	intensity = 0;
	currIteration = [];
	
	# attempting to get first number of each block
	while True:
		try:
			delta = struct.unpack('>h', f.read(2))[0];

			# check for known stopbytes here

			intensity += delta;
			currIteration += [intensity];
			# currIteration += [delta];
			# print currIteration

			if delta == -10226: #d80e
				f.seek(f.tell() - 10)

				for x in range(12):
					if x < 4:
						intensity -= struct.unpack('>h', f.read(2))[0];
					# print address in hex
					# print format(f.tell(), '04x')
					else: 
						# skip over rest of stop byte section
						struct.unpack('>h', f.read(2))[0];

				times.append(list(currIteration[:-5]));
				currIteration = [];

				iteration = 0; # may or may not be wanted 

		except struct.error:
			break;


# print first element of each iteration?
for x in times:
	print x[0];

# len(times) = 4988
# on the money ish, very close to 4950




################

# #
# # Parse all listed files.
# #

# dir1 = 'YUF13 9-15-1.D'
# dir2 = 'YUF13 9-15-2.D'
# filePath1 = 'Rice Data/150319/150319 2015-03-19 17-06-40/' + dir1 + '/DAD1.UV'
# filePath2 = 'Rice Data/150319/150319 2015-03-19 17-06-40/' + dir2 + '/DAD1.UV'

# f1 = open(filePath1, 'rb')
# f2 = open(filePath2, 'rb')

# out = open('out_' + dir1 + '_' + dir2, 'w')

# readFile = 1
# counter = 0
# strBuf = ""
# tupleArray = []
# address = 0

# print "Working..."

# while readFile == 1:
# 	try:
# 		address += 1
# 		byte1 = struct.unpack('>B', f1.read(1))
# 		byte2 = struct.unpack('>B', f2.read(1))
# 		if byte1 == byte2:
# 			strBuf += str(byte1)
# 			counter += 1
# 		else:
# 			if counter > 0:
# 				tupleArray.append([strBuf, counter, address])
# 			strBuf = ""
# 			counter = 0
# 	except struct.error:
# 		readFile = 0

# tupleArray.sort(key=lambda x: x[1])
# tupleArray.reverse()

# common4 = filter(lambda x: x[1] == 4, tupleArray)
# common4.sort(key=lambda x: x[2])

# print "Done, writing to file."

# out.write(dir1 + '_' + dir2 + '\n')

# for num in common4:
# 	out.write(str(num) + '\n')

# out.close()
# # # # # #
#
#
#
#
#


# sizeOfNum = 8 # type of number

# for offset in range(sizeOfNum): 

# 	toWrite = open('toWrite-' + str(sizeOfNum) + '-' + str(offset), 'w')

# 	for file in ['DAD1.UV']:
# 		f = open(file, 'rb')
# 		readFile = 1
# 		while readFile == 1:
# 			try:
# 				floats = struct.unpack('d', f.read(sizeOfNum))
# 				toWrite.write(str(floats[0]) + '\n')
# 			except struct.error:
# 				readFile = 0

# 	toWrite.close()