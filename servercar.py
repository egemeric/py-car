import socket
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
        self.client.settimeout(10) #set timeout for 10 sec
        print(f"Yeni Baglanti:{self.address}")
    def com(self,send_data):
        try:
            self.recv_data=self.client.recv(1024).decode()
            self.parse_data()
            send_data=","+send_data+","+self.time_info 

            self.client.send(send_data.encode())

            if(self.client_header!="cmd"):
                print(f"{self.client_header}:")
                self.client.close()
                return None
            else:
                return self.command_char,self.option_car
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
    
    def parse_data(self):
        self.recv_data=self.recv_data.split(",")
        self.client_header=self.recv_data[0]
        self.command_char=self.recv_data[1]
        self.time_info=self.recv_data[2]
        if(len(self.recv_data)>3):
            self.option_car=self.recv_data[3]
        else:
            self.option_car=None
            pass
        

class cgi_gpio(server):

    def start_com(self):
        self.handle_tcp()

    def com_continue(self,Direction):
        dat=self.com(Direction)
        if(dat==None or dat=="q"):
            self.close_stream()
        else:
            return dat


print("servercar.py has imported!")
