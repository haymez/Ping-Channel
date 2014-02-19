Ping-Channel
============

Covert channel project for CYEN 402

##Description
This is a simple program that creates a cover thannel between client and server. 

##Usage
pingClient.py:

usage: pingClient.py [-h] [-d D] [-s S] [-m M]

arguments:
  -h, --help  show this help message and exit
  -d D        destination IP address
  -s S        source IP address
  -m M        message to send (in quotes)
  -w W	      Wait time between packets


pingServer.py:

usage: pingServer.py [-h] [-s S]

arguments:
  -h, --help  show this help message and exit
  -s S        source IP address to listen for
  -w W        Wait time between packets
