from scapy.all import *
import time, binascii, argparse, sys

parser=argparse.ArgumentParser()
parser.add_argument('-s', help = 'source IP address to listen for')
args=parser.parse_args()

y = 0
binary = ""
currTime = 0

#get current time in milliseconds
curr_time_milli = lambda: int(round(time.time() * 1000))

#Converts binary back to string
def binToString(binary):
	hexVal = hex(int(binary, 2))[2:]
	if(len(hexVal) % 2 != 0):
		hexVal = hexVal[:len(hexVal)-1]
	return hexVal.decode('hex')

#initializes global variables back to defaults
def init():
	global binary
	binary = ""
	global y
	y = 0
	global currTime
	currTime = 0


#Listens for end packet
def stopListening(x):
	if(x[IP].ttl == 100):
		return True
	else:
		return False


#Listens for pings
def listener(x):
	global y
	global binary
	global currTime
	
	if(y == 0):
		y = y + 1
		
		#this is the first ping we have recieved
		if(currTime == 0):
			currTime = curr_time_milli() - 100
		#This is every ping after the first one
		else:
			zeroes = int(((curr_time_milli() - currTime)/100)) - 1
			currTime = curr_time_milli()
			
			#Add in zeroes
			for i in range(zeroes):
				binary = binary + "0"
			binary = binary + "1"
		
	else:
		y = 0

if(len(sys.argv) < 2):
	print "Incorrect number of inputs."
	print "Try running 'sudo python pingServer.py -h' for more information."
else:
	while(1):
		#this sniffs for the first packet. after this packet, we start listening for message
		sniff(iface="lo", filter="icmp and (src " + str(args.s) + ")", prn=listener, count=1)
		
		#sniff for message and timeout after 8 seconds
		sniff(iface="lo", filter="icmp and (src " + str(args.s) + ")", prn=listener, stop_filter=stopListening)
		while(len(binary) % 8 != 0):
			binary = binary + "0"
		
		print binToString(binary)
		init()



