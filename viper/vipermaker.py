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

import threading, codecs, json, time, socket, viper
from viper.viperlords import Master
from viper.vipermethods import bubbleSort, treatData, AuthUser


class Maker(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self, name='Lands Maker')
		self.loadServerConf()
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.settimeout(15)
		self.sock.bind( (viper.SERVER_ADDR, viper.CONF['service-port']) )
		self.sock.listen(50)
	
	def run(self):
		# Launch worlds
		self.startWorlds()
		while True:
			try: (conn, addr) = self.sock.accept()
			except socket.timeout: pass
			else:
				data_str = conn.recv(viper.BUFSIZE)
				print('New connection: %s from %s %d' % (data_str, addr[0], addr[1]) )
				(loggedIn, serv_service_port, cli_data_port, msg) = self.loginPlayer( data_str, addr[0] )
				# Debug
				print('Logged in: ', end='')
				print(loggedIn)
				print('World service port: ', end='')
				print(serv_service_port)
				print('Client data port: ', end='')
				print(cli_data_port)
				print('Result message: ', end='')
				print(msg)
				# -----
				if loggedIn:
					answer = u'%s %d' % (viper.SERVER_ADDR, serv_service_port)
					print(u'Sending back %s' % answer)
				else:
					answer = msg
				try: conn.sendall(answer.encode('utf-8'), viper.BUFSIZE)
				except socket.timeout: print('Tiemd out when sending answer')
				else: print('Answer successfully sent')
				finally: conn.close()
			time.sleep(1)
	
	def loginPlayer(self, data_str, addr):
		data = data_str.split()
		for i in range(len(data)):
			data[i] = treatData(data[i])
		player_data = { 'addr': addr,
						'data-port': data[0],
						'graphics-port': data[1] }
		# Gets/adds player from/to DB and returns a boolean, message then the data.
		(auth_res, msg, db_data) = AuthUser(data[2], data[3], data[4])
		if auth_res:
			for n in db_data: player_data[n] = db_data[n]
			world = player_data['world']
			# TODO: Use a script at assets/scripts for building the player based on DB data.
			viper.WORLDS[world]['master'].addPlayer(player_data)
			return True, viper.WORLDS[world]['listen-port'], player_data['data-port'], msg
		else:
			return False, 0, 0, msg
	
	def startWorlds(self):
		for i in range( len(viper.WORLDS) ):
			viper.WORLDS[i]['master'] = self.raiseMaster(i)
			viper.WORLDS[i]['players'] = {}
			viper.WORLDS[i]['master'].start()
			time.sleep(1)
	
	def raiseMaster(self, wid):
		return Master(wid)
	
	def loadServerConf(self):
		with codecs.open('server.conf', 'r', 'utf-8') as conf_file:
			conf_dict = json.load(conf_file)
			for n in conf_dict:
				if n != 'worlds':
					viper.CONF[n] = treatData(conf_dict[n])
			worlds_meta = bubbleSort(conf_dict['worlds'], 'id')
			for w in worlds_meta: 
				viper.WORLDS.append(w)

			
			
			
		





























