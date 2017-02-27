import threading, socket, time, sys, snek
from snek.snekmethods import treatData

HOST_ADDR = '192.168.25.32'
#HOST_ADDR = '192.168.0.4'

class GameClient(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.effective_server = None
        self.sock_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock_data = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock_data.setblocking(False)
        self.sock_data.bind( (HOST_ADDR, snek.CONF['data_port']) )
        self.sock_graphics = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock_graphics.setblocking(False)
        self.sock_graphics.bind( (HOST_ADDR, snek.CONF['graphics_port']) )
        self.handshake = '%d %d' % (snek.CONF['data_port'], snek.CONF['graphics_port'])
        self.rem_serv_info = (snek.CONF['remote_server_ip'], snek.CONF['remove_server_port'])
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
                handshake += u' %s %s %s' % (login, password, email)
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
                    try: (data,addr) = self.sock_data.recvfrom(snek.BUFSIZE)
                    except BlockingIOError: pass
                    else:
                        answer = data.decode('utf-8')
                        print('Server answer: %s' % answer)
                        content = answer.split()
                        if len(content) == 2:
                            serv_eff_addr = content[0]
                            serv_eff_port = treatData(content[1])
                            self.id_hash = content[2]
                        else: continue
                        snek.EFF_REM_SERV = ( treatData(serv_eff_addr), treatData(serv_eff_port ) )
                        self.online = True
                        break
                    print(' %d' % (10 - j), end=u'', flush=True)
                if self.online:
                    print('\n\tServer answered. We are online!')
                    print('\tConnected to ', end='')
                    print(snek.EFF_REM_SERV)
                    break
                else:
                    print('\n\tNo answer. Sending handshake again.\n\twaiting for the server...', end='', flush=True)
                    try: self.sock_out.sendto(handshake.encode('utf-8'), self.rem_serv_info )
                    except OSError:
                        print('\n\tOS Error. Check your internet connection.')
                        break
            
            # Game loop
            print('\n\nRunning...')
            while self.online:
                # Receive game data from Herald
                try: (game_data, herald) = self.sock_data.recvfrom(snek.BUFSIZE)
                except BlockingIOError: pass
                # Receive graphic data from Artificer
                try: (graphic_data, artificer) = self.sock_graphics.recvfrom(snek.BUFSIZE)
                except BlockingIOError: pass
                
                # Display raw data for debug
                try: print(game_data.decode('utf-8'))
                except: pass
                try: print(graphic_data.decode('utf-8'))
                except: pass
                
                # Prepare player input
                
                # Send player actions to the server
                # First line use:
                #    online - player is online and present
                #    afk - client detected the player is not giving input
                #    off - player purposely left the game
                # this may be usefull.
                msg = u'%s\n' % self.id_hash # For identification
                msg += u'KeyStrokeSequenceCompactedByTheClient\n' # For the director to process
                msg += u'800 600' # Screen resolution. For sectors loading and graphics packing. Max 1920 1080.
                self.sock_out.sendto(msg.encode('utf-8'), snek.EFF_REM_SERV)
                
                # Sleep a little
                time.sleep(2)


