from scapy.all import *
import time, binascii, argparse, sys

parser=argparse.ArgumentParser()
parser.add_argument('-d', help = 'destination IP address')
parser.add_argument('-s', help = 'source IP address')
parser.add_argument('-m', help = 'message to send (in quotes)')
parser.add_argument('-w', help = 'wait time for timing channel (in seconds)', type=float)
args=parser.parse_args()


def pinger(dst_ip, src_ip, last_bool):
	# define ip and icmp
	ip = IP()
	icmp = ICMP()
	
	#set destination and source IP
	ip.dst = dst_ip
	ip.src = src_ip
	if(last_bool == 1):
		ip.ttl = 100
	icmp.type = 8
	icmp.code = 0
	
	#Send packet
	send(ip/icmp)


#encode message into timing channel using pings
def encodeMessage(dst_ip, src_ip, message):
	#convert message to binary
	binary = strToBinary(message)
	#initial ping to start timeout of sniffer
	pinger(dst_ip, src_ip, 0)
	sniff(filter="icmp and (src " + dst_ip + ")",count=1)
	for i in range(len(binary)):
		if(binary[i:i+1] == "1"):
			pinger(dst_ip, src_ip, 0)
			time.sleep(args.w)
		else:
			time.sleep(args.w)
	#send end of mesage ping
	pinger(dst_ip, src_ip, 1)
	

#Convert string to binary representation
def strToBinary(string):
	binary = bin(int(binascii.hexlify(string), 16))[2:]
	while(len(binary) % 8 != 0):
		binary = "0" + binary
	return binary

if(len(sys.argv) < 9):
	print "Incorrect number of inputs."
	print "Try running 'sudo python pingClient.py -h' for more information."
else:
	encodeMessage(args.d, args.s, args.m)








