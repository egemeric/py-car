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
    def handle_con(self,char):
        
        str="cmd,"+char+self.send_client_time()
        self.s.send(str.encode())
        self.res_raw=self.s.recv(1024) #get raw data
        self.parse_data() #you need to parse, to calc ping or to access parsed data (self.result) 
        
    def parse_data(self):
        res=self.res_raw.decode()
        res=res.split(",")
        self.result=res
        
    def close_con(self):
        self.s.close()
    def send_client_time(self):
        self.s_time=","+str(time.time()) #with "," language
        return(self.s_time)
    def calc_ping(self):
        self.ping=time.time()-float(self.result[2])
        return(self.ping)

server_ip="10.1.1.4"
port_num=8888
    
cli=client(server_ip,int(port_num)) #start com cannel
while True:
    ch=getch()
    if(ch=="q"):
        cli.handle_con(ch)
        cli.close_con()
        break
    elif(ch=="O"): # will be options
        pass
        
    else:
        try:
            cli.handle_con(ch)
            res=cli.result
            print (f"sensor:{res[1]}  --tcp latency=%.3fms"%(cli.calc_ping()))
            time.sleep(0.1)
        except(IndexError):
            print("Connection timeout (10 sec) ") # if you dont send a command to server for 10 sec server closes the channel
            print("Creating new channel...")
            time.sleep(1)
            del cli
            cli=client(server_ip,int(port_num))
            print("New channel is created from:%s port:%d."%cli.s.getsockname())
