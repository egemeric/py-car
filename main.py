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
        gpio.setup(self.__left,gpio.OUT)
        gpio.setup(self.__right,gpio.OUT)
        gpio.setup(self.__reverseleft,gpio.OUT)
        gpio.setup(self.__reverseright,gpio.OUT)
        gpio.setup(self.__led,gpio.OUT) #status led pin
        gpio.setup(self.relay,gpio.OUT) #for motor driver's enable pin you can uncomment
        gpio.setwarnings(False)
        print("Gpios has been seted!")

    def d_right(self,worktime=0.2):
        gpio.output(self.__right,gpio.HIGH)
        print("turn right")
        time.sleep(worktime)
        gpio.output(self.__right,gpio.LOW)

    def d_left(self,worktime=0.2):
        gpio.output(self.__left,gpio.HIGH)
        print("turn left")
        time.sleep(worktime)
        gpio.output(self.__left,gpio.LOW)

    def d_forward(self,worktime=0.2):
        gpio.output(self.__left,gpio.HIGH)
        gpio.output(self.__right,gpio.HIGH)
        print("turn forward")
        time.sleep(worktime=0.2)
        gpio.output(self.__left,gpio.LOW)
        gpio.output(self.__right,gpio.LOW)

    def d_stop(self):
        gpio.output(self.__left,gpio.LOW)
        gpio.output(self.__right,gpio.LOW)

    def d_reverse(slef,worktime=0.2):
        gpio.output(self.__reverseleft,gpio.HIGH)
        gpio.output(self.__reverseright,gpio.HIGH)
        time.sleep(worktime)
        gpio.output(self.__reverseleft,gpio.LOW)
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
        char=rpi.com_continue(str(distance)+"cm")
        motor.enable_driver()
        motor.enable_led()
        print(char)
        if char==None:
            time.sleep(0.01)
            break
        char=char[1]
        if(char=="w"):
            if(distance>35):
                motor.d_forward()
            elif(distance>25 and distance<36):
                motor.d_forward(0.1)
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
            print("invalid command")
            time.sleep(0.1)
            continue
    motor.disable_driver()
    motor.disable_led()
    if(char=="T"):
        break

del rpi
gpio.cleanup()
