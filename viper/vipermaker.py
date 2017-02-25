""" Copyright 2017 Kallyous Caos Negro
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License. """

import threading, codecs, json, time, socket
from viper.__init__ import WORLDS, CONF, BUFSIZE
from viper.viperlords import Master
from viper.vipermethods import bubbleSort, treatData

SERVER_ADDR = '46.101.28.141'

class Maker(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self, name='Lands Maker')
		self.LoadServerConf()
		self.service_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.service_sock.setblocking(False)
		self.service_sock.bind( (SERVER_ADDR, CONF['service-port']) )
		self.temp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.temp_sock.setblocking(False)
		print(CONF)
		print(socket.gethostname())
	
	def run(self):
		# Launch worlds
		self.StartWorlds()
		while True:
			try: (data, addr) = self.service_sock.recvfrom(BUFSIZE)
			except BlockingIOError: pass
			else:
				print(data.decode('utf-8'))
				print(addr)
				client_info = data.decode('utf-8').split()
				for i in range(len(client_info)):
					client_info[i] = treatData(client_info[i])
				self.temp_sock.sendto('I see you.'.encode('utf-8'), (addr[0], client_info[0]) )
			time.sleep(1)
		
	
	def StartWorlds(self):
		for i in range( len(WORLDS) ):
			WORLDS[i]['master'] = self.RaiseMaster(i)
			WORLDS[i]['master'].start()
			time.sleep(1)
	
	def RaiseMaster(self, wid):
		return Master(wid)
	
	def LoadServerConf(self):
		with codecs.open('server.conf', 'r', 'utf-8') as conf_file:
			conf_dict = json.load(conf_file)
			for n in conf_dict:
				if n != 'worlds':
					CONF[n] = treatData(conf_dict[n])
			worlds_meta = bubbleSort(conf_dict['worlds'], 'id')
			for w in worlds_meta: 
				WORLDS.append(w)

			
			
			
		





























