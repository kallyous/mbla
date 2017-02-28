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
        self.sock_handshake = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_handshake.settimeout(15)
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
            #email = input(u'\tEmail: ')
            email = u'email@mail.com'
            #login = input(u'\tUsername: ')
            login = u'Lucas'
            #password = input(u'\tPassword: ')
            password = u'12345'
            if login != '' and password != '' and email != '':
                handshake += u' %s %s %s' % (login, password, email)
                print('\tSending ', end='', flush=False)
                print(handshake, end='', flush=False)
                print(' to ', end='', flush=False)
                print(self.rem_serv_info)
                for i in range(10):
                    print('\tConnection attempt #%d' % (i+1) )
                    if i == 9: print('\tLast attempt.')
                    # Try to connect
                    try: self.sock_handshake.connect( self.rem_serv_info )
                    except socket.timeout:
                        print('\tConnection timed out.')
                        continue
                    # Try to send handshake and receive the answer
                    try:
                        self.sock_handshake.sendall(handshake.encode('utf-8'))
                        serv_answer = self.sock_handshake.recv(snek.BUFSIZE).decode('utf-8')
                    except socket.timeout:
                        print('\tData exchange timed out.')
                        continue
                    # Quick answer checkup then store it
                    print(u'\tReceived form server: %s' % serv_answer)
                    content = serv_answer.split()
                    if not len(content) == 2:
                        print(u'\tServer answer must have [addr port]')
                        self.sock_handshake.close()
                        continue
                    snek.EFF_REM_SERV = ( treatData(content[0]), treatData(content[1]) )
                    # If we reach here, we should be OK to start exchanging data.
                    self.online = True
                    print('We are online!')
                    # Close connection and proceeds to game loop
                    self.sock_handshake.close()
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
                #msg = u'%s\n' % self.id_hash # For identification
                msg = u'KeyStrokeSequenceCompactedByTheClient\n' # For the director to process
                msg += u'800 600' # Screen resolution. For sectors loading and graphics packing. Max 1920 1080.
                self.sock_out.sendto(msg.encode('utf-8'), snek.EFF_REM_SERV)
                
                # Sleep a little
                time.sleep(2)


