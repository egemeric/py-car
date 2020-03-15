
import RPi.GPIO as gpio
import time
import sys, tty, termios
import sensor
gpio.setmode(gpio.BCM)
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def set_pins(left_,right_,rev_left,rev_right):
    gpio.setup(left_,gpio.OUT)
    gpio.setup(right_,gpio.OUT)
    gpio.setup(rev_left,gpio.OUT)
    gpio.setup(rev_right,gpio.OUT)
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
right_pin=20
left_pin=21
left_reverse=19
right_reverse=26
set_pins(left_pin,right_pin,left_reverse,right_reverse)
while(True):
    char=getch()
    distance=sensor.main()
    if(char=="w"):
        if(distance>25):
            print(f"{distance}cm")
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
    else:
        time.sleep(0.01)
        print("invalid command")
        pass
