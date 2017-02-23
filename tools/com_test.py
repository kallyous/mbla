# -*- coding: utf-8 -*-

import socket

PORT = 8788
HOST = '127.0.1.2'
msg = 'Testing connection'.encode('utf-8')

udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpsock.bind( (HOST, PORT) )
udpsock.sendto(msg, ('127.0.1.1', 3793) )

while True:
	try: (data, addr) = udpsock.recvfrom(4096)
	except socket.timeout: pass
	else:
		print('Received:\n%s' % data.decode('utf-8'))

