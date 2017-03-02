import time, _thread as thread # or use threading.Thread().start()
from socket import * # get socket constructor and constants
from tkinter import *
import sqlite3
import socket, ssl, pprint

myHost = '' # server machine, '' means local host
myPort = 50007 # listen on a non-reserved port number
bindsocket = socket.socket()
bindsocket.bind((myHost, myPort))
bindsocket.listen(5)

def now():
    return time.ctime(time.time()) # current time on the server

def logfunction(address,time):
    conn = sqlite3.connect(r'server.db')
    c= conn.cursor()
    tblcmd = 'create table if not exists logs (ip char(30), port char(30), time char(30))'
    c.execute(tblcmd)
    data=address+(time,)
    c.execute('insert into logs values (? , ?, ?)',data)
    conn.commit()
    print('SSL Verification failed')
def handleClient(connection): # in spawned thread: reply
    time.sleep(5) # simulate a blocking activity
    conn = sqlite3.connect(r'server.db')
    c= conn.cursor()
    tblcmd = 'create table if not exists account (userid char(30), password char(10))'
    c.execute(tblcmd)
    c.execute('insert into account values (?, ?)', ('test', '1234'))
    tblcmd = 'create table if not exists measurement (height char(30), weight char(30), bp char(30))'
    c.execute(tblcmd)
    tblcmd = 'create table if not exists logs (ip char(30), port char(30), time char(30))'
    c.execute(tblcmd)
  
    while True: # read, write a client socket
        data = connection.recv(1024)
        print(data)
        if data.split(b'@')[0]==b'2':
            data1=data.decode()
            data1=data1.split('@')
            data1.remove('2')
            c.execute('insert into measurement values (? , ?, ?)',data1)
            conn.commit()
        if data.split(b'@')[0]==b'3':
           c.execute('SELECT * FROM measurement')
           lastdata=c.fetchall()
           l=len(lastdata)
           reply=lastdata[l-1][0]+','+lastdata[l-1][1]+','+lastdata[l-1][2]
           print(reply)
        else:
            uid=data.decode().split('@')[0]
            c.execute('SELECT * FROM account WHERE userid= ?',(uid,))
            chek=c.fetchall()
            if not data: break
            if not chek:
                reply = 'Flase'
            elif  data.decode().split('@')[0]== chek[0][0] and data.decode().split('@')[1]== chek[0][1]:
                reply = 'True'
            else:
                reply = 'Flase'
        connection.send(reply.encode())
        
    connection.close()
    
def dispatcher(): # listen until process killed
    while True:
        newsocket, address = bindsocket.accept()
        try:    
            connection = ssl.wrap_socket(newsocket,
                                 server_side=True,
                                 certfile="serverkey.pem",
                                 keyfile="serverkey.pem",
                                 ca_certs="clientkey.pem",
                                 cert_reqs=ssl.CERT_REQUIRED)
            print (repr(connection.getpeername()))
            print (connection.cipher())
            print (pprint.pformat(connection.getpeercert()))
            print('Server connected by', address, 'at', now())
            thread.start_new_thread(handleClient, (connection,))
        except:
            logfunction(address,now())

def makeWindow(myTitle):
    root = Tk()
    root.title(myTitle)
    label1 = Label(root, text='Server is running!')
    label1.pack()
    root.mainloop()

thread.start_new_thread(makeWindow, ('Server',))
dispatcher()

