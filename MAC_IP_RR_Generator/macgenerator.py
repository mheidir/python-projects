#!/home/mheidir/.pyenv/shims/python

from progressbar import ProgressBar
import sys

genType = ""
maxCount = 0

def printError():
	print("Proper usage: python ./macgenerator.py [ip/mac] [integer]")
	print("python ./macgenerator.py mac 100")


def toStr(n,base):
	convertString = "abcdefghijklmnopqrstuvwxyz"
	#print (n)
	if n < base:
		return convertString[n]
	else:
		return toStr(n//base,base) + convertString[n%base]
	  

def base10toN(num, base):
	"""Change ``num'' to given base
	Upto base 36 is supported."""

	converted_string, modstring = "", ""
	currentnum = num
	if not 2 < base < 37:
		raise ValueError("base must be between 2 and 36")
	#if not num:
		#return '0'
		
	while currentnum:
		mod = (currentnum % base)
		currentnum = currentnum // base
		
		#print (chr(96 + mod + 1*(mod > 9)))
		print (7*(mod > 26))
		converted_string = chr(97 + mod + 7*(mod > 26)) + converted_string
		#converted_string = chr(97 + mod) + converted_string
	return converted_string


def genMacAddress(count):
	f = open("macaddress.txt", "w")
	i = 1
	while i < count + 1:
		macAddr = str(hex(i).lstrip("0x").rstrip("L"))
		
		if len(macAddr) == 1:
			macAddr = "00000000000" + macAddr
		if len(macAddr) == 2:
			macAddr = "0000000000" + macAddr
		if len(macAddr) == 3:
			macAddr = "000000000" + macAddr
		if len(macAddr) == 4:
			macAddr = "00000000" + macAddr
		if len(macAddr) == 5:
			macAddr = "0000000" + macAddr
		if len(macAddr) == 6:
			macAddr = "000000" + macAddr
		if len(macAddr) == 7:
			macAddr = "00000" + macAddr
		if len(macAddr) == 8:
			macAddr = "0000" + macAddr
		if len(macAddr) == 9:
			macAddr = "000" + macAddr
		if len(macAddr) == 10:
			macAddr = "00" + macAddr
		if len(macAddr) == 11:
			macAddr = "0" + macAddr

		macAddr = ':'.join(macAddr[i:i+2] for i in range (0, len(macAddr), 2))
		f.write(macAddr + "\n")

		pb.print_progress_bar(i)
		i += 1
		
	f.close()
	return
		
def genIpAddress(count):
	ipAddr = [2, 0, 0 ,0]
	
	f = open("ipaddress.txt", "w")

	i = 1
	n = 0
	while i < count + 1:
		ipAddr[3] += 1
		
		f.write(str(ipAddr[0]) + "." + str(ipAddr[1]) + "." + str(ipAddr[2]) + "." + str(ipAddr[3]) + "\n")
		
		if ipAddr[3] == 255:
			ipAddr[2] += 1
			ipAddr[3] = -1
		if ipAddr[2] == 256:
			ipAddr[1] += 1
			ipAddr[2] = 0
			ipAddr[3] = -1
		if ipAddr[1] == 256:
			ipAddr[0] += 1
			ipAddr[1] = 0
			ipAddr[2] = 0
			ipAddr[3] = -1
		
		pb.print_progress_bar(i)
		i += 1
	
	f.close()
	return

def genARecord(count):
	domainName = ".acme.corp"
	
	f = open("arecord.txt", "w")
	i = 0
	base = 26
	convertString = "abcdefghijklmnopqrstuvwxyz"
		
	while i < count + 1:
		if i < base:
			f.write(convertString[i] + domainName + "\n")
		else:
			f.write(toStr(i//base,base) + convertString[i%base] + domainName + "\n")
	
		if i == count:
			break;
		
		pb.print_progress_bar(i)
		i += 1
		
	f.close()
	return


if len(sys.argv) == 3:
	genType = sys.argv[1]
	maxCount = int(sys.argv[2])
	
	pb = ProgressBar(total=maxCount,prefix='Here', suffix='Now', decimals=3, length=50, fill='X', zfill='-')
	
	if genType == "ip":
		genIpAddress(maxCount)
	if genType == "mac":
		genMacAddress(maxCount)
	if genType == "a":
		genARecord(maxCount)
	
else:
	printError()


# References:
# https://pypi.org/project/console-progressbar/
