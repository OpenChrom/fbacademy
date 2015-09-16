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

#
# Parse all listed files.
#
for file in ['DAD1A.ch','DAD1B.ch','DAD1C.ch']:
	#
	# Create the binary file handle.
	#
	f = open(file, 'rb')
	#
	# Wavelength
	#
	f.seek(0x108B)
	bytes = struct.unpack('>6B', f.read(6))
	print "---------------------------"
	print "File: ", file
	print "Wavelength: ", chr(bytes[1]) + chr(bytes[3]) + chr(bytes[5])
	print "---------------------------"
	#
	# Data
	#
	f.seek(0x1800)
	f.read(2)
	#
	intensity = 0
	marker = 0
	toggle = 0
	#
	readData = 1
	readFile = 1
	#
	while(readFile == 1):
		try:
			#
			# Pre-evaluate
			#
			delta = struct.unpack('>h', f.read(2))[0]
			if delta == 0x1019 or delta == 0x101A or delta == 0x1033:
				readData = 0
				if delta == 0x101A:
					deltaNext = struct.unpack('>h', f.read(2))[0]
					if abs(delta - deltaNext) <= 0xFF:
						#
						# Add 2x
						#
						intensity += delta
						print intensity
						intensity += deltaNext
						print intensity
					else:
						#
						# Skip
						#
						f.seek(f.tell() - 2)
			else:
				readData = 1
			
			#
			# Data
			#
			if readData == 1:
				if delta == 0x1032:
					deltaNext = struct.unpack('>h', f.read(2))[0]
					if deltaNext == 0x10FF and abs(delta - deltaNext) <= 0xFF:
						#
						# Add 2x
						#
						intensity += delta
						print intensity
						intensity += deltaNext
						print intensity
					else:
						#
						# Skip
						#
						f.seek(f.tell() - 2)
					
				else:
					#
					# 80 00 (-32768)
					#
					if delta == -32768:
						delta = struct.unpack('>i', f.read(4))[0]
						intensity = delta
						print intensity
					else:
						deltaNext = struct.unpack('>h', f.read(2))[0]
						if deltaNext == 0x1032 and abs(delta - deltaNext) <= 0xFF:
							#
							# Add 2x
							#
							intensity += delta
							print intensity
							intensity += deltaNext
							print intensity
						else:
							#
							# Add 1x
							#
							f.seek(f.tell() - 2)
							intensity += delta
							print intensity
		except struct.error:
			readFile = 0
		

