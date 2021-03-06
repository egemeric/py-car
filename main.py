import RPi.GPIO as gpio
import time
import sensor
import servercar 
gpio.setmode(gpio.BCM)
class motor_driver():
    
    def __init__(self,right_pin,left_pin,reverseleft_pin,reverseright_pin,led_pin,relay_pin):
        self.__right=right_pin
        self.__left=left_pin
        self.__reverseleft=reverseleft_pin
        self.__reverseright=reverseright_pin
        self.__led=led_pin
        self.__relay=relay_pin
        self.set_360=None # sharp Turn enable
        gpio.setup(self.__left,gpio.OUT)
        gpio.setup(self.__right,gpio.OUT)
        gpio.setup(self.__reverseleft,gpio.OUT)
        gpio.setup(self.__reverseright,gpio.OUT)
        gpio.setup(self.__led,gpio.OUT) #status led pin
        gpio.setup(self.__relay,gpio.OUT) #for motor driver's enable pin you can uncomment
        gpio.setwarnings(False)
        self.last_direction=None #if car goes Forward it's true (for reverse and forward movement(right or left) )
        print("Gpios has been seted!")

    
    def d_right(self,worktime=0.2):
        if(self.last_direction==True or self.last_direction==None):
            if(self.set_360==None or self.set_360==False):
                gpio.output(self.__right,gpio.HIGH)
                print("turn right")
                time.sleep(worktime)
                gpio.output(self.__right,gpio.LOW)
            else: #Sharp Turn right
                gpio.output(self.__right,gpio.HIGH)
                gpio.output(self.__reverseright,gpio.HIGH)
                time.sleep(worktime)
                gpio.output(self.__right,gpio.LOW)
                gpio.output(self.__reverseright,gpio.LOW)
        else:
            self.d_rev_right(worktime) #reverse right turn

    def d_left(self,worktime=0.2):
        if(self.last_direction==True or self.last_direction==None):
            if(self.set_360==None or self.set_360==False):
                gpio.output(self.__left,gpio.HIGH)
                print("turn left")
                time.sleep(worktime)
                gpio.output(self.__left,gpio.LOW)
            else: #sharp left turn
                gpio.output(self.__left,gpio.HIGH)
                gpio.output(self.__reverseleft,gpio.HIGH)
                time.sleep(worktime)
                gpio.output(self.__left,gpio.LOW)
                gpio.output(self.__reverseleft,gpio.LOW)
        else:
            self.d_rev_left(worktime) #reverse left turn

    def d_forward(self,worktime=0.2):
        gpio.output(self.__left,gpio.HIGH)
        gpio.output(self.__right,gpio.HIGH)
        print("turn forward")
        time.sleep(worktime)
        gpio.output(self.__left,gpio.LOW)
        gpio.output(self.__right,gpio.LOW)
        self.last_direction=True

    def d_stop(self):
        gpio.output(self.__left,gpio.LOW)
        gpio.output(self.__right,gpio.LOW)

    def d_reverse(self,worktime=0.2):
        gpio.output(self.__reverseleft,gpio.HIGH)
        gpio.output(self.__reverseright,gpio.HIGH)
        time.sleep(worktime)
        gpio.output(self.__reverseleft,gpio.LOW)
        gpio.output(self.__reverseright,gpio.LOW)
        self.last_direction=False
    
    def d_rev_left(self,worktime=0.2):
        gpio.output(self.__reverseleft,gpio.HIGH)
        time.sleep(worktime)
        gpio.output(self.__reverseleft,gpio.LOW)
    
    def d_rev_right(self,worktime=0.2):
        gpio.output(self.__reverseright,gpio.HIGH)
        time.sleep(worktime)
        gpio.output(self.__reverseright,gpio.LOW)

    def get_dist(self):
        return(sensor.main())

    def enable_driver(self):
        gpio.output(self.__relay,gpio.LOW)
        self.relaystatus=True

    def disable_driver(self):
        gpio.output(self.__relay,gpio.HIGH)
        self.relaystatus=False
    def enable_led(self):
        gpio.output(self.__led,gpio.HIGH)
        self.ledstatus=True
    def disable_led(self):
        gpio.output(self.__led,gpio.LOW)
        self.ledstatus=False
    def set_option_car(self,option):
        if(option==0):
            return(None)#nothinng has setted
        else:
            option=option.split("=")
            if(option[0]=="set"or option[0]=="unset"):
                pass #go to set variables
            else:
                return(False) #wrong language
        
        if(option[0]=="set"):
            if option[1]=="360":
                self.set_360=True
                return(True) # Ok
        elif(option[0]=="unset"):
            if option[1]=="360":
                self.set_360=False
                return(True) #Ok
       
            
        
right_pin=20
left_pin=21
left_reverse=19
right_reverse=26
relay_pin=12
led_pin=16

motor=motor_driver(right_pin,left_pin,left_reverse,right_reverse,led_pin,relay_pin) # set motor driver  , led and enable pins
rpi=servercar.cgi_gpio(8888) #start server on port tcp 8888

while(True):
    rpi.start_com()
    while(True):
        distance=motor.get_dist()
        dat_tuple=rpi.com_continue(str(distance)+"cm")
        motor.enable_driver()
        motor.enable_led()
        if dat_tuple==None:
            time.sleep(0.01)
            break
        else:
            char=dat_tuple[0]
            option=dat_tuple[1] #options will be added
            print("option=",option,"char=",char)
            op_res= motor.set_option_car(option)
            
        if(char=="w"):
            if(distance>40):
                motor.d_forward()
            elif(distance>10 and distance<41):
                motor.d_forward(0.01)
            else:
                motor.d_stop()
                print("NOT SAFE!!")
        elif(char=="a"):
            motor.d_left()
        elif(char=="d"):
            motor.d_right()
        elif(char=="s"):
            
            motor.d_reverse()
        elif(char=="q"):
            break
        elif(char=="T"):
            break
        else:
            if op_res==None:
                print("no option entry")
            elif op_res==True:
                print("Option has been setted")
            else:
                print("wrong option language")
            continue
    motor.disable_driver()
    motor.disable_led()
    if(char=="T"):
        break

del rpi
gpio.cleanup()
