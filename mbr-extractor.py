#!/usr/bin/python
from __future__ import print_function
import sys



#extract the 512 bytes from /dev/sda
def rawMbrData():
	with open('/dev/sda', 'rb') as fp:
		hex_list = ["{:02x}".format(ord(c)) for c in fp.read(512)]
	fp.close();
	return hex_list

def dumpRawData(rawData):
	print ("Dumping raw MBR data.....\n")
	print ("00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F")
	print ("-----------------------------------------------")
	#sys.stdout.write(rawData[0]+ " ")
	for i in range(0,512):
		if i%16 == 0 and i != 0:
			print(rawData[i], end=' ')
			print ("\n")
		else:
			print(rawData[i], end=' ')
	print ("\n")



def parseInfo(rawData):
	if (checkSignature(rawData) != True):
		exit

	print ("Parsing info....")
	print ("------------------------")
	print ("Disk Signature:" +rawData[440] + rawData[441] + rawData[442] +rawData[443])

	print("Possible MBR scheme", end=':')
	if (rawData[218] == "00" and rawData[219] == "00"):
		print(" Modern standard MBR found.")
	elif (rawData[428] == "78" and rawData[429] == "56"):
		print (" Advanced Active Partitions (AAP) MBR found")
	elif (rawData[0] == "eb" and rawData[2] == "4e" and rawData[3] == "45" and rawData[4] == "57" and rawData[6] == "4c" and raw_input[7] == "44" and rawData[8] == "52"):
		print (" NEWLDR MBR found.")
	elif (rawData[380] == "5a" and rawData[381] == "a5"):
		print (" MS-DOS MBR found.")
	elif (rawData[252] == "aa" and rawData[253] == "55"):
		print (" Disk Manager MBR")
	else:
		print (" Generic MBR found")



def checkSignature(rawData):
	print ("Checking Signature.....")
	if (rawData[511] == "aa" and rawData[510] == "55" and rawData[444] == "00" and rawData[445] == "00" or rawData[444] == "5a" or rawData[445] == "5a"):
		print("MBR found on Sector 0")
		return True
	else:
		print("MBR signatures doesn't match (MBR may not present)")
		return False

def main():
	rawData = rawMbrData()
	#print rawData
	if len(sys.argv) == 1:
		#print help message
		print ("Less argument")
	else:
		if sys.argv[1] == "rawdump":
			dumpRawData(rawData)
		elif sys.argv[1] == "info":
			parseInfo(rawData)
		elif sys.argv[1] == "check":
			checkSignature(rawData)
		else:
			print ("Try again")


if __name__== "__main__":
	main()
