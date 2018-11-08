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
	print ("Parsing info")



def checkSignature(rawData):
	print ("Checking Signature.....")
	if (rawData[511] == "aa" and rawData[510] == "55" and rawData[444] == "00" and rawData[445] == "00"):
		print("MBR found on Sector 0")
		print (rawData[444]+rawData[445])
	else:
		print("MBR signature doesn't match (MBR may not present)")


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
