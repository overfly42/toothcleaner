import RPi.GPIO as GPIO
from time import sleep

channel_a=11
channel_b=13
channel_c=15

GPIO.setmode(GPIO.BOARD)
GPIO.setup(channel_a,GPIO.IN)
GPIO.setup(channel_b,GPIO.IN)
GPIO.setup(channel_c,GPIO.IN)

def cb(value):
    print('Got an edge from {}.'.format(value))
GPIO.add_event_detect(channel_a,GPIO.RISING,callback=cb)
GPIO.add_event_detect(channel_b,GPIO.RISING,callback=cb)
GPIO.add_event_detect(channel_c,GPIO.RISING,callback=cb)
for i in range(20):
    print('current state for a is {}'.format(GPIO.input(channel_a)))
    print('current state for a is {}'.format(GPIO.input(channel_b)))
    print('current state for a is {}'.format(GPIO.input(channel_c)))
    print('Going to sleep')
    sleep(1)