import threading, socket, time, sys
from snek.__init__ import CONF, GAME_HOME, SERVER_HOME, BUFSIZE

HOST_ADDR = '192.168.25.32'

class GameClient(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.sock_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock_data = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock_data.setblocking(False)
        self.sock_data.bind( (HOST_ADDR, CONF['data_port']) )
        self.sock_graphics = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock_graphics.setblocking(False)
        self.sock_graphics.bind( (HOST_ADDR, CONF['graphics_port']) )
        self.greeting = '%d %d' % (CONF['data_port'], CONF['graphics_port'])
        self.rem_serv_info = (CONF['remote_server_ip'], CONF['remove_server_port'])
    
    def run(self):
        server_comm = 0
        greetings = self.greeting
        print(u'\n ***** Mythical Byte Lands (pre)Alpha *****\n')
        # Interface loop
        while True:
            print(u'\tReady to connect. Local game not implemented.')
            login = input(u'\tUsername: ')
            password = input(u'\tPassword: ')
            if login != '' and password != '':
                greetings += ' %s %s' % (login, password)
                print('\tSending ', end='', flush=False)
                print(greetings, end='', flush=False)
                print(' to ', end='', flush=False)
                print(self.rem_serv_info)
                try: self.sock_out.sendto(greetings.encode('utf-8'), self.rem_serv_info )
                except OSError:
                    print('OS Error. Check your internet connection.')
                    sys.exit(1)
            print('\n\twaiting for the server...', end='', flush=True)
            for i in range(10):
                die = True
                time.sleep(1)
                try: (data,addr) = self.sock_data.recvfrom(BUFSIZE)
                except BlockingIOError: pass
                else:
                    server_comm = data.decode('utf-8')
                    die = False
                    break
                print(' %d' % (10 - i), end=u'', flush=True)
            
            # Game loop
            print('\n\nRunning...')
            while True:
                try: (game_data, herald) = self.sock_data.recvfrom(BUFSIZE)
                except BlockingIOError: pass
                try: (graphic_data, artificer) = self.sock_graphics.recvfrom(BUFSIZE)
                except BlockingIOError: pass
                try: print(game_data.decode('utf-8'))
                except: pass
                try: print(graphic_data.decode('utf-8'))
                except: pass
                self.sock_out.sendto(greetings.encode('utf-8'), self.rem_serv_info)
                time.sleep(1)
    
    def configure(self, name, value):
        global CONF
        global GAME_HOME
        global SERVER_HOME
        if name == 'game_home':
            GAME_HOME = value
            return
        if name == 'server_home':
            SERVER_HOME = value
        CONF[name] = value
        return

