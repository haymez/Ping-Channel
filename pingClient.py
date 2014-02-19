from scapy.all import *
import time, binascii


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
	
	for i in range(len(binary)):
		if(binary[i:i+1] == "1"):
			pinger(dst_ip, src_ip, 0)
			time.sleep(.1)
		else:
			time.sleep(.1)
	#send end of mesage ping
	pinger(dst_ip, src_ip, 1)
	

#Convert string to binary representation
def strToBinary(string):
	binary = bin(int(binascii.hexlify(string), 16))[2:]
	while(len(binary) % 8 != 0):
		binary = "0" + binary
	return binary



encodeMessage("127.0.0.1", "192.168.1.190", "Hi")








