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

GAME_HOME = u''
SERVER_HOME = u''
WORLDS = []
SECTOR_SIZE = 32
SECTOR_WIDTH = SECTOR_SIZE
SECTOR_HEIGHT = SECTOR_SIZE
BUFSIZE = 4096
CONF = {'sec_w':SECTOR_WIDTH, 'sec_h':SECTOR_HEIGHT}

def Setup(game_home, server_home):
    global GAME_HOME
    global SERVER_HOME
    GAME_HOME = game_home
    SERVER_HOME = server_home

