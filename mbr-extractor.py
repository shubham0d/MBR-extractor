#!/usr/bin/python
from __future__ import print_function
import sys
import partitionID

def helpText():
	print ("Usage: $sudo python mbr-extractor.py <cmd> <device>")
	print ("Parameters:")
	print ("	cmd:")
	print ("		rawdump - dump hex data of MBR sector")
	print ("		parseinfo - extract the MBR and interprete it.")
	print ("		check - check whether the first sector is a valid MBR or not.")
	print ("	diskpath:")
	print ("		optional disk name from where MBR data need to extract(default set to your harddisk)")
#extract the 512 bytes from /dev/sda
def rawMbrData():
	possible_drives = [
        r"\\.\PhysicalDrive1", # Windows
        r"\\.\PhysicalDrive2",
        r"\\.\PhysicalDrive3",
        "/dev/mmcblk0", # Linux - MMC
        "/dev/mmcblk1",
        "/dev/mmcblk2",
        "/dev/sda", # Linux - Disk
        "/dev/sdb",
        "/dev/sdc",
        "/dev/disk1", #MacOSX
        "/dev/disk2",
        "/dev/disk3",
	]
	for drive in possible_drives:
		try:
			with open(drive, 'rb') as fp:
				hex_list = ["{:02x}".format(ord(c)) for c in fp.read(512)]
			fp.close();
			return hex_list
		except:
			pass

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
	print ("Disk Signature:" +rawData[443] + rawData[442] + rawData[441] +rawData[440])

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

	# Parsing Partition info for 1st partition
	if ((rawData[446] == "00" or rawData[446] == "80") and (rawData[447] != "00" or rawData[448] != "00" or rawData[449] !="00") and rawData[450] != "00"):
		print ("---------------------------1st Partition found---------------------------")
		partitionTypes = partitionID.partitionIdList(rawData[450])
		print ("Possible partition type: "+ partitionTypes)
		# size and sector calculator
		# 454 to 457 are starting lsb, 458 to 461 are sectors number
		lsbStringInHex = rawData[457]+rawData[456]+rawData[455]+rawData[454]
		startingSector = int(lsbStringInHex, 16)
		print("Starting sector: "+str(startingSector)+" ("+str(int(startingSector)*512)+" bytes)")
		noOfSectorsinHex = rawData[461]+rawData[460]+rawData[459]+rawData[458]
		noOfSectors = int(noOfSectorsinHex, 16)
		print ("Last sector: "+str(startingSector+noOfSectors-1)+" ("+str((startingSector+noOfSectors)*512)+" bytes)")
		totalSizeInByte = ((startingSector+noOfSectors)*512)-(startingSector*512)
		print ("Total size: "+str(totalSizeInByte/10**6)+"MB")
	else:
		print("-----------------------No Partition found on disk-----------------------")
	#Parsing Partition info for 2nd partition
	if ((rawData[462] == "00" or rawData[462] == "80") and (rawData[463] != "00" or rawData[464] !="00" or rawData[465] != "00") and rawData[466] != "00"):
		print ("---------------------------2nd Partition found---------------------------")
		partitionTypes = partitionID.partitionIdList(rawData[466])
		print ("Possible partition type: "+ partitionTypes)
		# 470 to 473 are starting lsb,474 to 477 are sector number
		lsbStringInHex = rawData[473]+rawData[472]+rawData[471]+rawData[470]
		startingSector = int(lsbStringInHex, 16)
		print("Starting sector: "+str(startingSector)+" ("+str(int(startingSector)*512)+" bytes)")
		noOfSectorsinHex = rawData[477]+rawData[476]+rawData[475]+rawData[474]
		noOfSectors = int(noOfSectorsinHex, 16)
		print ("Last sector: "+str(startingSector+noOfSectors-1)+" ("+str((startingSector+noOfSectors)*512)+" bytes)")
		totalSizeInByte = ((startingSector+noOfSectors)*512)-(startingSector*512)
		print ("Total size: "+str(totalSizeInByte/10**6)+"MB")
	else:
		print("-----------------------End partition list-----------------------")
		return
	#Parsing Partition info for 3rd partition
	if ((rawData[478] == "00" or rawData[478] == "80") and (rawData[479] != "00" or rawData[480] !="00" or rawData[481] != "00") and rawData[482] != "00"):
		print ("---------------------------3rd Partition found---------------------------")
		partitionTypes = partitionID.partitionIdList(rawData[482])
		print ("Possible partition type: "+ partitionTypes)
		# 486 to 489 are starting lsb, 490 to 493 are sector number
		lsbStringInHex = rawData[489]+rawData[488]+rawData[487]+rawData[486]
		startingSector = int(lsbStringInHex, 16)
		print("Starting sector: "+str(startingSector)+" ("+str(int(startingSector)*512)+" bytes)")
		noOfSectorsinHex = rawData[493]+rawData[492]+rawData[491]+rawData[490]
		noOfSectors = int(noOfSectorsinHex, 16)
		print ("Last sector: "+str(startingSector+noOfSectors-1)+" ("+str((startingSector+noOfSectors)*512)+" bytes)")
		totalSizeInByte = ((startingSector+noOfSectors)*512)-(startingSector*512)
		print ("Total size: "+str(totalSizeInByte/10**6)+"MB")
	else:
		print("-----------------------End partition list-----------------------")
		return
	#Parsing Partition info for 4th partition
	if ((rawData[494] == "00" or rawData[494] == "80") and (rawData[495] != "00" or rawData[496] !="00" or rawData[497] != "00") and rawData[498] != "00"):
		print ("---------------------------4th Partition found---------------------------")
		partitionTypes = partitionID.partitionIdList(rawData[498])
		print ("Possible partition type: "+ partitionTypes)
		# 502 to 505 are starting lsb, 506 to 509 are sector number
		lsbStringInHex = rawData[505]+rawData[504]+rawData[503]+rawData[502]
		startingSector = int(lsbStringInHex, 16)
		print("Starting sector: "+str(startingSector)+" ("+str(int(startingSector)*512)+" bytes)")
		noOfSectorsinHex = rawData[509]+rawData[508]+rawData[507]+rawData[506]
		noOfSectors = int(noOfSectorsinHex, 16)
		print ("Last sector: "+str(startingSector+noOfSectors-1)+" ("+str((startingSector+noOfSectors)*512)+" bytes)")
		totalSizeInByte = ((startingSector+noOfSectors)*512)-(startingSector*512)
		print ("Total size: "+str(totalSizeInByte/10**6)+"MB")
	else:
		print("-----------------------End partition list-----------------------")
		return

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
		helpText()
		return
	else:
		if sys.argv[1] == "rawdump":
			dumpRawData(rawData)
		elif sys.argv[1] == "parseinfo":
			parseInfo(rawData)
		elif sys.argv[1] == "check":
			checkSignature(rawData)
		else:
			print ("Try again")


if __name__== "__main__":
	main()
