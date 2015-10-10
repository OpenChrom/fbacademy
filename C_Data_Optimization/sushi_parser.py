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

#
# Parse all listed files.
#
INTERESTED_FILE = 'DAD1C.ch'
RICE_TYPE = 'SUSHI'

results = []
working_directory = os.getcwd()
sub_dirs = os.listdir(working_directory)

for directory in sub_dirs:
	if RICE_TYPE in directory:
		for files in os.listdir(working_directory + "/" + directory):

			current_results = []
			
			if INTERESTED_FILE == files:
				f = open(working_directory + "/" + directory + "/" + files, 'rb')
				#
				# Wavelength
				#
				f.seek(0x108B)
				bytes = struct.unpack('>6B', f.read(6))
				# temp_string = "Wavelength: ", chr(bytes[1]) + chr(bytes[3]) + chr(bytes[5])
				# current_results.append( temp_string );
				# current_results.append( "--------------------------" );
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
									current_results.append( intensity );
									intensity += deltaNext
									current_results.append( intensity );
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
									current_results.append( intensity );
									intensity += deltaNext
									current_results.append( intensity );
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
									current_results.append( intensity );
								else:
									deltaNext = struct.unpack('>h', f.read(2))[0]
									if deltaNext == 0x1032 and abs(delta - deltaNext) <= 0xFF:
										#
										# Add 2x
										#
										intensity += delta
										current_results.append( intensity );
										intensity += deltaNext
										current_results.append( intensity );
									else:
										#
										# Add 1x
										#
										f.seek(f.tell() - 2)
										intensity += delta
										current_results.append( intensity );
					except struct.error:
						readFile = 0
				results.append(current_results)
f = open('out.csv', 'w')
for item in results:
	temp = ", ".join(map(str,item))

	print >> f, temp # or f.write('...\n')
