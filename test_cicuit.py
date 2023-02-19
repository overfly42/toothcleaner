import RPi.GPIO as GPIO
from time import sleep

channel=3

GPIO.setmode(GPIO.BOARD)
GPIO.setup(channel,GPIO.IN)
def cb(value):
    print('Got an edge from {}.'.format(value))
GPIO.add_event_detect(channel,GPIO.RISING,callback=cb)
for i in range(20):
    print('Going to sleep')
    sleep(1)