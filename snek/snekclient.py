import threading, socket, time, sys
from snek.__init__ import CONF, GAME_HOME, LOC_SERV_HOME, BUFSIZE, EFF_REM_SERV
from snek.snekmethods import treatData

HOST_ADDR = '192.168.25.32'

class GameClient(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.effective_server = None
        self.sock_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock_data = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock_data.setblocking(False)
        self.sock_data.bind( (HOST_ADDR, CONF['data_port']) )
        self.sock_graphics = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock_graphics.setblocking(False)
        self.sock_graphics.bind( (HOST_ADDR, CONF['graphics_port']) )
        self.handshake = '%d %d' % (CONF['data_port'], CONF['graphics_port'])
        self.rem_serv_info = (CONF['remote_server_ip'], CONF['remove_server_port'])
        self.online = False
    
    def run(self):
        server_comm = 0
        handshake = self.handshake
        print(u'\n ***** Mythical Byte Lands (pre)Alpha *****\n')
        # Interface loop
        while True:
            print(u'\tReady to connect. Local game not implemented.')
            email = input(u'\tEmail: ')
            login = input(u'\tUsername: ')
            password = input(u'\tPassword: ')
            if login != '' and password != '' and email != '':
                handshake += u' %s %s %s' % (email, login, password)
                print('\tSending ', end='', flush=False)
                print(handshake, end='', flush=False)
                print(' to ', end='', flush=False)
                print(self.rem_serv_info)
                try: self.sock_out.sendto(handshake.encode('utf-8'), self.rem_serv_info )
                except OSError:
                    print('OS Error. Check your internet connection.')
                    sys.exit(1)
            print('\n\twaiting for the server...', end='', flush=True)
            for i in range(10):
                for j in range(10):
                    time.sleep(1)
                    try: (data,addr) = self.sock_data.recvfrom(BUFSIZE)
                    except BlockingIOError: pass
                    else:
                        (serv_eff_addr, serv_eff_port) = data.decode('utf-8').split()
                        EFF_REM_SERV = ( treatData(serv_eff_addr), treatData(serv_eff_port ) )
                        self.online = True
                        break
                    print(' %d' % (10 - j), end=u'', flush=True)
                if self.online:
                    print('\n\tServer answered. We are online!')
                    print('\tConnected to ', end='')
                    print(EFF_REM_SERV)
                    break
                else:
                    print('\n\tNo answer. Sending handshake again...', end='', flush=True)
                    try: self.sock_out.sendto(handshake.encode('utf-8'), self.rem_serv_info )
                    except OSError:
                        print('OS Error. Check your internet connection.')
                        sys.exit(1)
                    
            
            # Game loop
            print('\n\nRunning...')
            while self.online:
                # Receive game data from Herald
                try: (game_data, herald) = self.sock_data.recvfrom(BUFSIZE)
                except BlockingIOError: pass
                # Receive graphic data from Artificer
                try: (graphic_data, artificer) = self.sock_graphics.recvfrom(BUFSIZE)
                except BlockingIOError: pass
                
                # Display raw data for debug
                try: print(game_data.decode('utf-8'))
                except: pass
                try: print(graphic_data.decode('utf-8'))
                except: pass
                
                # Pool player input
                
                # Send player actions to the server
                # First line use:
                #    online - player is online and present
                #    afk - client detected the player is not giving input
                #    off - player purposely left the game
                # this may be usefull.
                self.sock_out.sendto('online\n'.encode('utf-8'), self.rem_serv_info)
                
                # Sleep a little
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

