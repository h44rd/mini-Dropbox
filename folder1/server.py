import socket
import os
import re
import hashlib

ENDSTRING = 'oUtAnDoVeRHello'
port = input("Enter port: ")
s = socket.socket()
host = ""

s.bind((host, port))
s.listen(5)

def longlistFunc(conn):
    fl =  os.listdir('.')
    print fl
    for f in fl:
        stas = os.stat(f)
        conn.send("\n\nName: "+f)
        if conn.recv(1024) != 'received':
            break
        conn.send("\nSize: "+str(stas.st_size))
        if conn.recv(1024) != 'received':
            break
        conn.send("\nLast modification: "+str(stas.st_mtime))
        if conn.recv(1024) != 'received':
            break
        type  = "";
        if os.path.isdir(f):
            type = "Directory"
        else:
            type = "Regular file"
        conn.send("\nFile type: "+type)
        if conn.recv(1024) != 'received':
            break
    conn.send(ENDSTRING)
    conn.recv(1024)

def shortlistFunc(conn,com):
    fl =  os.listdir('.')
    print fl
    for f in fl:
        stas = os.stat(f)
        if int(com[2]) <= stas.st_mtime and stas.st_mtime <= int(com[3]):
            conn.send("\n\nName: "+f)
            if conn.recv(1024) != 'received':
                break
            conn.send("\nSize: "+str(stas.st_size))
            if conn.recv(1024) != 'received':
                break
            conn.send("\nLast modification: "+str(stas.st_mtime))
            if conn.recv(1024) != 'received':
                break
            type  = "";
            if os.path.isdir(f):
                type = "Directory"
            else:
                type = "Regular file"
            conn.send("\nFile type: "+type)
            if conn.recv(1024) != 'received':
                break
    conn.send(ENDSTRING)
    conn.recv(1024)
# filename = raw_input("Enter file to share:")
# print 'Server listening....'
def regexFunc(conn,com):
    # pat = re.compile(com[2])
    print com[2]
    fl =  os.listdir('.')
    print fl
    for f in fl:
        stas = os.stat(f)
        try:
            if re.search(com[2], f):
                conn.send("\n\nName: "+f)
                if conn.recv(1024) != 'received':
                    break
                conn.send("\nSize: "+str(stas.st_size))
                if conn.recv(1024) != 'received':
                    break
                conn.send("\nLast modification: "+str(stas.st_mtime))
                if conn.recv(1024) != 'received':
                    break
                type  = "";
                if os.path.isdir(f):
                    type = "Directory"
                else:
                    type = "Regular file"
                conn.send("\nFile type: "+type)
                if conn.recv(1024) != 'received':
                    break
        except:
            print "Error in regex"
    conn.send(ENDSTRING)
    conn.recv(1024)

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def verifyFunc(conn,com):
    if os.path.isfile(com[2]):
        hash=md5(com[2])
        conn.send(hash)
        if conn.recv(1024) != 'received':
            print "Problem in connection\n"
        tmsp = str(os.stat(com[2]).st_mtime)
        conn.send("\nTime stamp: "+tmsp)
        if conn.recv(1024) != 'received':
            print "Problem in connection\n"
        conn.send(ENDSTRING)
        conn.recv(1024)
    else:
        conn.send("\nNot a regular file\n")
        if conn.recv(1024) != 'received':
            print "Problem in connection\n"
        conn.send(ENDSTRING)
        conn.recv(1024)

def checkallFunc(conn):
    fl =  os.listdir('.')
    print fl
    for f in fl:
        stas = os.stat(f)
        conn.send("\n\nName: "+f)
        if conn.recv(1024) != 'received':
            break
        conn.send("\nChecksum: "+md5(f))
        if conn.recv(1024) != 'received':
            break
        conn.send("\nLast modification: "+str(stas.st_mtime))
        if conn.recv(1024) != 'received':
            break
    conn.send(ENDSTRING)
    conn.recv(1024)

def downloadTCPFunc(conn,com):
    f = open(com[2],'rb')
    text = f.read(1024)
    while text:
        conn.send(text)
        if conn.recv(1024) != 'received':
            break
        text = f.read(1024)
    conn.send(ENDSTRING)
    conn.recv(1024)

def downloadUDPFunc(conn,com):
    f = open(com[2],'rb')
    soc2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    port2 = create_port(soc2)
    conn.send(str(port2))
    if conn.recv(1024) != 'received':
        print "Problem in connection\n"
    text = f.read(1024)
    addr = (host,port2)
    while text:
        soc2.sendto(text,addr)
        ack,addr = soc2.recvfrom(1024)
        if ack != 'received':
            print 'Problem in connection'
            break
        f.read(1024)


while True:
    conn, addr = s.accept()
    print 'Got connection from', addr
    while True:
        data = conn.recv(1024)
        if not data:
            break
        print "Request: "+data
        data = data.split()
        if data[1] == 'longlist':
            longlistFunc(conn)
        elif data[1] == 'shortlist':
            shortlistFunc(conn,data)
        elif data[1] == 'regex':
            regexFunc(conn,data)
        elif data[1] == 'verify':
            verifyFunc(conn,data)
        elif data[1] == 'checkall':
            checkallFunc(conn)
        elif data[1] == 'TCP':
            downloadTCPFunc(conn,data)
        elif data[1] == 'UDP':
            downloadUDPFunc(conn,data)
        print('Done sending')
        # conn.send('Thank you for connecting')
    conn.close()
