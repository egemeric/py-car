import socket
import time
class server():
    def __init__(self,port_num):
        self.port_num=port_num

        try:
            self.s=socket.socket()

            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.bind(('',self.port_num))
            print(f"Socket binded:{self.port_num}")
            self.s.listen(1)
            print("socket has binded only 1 con available")
        except socket.error as err:
            print(f"Socket Creation Error:{err}")
    def handle_tcp(self):
        self.client,self.address=self.s.accept()
        self.client.settimeout(10)
        print(f"Yeni Baglanti:{self.address}")
    def com(self,send_data):
        try:
            self.data=self.client.recv(1024).decode()
            self.data=self.data.split(",")
            send_data=","+send_data+","+self.data[2]

            self.client.send(send_data.encode())

            if(self.data[0]!="cmd"):
                print(f"{self.data[0]}:")
                self.client.close()
                return None
            else:
                return self.data
        except(OSError):
            print("Unkown client")
            return None
        except(UnicodeDecodeError):
            print("'utf-8' codec can't decode (can be caused multiple connections)")
            return None
        except(IndexError):
            print("Info:Comminication has ended")


    def close_stream(self):
        print("closed")
        self.client.close()

class cgi_gpio(server):

    def start_com(self):
        self.handle_tcp()

    def com_continue(self,Direction):
        dat=self.com(Direction)
        if(dat==None or dat=="q"):
            self.close_stream()
        else:
            return dat


print("ok")


