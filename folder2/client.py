import socket
ENDSTRING = 'oUtAnDoVeRHello'
s = socket.socket()
host = ""
port = input("Enter port for client: ");
s.connect((host, port))
# s.send("Hello server!")
def receiveFunc(com):
    s.send(com)
    data = s.recv(1024)
    s.send('received')
    retstr = ''
    while data != ENDSTRING:
        # print data+'\n'
        retstr += data
        data = s.recv(1024)
        s.send('received')
    # print retstr
    return retstr

def indexFunc( com ):
    com1 = com.split()
    text = receiveFunc(com)
    print text

def downloadFunc(com):
    s.send(com)
    com = com.split()
    if com[1] == 'TCP':
        f = open(com[2],'wb')
        data = s.recv(1024)
        s.send('received')
        while data!= ENDSTRING:
            f.write(data)
            data = s.recv(1024)
            s.send('received')
        f.close()
    elif com[1] == 'UDP':
        port2 = int(s.recv(1024))
        s.send('received')
        soc2 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        f = open(com[2],'wb')
        addr = (host,port2)
        # soc2.sendto('received',addr)
        data = soc2.recvfrom(1024)
        while data:
            f.write(data)
            data, addr = soc2.recvfrom(1024)
            soc2.sendto('received',addr)


FLAG = True
while FLAG==True:
    com = raw_input("prompt> ")
    com1 = com.split()
    if len(com1) >= 2 :
        if(com1[0]=='index'):
            indexFunc(com)
        elif(com1[0]=='hash'):
            indexFunc(com)
        elif(com1[0]=='download'):
            downloadFunc(com)
        elif(com1[0]=='exit'):
            FLAG=False
        else:
            print "Not a correct command\n"
    else:
        print "Not a correct command\n"

s.close()

print('connection closed')
# with open('received_file', 'wb') as f:
#     print 'file opened'
#     while True:
#         print('receiving data...')
#         data = s.recv(1024)
#         print('data=%s', (data))
#         if not data:
#             break
#         # write data to a file
#         f.write(data)
# f.close()
# print('Successfully get the file')
