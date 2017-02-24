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

import threading, codecs, json, time
from viper.__init__ import WORLDS, CONF
from viper.viperlords import Master
from viper.vipermethods import bubbleSort


META = []

class Maker(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.LoadServerConf()
	
	def run(self):
		for i in range( len(META) ):
			WORLDS.append({})
			for n in META[i]: WORLDS[i][n] = META[i][n]
			WORLDS[i]['master'] = self.RaiseMaster(i)
			WORLDS[i]['master'].start()
			time.sleep(1)
	
	def RaiseMaster(self, wid):
		return Master(wid)
	
	def LoadServerConf(self):
		global META
		with codecs.open('server.json', 'r', 'utf-8') as conf_file:
			conf_dict = json.load(conf_file)
			self.name = CONF['name'] = conf_dict['server_name']
			META = bubbleSort(conf_dict['worlds'], 'id')
			CONF['worlds_path'] = conf_dict['worlds_path']
			
			
			
		





























