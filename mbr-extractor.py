#!/usr/bin/python
import sys

#extract the 512 bytes from /dev/sda
def rawMbrDData():
	with open('/dev/sda', 'rb') as fp:
		hex_list = ["{:02x}".format(ord(c)) for c in fp.read(512)]

	print hex_list[0]
	print type(hex_list)
	fp.close();
	return hex_list

def main():
	rawData = rawMbrDData()
	print rawData


if __name__== "__main__":
	main()
