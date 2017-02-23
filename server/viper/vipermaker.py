""" Copyright {yyyy} {name of copyright owner}

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License. """

import threading, builtins, codecs, json, socket, time
from viper.viperconf import *
from viper.viperworld import *

builtins.WORLDS = []
META = []

class Maker(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.LoadServerConf()
	
	def run(self):
		for i in range( len(META) ):
			builtins.WORLDS.append({})
			for n in META[i]: builtins.WORLDS[i][n] = META[i][n]
			builtins.WORLDS[i]['master'] = self.RaiseMaster(i)
			builtins.WORLDS[i]['master'].start()
			time.sleep(1)
	
	def RaiseMaster(self, id):
		return Master(id)
	
	def LoadServerConf(self):
		global META
		with codecs.open('server.json', 'r', 'utf-8') as conf_file:
			conf_dict = json.load(conf_file)
			self.name = builtins.CONF['name'] = conf_dict['server_name']
			META = bubbleSort(conf_dict['worlds'], 'id')
			builtins.CONF['worlds_path'] = conf_dict['worlds_path']
			
			
			
		





























