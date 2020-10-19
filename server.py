import threading 
import socket

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #開啟 server 等待 client 進入
socket.bind( ( '',5550 ) )
socket.listen(5)

print('Server listening ...')

nickname_dir = {}
people = []
def tellothers( exceptNum, words ):  #發送 words 聊天室的其他人 
    for person in people:
        if person.fileno() != exceptNum:
            try:
                person.send(words.encode())
            except:
                pass

def room(person, person_id ):  #將連線的 socket 設定 nickname , 並處理聊天室的公共事務( 廣播, server 轉發 )
    nickname = person.recv(1024).decode()
    nickname_dir[person_id] = nickname
    people.append(person)
    print('connection',person_id,'has nickname : ',nickname)
    tellothers( person_id , '系統提示 '+nickname+' 進入聊天室')
    while 1:
        try:
            msg = person.recv(1024).decode()
            if msg:
                print(nickname, ":", msg)
                tellothers( person_id,nickname+ ":"+ msg )
        except ( OSError, ConnectionResetError ):
            try:
                people.remove(person)
            except:
                pass
            print(person_id,'exit, ',len(people), ' people left ' )
            tellothers( person_id, 'exit, '+str(len(people))+' people left ' )
            person.close()
            return 
while 1:
    client, addr = socket.accept()
    print('Accept a new connection', client.getsockname(), client.fileno())
    try:
        words = client.recv(1024).decode()
    
        if words == '1':
            client.send(b'welcome to server')
            t1 = threading.Thread( target = room, args = (client, client.fileno()) )
            t1.setDaemon(True)
            t1.start()
        else:
            client.send(b'go out')
            client.close()
    except:
        pass
    