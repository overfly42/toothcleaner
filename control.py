import RPi.GPIO as GPIO
from time import sleep
import counter

BTN_START_COUNTING = 7
BTN_REPEAT_COUNTING = 11
BTN_CHOOSE_DIRECTION = 13


#channel=7

#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(channel,GPIO.IN)
#def cb(value):
#    print('Got an edge from {}.'.format(value))
#GPIO.add_event_detect(channel,GPIO.RISING,callback=cb)
#for i in range(20):
#    print('Going to sleep')
#    sleep(1)

class master_control_program():
    def __init__(self) -> None:
        self.setup()
        self.state_maschine = counter.init_state_maschine(self.get_direction)

    def callback_start(self):
        if self.state_maschine.running == False:
            self.state_maschine.enter_state()
    
    def callback_repeat(self):
        counter.REPEAT = True
        
    def get_direction(self):
        if GPIO.input(BTN_CHOOSE_DIRECTION):
            return counter.count_direction.up
        else:
            return counter.count_direction.down
    
    def setup(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(BTN_START_COUNTING,GPIO.IN)
        GPIO.setup(BTN_REPEAT_COUNTING,GPIO.IN)
        GPIO.setup(BTN_CHOOSE_DIRECTION,GPIO.IN)
        #Set Callbacks
        GPIO.add_event_detect(BTN_START_COUNTING,GPIO.RISING,callback=self.callback_start)
        GPIO.add_event_detect(BTN_REPEAT_COUNTING,GPIO.RISING,callback=self.callback_repeat)
    
if __name__ == '__main__':
    mcp = master_control_program()
    while True:
        sleep(100)