import socket
import sys, tty, termios
import time
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch
class client():
    def __init__(self,ip_,portnum_):
        self.portnum_=portnum_
        self.ip_=ip_
        self.s = socket.socket()
        self.s.connect((self.ip_,self.portnum_))
    def handle_con(self,str):
        str="cmd,"+str
        self.s.send(str.encode())
        res=self.s.recv(1024)
        res=res.decode()
        return (res)
    def close_con(self):
        self.s.close()

#s.close()
cli=client("10.1.1.4",int(8888))
while True:
    ch=getch()
    if(ch=="q"):
        cli.handle_con(ch)
        cli.close_con()
        break
    else:
        s_time=","+str(time.time())
        res=cli.handle_con(ch+s_time)
        res=res.split(",")
        ping=time.time()-float(res[2])
        print (f"result:{res[1]}--tcp latency=%.5f"%(ping))
        time.sleep(0.1)
