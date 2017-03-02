import sys
from socket import *
from tkinter import * # get widget classes
from tkinter.messagebox import * # get standard dialogs
import socket, ssl, pprint

serverHost = '127.0.0.1' # server name
serverPort = 50007 # non-reserved port used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sockobj = ssl.wrap_socket(s,
                           certfile="clientkey.pem",
                           keyfile="clientkey.pem",
                           ca_certs="serverkey.pem",
                           cert_reqs=ssl.CERT_REQUIRED)

    sockobj.connect((serverHost, serverPort))

    print (repr(sockobj.getpeername()))
    print (sockobj.cipher())
    print (pprint.pformat(sockobj.getpeercert()))
    ssl=1;
except:
    ssl=0;

def default(ssl):
    if ssl==0:
        file.entryconfig(1, state=DISABLED)
        Account.entryconfig(1, state=DISABLED)
        Account.entryconfig(2, state=DISABLED)
        About.entryconfig(1, state=DISABLED)
        Measure.entryconfig(1, state=DISABLED)
        Measure.entryconfig(2, state=DISABLED)
        sslfail()
    return()
def sslfail():
    showerror('error', 'SSL Handshaking Failed!!')
    return
def current():
    def send():
        text1=hgt.get()
        text2=wht.get()
        text3=bp.get()
        message = [b'2'+b'@'+text1.encode()+b'@'+text2.encode()+b'@'+text3.encode()] # default text to send to server
            
        for line in message:
            sockobj.send(line) # send line to server over socket
            data = sockobj.recv(1024) # receive line from server: up to 1k
            print('Client received:', data) # bytes are quoted, was `x`, repr(x)
    
        close(win)
        return
    
    win=Toplevel()
    win.title('Measure')

    frame1=Frame(win)
    wgt= Label(frame1, text="Height:")
    wgt.pack(side=LEFT)
    hgt = Entry(frame1)
    hgt.insert(0,'')
    hgt.bind('<Return>', (lambda: send()))
    hgt.pack(side=RIGHT) 
    hgt.focus() 
    frame1.pack(side=TOP)

    frame3=Frame(win)
    wgt= Label(frame3, text="Weight:")
    wgt.pack(side=LEFT)
    wht = Entry(frame3)
    wht.insert(0,'')
    wht.bind('<Return>', (lambda: send()))
    wht.pack(side=RIGHT) 
    frame3.pack(side=TOP)

    frame4=Frame(win)
    wgt= Label(frame4, text="BP:")
    wgt.pack(side=LEFT)
    bp = Entry(frame4)
    bp.insert(0,'')
    bp.bind('<Return>', (lambda: send()))
    bp.pack(side=RIGHT) 
    frame4.pack(side=TOP)

    frame2 = Frame(win)
    btn1 = Button(frame2, text='Enter', command=send) 
    btn1.pack(side=LEFT)
    btn2 = Button(frame2, text='Quit', command=(lambda: close(win))) 
    btn2.pack(side=RIGHT)
    frame2.pack(side=TOP)

    return
def last():
   
    message = [b'3'+b'@'] # default text to send to server
            

    for line in message:
        sockobj.send(line) # send line to server over socket
        data = sockobj.recv(1024) # receive line from server: up to 1k
        print('Client received:', data) # bytes are quoted, was `x`, repr(x)
    
    win=Toplevel()
    win.title('Last Measurement')
    frame1=Frame(win)
    label=Label(frame1, text="Test")
    label.pack(side=TOP)
    label1=Label(frame1, text="Height:"+data.decode().split(',')[0])
    label1.pack(side=TOP)
    label2=Label(frame1, text="Weight:"+data.decode().split(',')[1])
    label2.pack(side=TOP)
    label3=Label(frame1, text="BP:"+data.decode().split(',')[2])
    label3.pack(side=TOP)
    frame1.pack(side=TOP)

    frame2 = Frame(win)
    btn2 = Button(frame2, text='Quit', command=(lambda: close(win))) 
    btn2.pack(side=RIGHT)
    frame2.pack(side=TOP)

        
    return

def save():
    if askokcancel('save','save?'):
        close(root)
    return

def classinfo():
    showinfo("Class info", "This is ECE424/ECE514")    
    return

def close(win):
    win.destroy()
    return

def alert(val):
    win1=Toplevel()
    win1.title('Info')
    frame1=Frame(win1)
    if val==1:
        pop= Label(frame1, text="log in sucessfully")
    elif val==2:
        pop= Label(frame1, text="log in unsucessfull")
    else:
        pop= Label(frame1, text="log out sucessfully")

    pop.pack(side=TOP)
    btn1 = Button(frame1, text='OK', command=(lambda: close(win1))) 
    btn1.pack(side=BOTTOM)
    frame1.pack(side=TOP)
    return

    
def login():

     def check():
        text1=nme.get()
        text2=psw.get()
        print(text1)
        message = [text1.encode()+b'@'+text2.encode()] # default text to send to server
            
        for line in message:
            sockobj.send(line) # send line to server over socket
            data = sockobj.recv(1024) # receive line from server: up to 1k
            print('Client received:', data) # bytes are quoted, was `x`, repr(x)
    
        if data==b'True':
            close(win)
            print("login")
            alert(1)
            change(1)
        else:
            close(win)
            alert(2)
            print("notlogin")
        return
    
     win=Toplevel()
     win.title('Login')

     frame1=Frame(win)
     wgt= Label(frame1, text="Name:")
     wgt.pack(side=LEFT)
     nme = Entry(frame1)
     nme.insert(0, 'Name')
     nme.bind('<Return>', (lambda: check()))
     nme.pack(side=RIGHT) 
     nme.focus() 
     frame1.pack(side=TOP)

     frame3=Frame(win)
     wgt= Label(frame3, text="ID:")
     wgt.pack(side=LEFT)
     psw = Entry(frame3)
     psw.insert(0, 'password')
     psw.bind('<Return>', (lambda: check()))
     psw.pack(side=RIGHT) 
     frame3.pack(side=TOP)

     frame2 = Frame(win)
     btn1 = Button(frame2, text='Enter', command=check) 
     btn1.pack(side=LEFT)
     btn2 = Button(frame2, text='Quit', command=(lambda: close(win))) 
     btn2.pack(side=RIGHT)
     frame2.pack(side=TOP)

     return

def logout():
    def logoutdone():
         close(win3)
         alert(3)
         change(2)
         return
    win3=Toplevel()
    win3.title('Log Out')
    frame1 = Frame(win3)
    pop= Label(frame1, text="log Out?")
    pop.pack(side=TOP)
    btn1 = Button(frame1, text='Yes', command=logoutdone) 
    btn1.pack(side=LEFT)
    btn2 = Button(frame1, text='No', command=(lambda: close(win3))) 
    btn2.pack(side=RIGHT)
    frame1.pack(side=TOP)
    return

def change(val):
    if val==1:
        file.entryconfig(1, state=NORMAL)
        Account.entryconfig(1, state=DISABLED)
        Account.entryconfig(2, state=NORMAL)
        About.entryconfig(1, state=DISABLED)
        Measure.entryconfig(1, state=NORMAL)
        Measure.entryconfig(2, state=NORMAL)
    else:
        file.entryconfig(1, state=DISABLED)
        Account.entryconfig(1, state=NORMAL)
        Account.entryconfig(2, state=DISABLED)
        About.entryconfig(1, state=NORMAL)
        Measure.entryconfig(1, state=DISABLED)
        Measure.entryconfig(1, state=DISABLED)
        
    return


    
def makemenu(win):
    top = Menu(win) 
    win.config(menu=top)
    global file,Account,About,Measure
    file = Menu(top, tearoff=True)
    file.add_command(label='save', command=save, underline=0, state=DISABLED)
    top.add_cascade(label='File', menu=file, underline=0)
    Account = Menu(top, tearoff=True)
    Account.add_command(label='Log In', command=login, underline=0, state=NORMAL)
    Account.add_command(label='Log Out', command=logout, underline=0, state=DISABLED)
    top.add_cascade(label='Account', menu=Account, underline=0)
    Measure = Menu(top, tearoff=True)
    Measure.add_command(label='Current', command=current, state=DISABLED)
    Measure.add_command(label='last', command=last, state=DISABLED)
    top.add_cascade(label='Measure', menu=Measure)
    About = Menu(top, tearoff=True)
    About.add_command(label='class Info', command=classinfo, underline=0, state=NORMAL)
    top.add_cascade(label='About', menu=About, underline=0)
    default(ssl)
    
if __name__ == '__main__':
    root = Tk() # or Toplevel()
    root.title('client DEMO') # set window-mgr info
    makemenu(root) # associate a menu bar
    msg = Label(root, text='Window menu basics') # add something below
    msg.pack(expand=YES, fill=BOTH)
    msg.config(width=40, height=20)
    root.mainloop()
