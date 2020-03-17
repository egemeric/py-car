import RPi.GPIO as gpio
import time
import sensor
import servercar 
gpio.setmode(gpio.BCM)
def set_pins(left_,right_,rev_left,rev_right):
    gpio.setup(left_,gpio.OUT)
    gpio.setup(right_,gpio.OUT)
    gpio.setup(rev_left,gpio.OUT)
    gpio.setup(rev_right,gpio.OUT)
    gpio.setup(16,gpio.OUT) #led pin
    gpio.output(16,gpio.HIGH)
    gpio.setwarnings(False)
    print("Gpios has been seted:",left_,",",right_)
def d_right(right_):
    gpio.output(right_,gpio.HIGH)
    print("turn right")
    time.sleep(0.2)
    gpio.output(right_,gpio.LOW)
def d_left(left_):
    gpio.output(left_,gpio.HIGH)
    print("turn left")
    time.sleep(0.2)
    gpio.output(left_,gpio.LOW)
def d_forward(left_,right_):
    gpio.output(left_,gpio.HIGH)
    gpio.output(right_,gpio.HIGH)
    print("turn forward")
    time.sleep(0.2)
    gpio.output(left_,gpio.LOW)
    gpio.output(right_,gpio.LOW)
def d_stop(left_,right_):
    gpio.output(left_,gpio.LOW)
    gpio.output(right_,gpio.LOW)
def d_reverse(rev_left,rev_right):
    gpio.output(rev_left,gpio.HIGH)
    gpio.output(rev_right,gpio.HIGH)
    time.sleep(0.2)
    gpio.output(rev_left,gpio.LOW)
    gpio.output(rev_right,gpio.LOW)
def get_dist():
    return(sensor.main())
right_pin=20
left_pin=21
left_reverse=19
right_reverse=26
set_pins(left_pin,right_pin,left_reverse,right_reverse)
rpi=servercar.cgi_gpio(8888) #start server on port tcp 8888

while(True):
    rpi.start_com()
    while(True):
        distance=get_dist()
        char=rpi.com_continue(str(distance)+"cm")
        print(char)
        if char==None:
            time.sleep(0.01)
            break
        char=char[1]
        if(char=="w"):
            if(distance>25):
                d_forward(left_pin,right_pin)
            else:
                print("NOT SAFE!!")
        elif(char=="a"):
            d_left(left_pin)
        elif(char=="d"):
            d_right(right_pin)
        elif(char=="s"):
            d_stop(left_pin,right_pin)
            d_reverse(left_reverse,right_reverse)
        elif(char=="q"):
            gpio.cleanup()
            exit(0)
        elif(char=="T"):
            break
        else:
            print("invalid command")
            time.sleep(0.1)
            continue
    if(char=="T"):
        break

del rpi
gpio.cleanup()
