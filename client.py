import socket 
import time 
import threading 

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(( 'localhost',5551 ))
sock.send(b'1')
print(sock.recv(1024).decode())
nickname = input( 'input your nickname :' )
sock.send(nickname.encode())

def sendwords():
    while 1:
        try:
            words = input()
            sock.send(words.encode())
        except ConnectionAbortedError:
            print('Sever closed this connection')
        except ConnectionResetError:
            print('Server is closed!')

def recvwords():
    while 1:
        try :
            words = sock.recv(1024)
            if words:
                print(words.decode())
            else:
                pass
        except ConnectionAbortedError:
            print('Sever closed this connection')
        except ConnectionResetError:
            print('Server is closed!')

t1 = threading.Thread(target = sendwords)
t2 = threading.Thread(target = recvwords)

threads = [t1,t2]
for t in threads:
    t.setDaemon(True)
    t.start()
t.join()
            